# file_metrics_analyzer.py
"""
File Metrics Analyzer for Wolfkit
Analyzes file sizes and provides actionable feedback for code quality
"""
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class SizeCategory(Enum):
    """File size categories with severity levels"""
    OPTIMAL = "optimal"        # ≤ 400 lines
    ACCEPTABLE = "acceptable"  # 401-600 lines  
    WARNING = "warning"        # 601-800 lines
    CRITICAL = "critical"      # 801-1200 lines
    DANGEROUS = "dangerous"    # >1200 lines


@dataclass
class FileMetrics:
    """Metrics for a single file"""
    file_path: str
    relative_path: str
    line_count: int
    size_category: SizeCategory
    lines_over_optimal: int
    complexity_indicators: Dict[str, int] = field(default_factory=dict)
    suggested_action: str = ""
    refactoring_suggestions: List[str] = field(default_factory=list)


@dataclass
class ProjectMetrics:
    """Overall project file size metrics"""
    total_files: int
    average_file_size: float
    largest_file: Optional[FileMetrics]
    files_by_category: Dict[SizeCategory, List[FileMetrics]] = field(default_factory=dict)
    problematic_files: List[FileMetrics] = field(default_factory=list)  # WARNING+ files
    summary_stats: Dict[str, int] = field(default_factory=dict)


class FileSizeThresholds:
    """Configurable file size thresholds"""
    
    PRESETS = {
        "strict": {"optimal": 250, "acceptable": 400, "warning": 500, "critical": 700},
        "standard": {"optimal": 400, "acceptable": 600, "warning": 800, "critical": 1200},
        "relaxed": {"optimal": 600, "acceptable": 800, "warning": 1000, "critical": 1500},
        "legacy": {"optimal": 800, "acceptable": 1200, "warning": 1500, "critical": 2000}
    }
    
    def __init__(self, preset: str = "standard", custom_thresholds: Optional[Dict] = None):
        """
        Initialize thresholds
        
        Args:
            preset: Preset name ("strict", "standard", "relaxed", "legacy")
            custom_thresholds: Override with custom values
        """
        if custom_thresholds:
            self.thresholds = custom_thresholds
        else:
            self.thresholds = self.PRESETS.get(preset, self.PRESETS["standard"])
    
    def categorize_file_size(self, line_count: int) -> SizeCategory:
        """Categorize file size based on line count"""
        if line_count <= self.thresholds["optimal"]:
            return SizeCategory.OPTIMAL
        elif line_count <= self.thresholds["acceptable"]:
            return SizeCategory.ACCEPTABLE
        elif line_count <= self.thresholds["warning"]:
            return SizeCategory.WARNING
        elif line_count <= self.thresholds["critical"]:
            return SizeCategory.CRITICAL
        else:
            return SizeCategory.DANGEROUS


class FileMetricsAnalyzer:
    """
    Analyzes file sizes and provides detailed metrics for code quality assessment
    """
    
    def __init__(self, thresholds: FileSizeThresholds = None):
        """
        Initialize analyzer
        
        Args:
            thresholds: File size thresholds (defaults to standard)
        """
        self.thresholds = thresholds or FileSizeThresholds()
        
        # File extensions to analyze
        self.source_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
            '.json', '.md', '.txt', '.yml', '.yaml', '.java',
            '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs'
        }
        
        # Directories to skip
        self.skip_dirs = {
            'node_modules', 'venv', 'env', '.git', '__pycache__',
            '.pytest_cache', 'dist', 'build', '.vscode', '.idea',
            'coverage', '.coverage', 'htmlcov', '.tox', 'target'
        }
    
    def analyze_files(self, file_paths: List[str]) -> ProjectMetrics:
        """
        Analyze a list of specific files
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            ProjectMetrics with analysis results
        """
        file_metrics = []
        
        for file_path in file_paths:
            if os.path.exists(file_path) and self._is_source_file(file_path):
                metrics = self._analyze_single_file(file_path)
                if metrics:
                    file_metrics.append(metrics)
        
        return self._compile_project_metrics(file_metrics)
    
    def analyze_project(self, project_path: str) -> ProjectMetrics:
        """
        Analyze all source files in a project directory
        
        Args:
            project_path: Path to project root
            
        Returns:
            ProjectMetrics with analysis results
        """
        file_metrics = []
        project_root = Path(project_path)
        
        for file_path in self._get_source_files(project_root):
            metrics = self._analyze_single_file(str(file_path), str(project_root))
            if metrics:
                file_metrics.append(metrics)
        
        return self._compile_project_metrics(file_metrics)
    
    def _analyze_single_file(self, file_path: str, project_root: str = None) -> Optional[FileMetrics]:
        """
        Analyze a single file for size metrics
        
        Args:
            file_path: Path to file
            project_root: Project root for relative path calculation
            
        Returns:
            FileMetrics or None if analysis fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Count non-empty lines (more meaningful than total lines)
            line_count = len([line for line in lines if line.strip()])
            
            # Calculate relative path
            if project_root:
                relative_path = str(Path(file_path).relative_to(project_root))
            else:
                relative_path = os.path.basename(file_path)
            
            # Categorize file size
            category = self.thresholds.categorize_file_size(line_count)
            lines_over = max(0, line_count - self.thresholds.thresholds["optimal"])
            
            # Generate suggestions
            suggested_action, refactoring_suggestions = self._generate_suggestions(
                file_path, line_count, category
            )
            
            # Calculate complexity indicators
            complexity = self._calculate_complexity_indicators(lines, file_path)
            
            return FileMetrics(
                file_path=file_path,
                relative_path=relative_path,
                line_count=line_count,
                size_category=category,
                lines_over_optimal=lines_over,
                complexity_indicators=complexity,
                suggested_action=suggested_action,
                refactoring_suggestions=refactoring_suggestions
            )
            
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
            return None
    
    def _generate_suggestions(self, file_path: str, line_count: int, 
                            category: SizeCategory) -> Tuple[str, List[str]]:
        """
        Generate refactoring suggestions based on file size and type
        
        Returns:
            Tuple of (main_suggestion, detailed_suggestions_list)
        """
        file_ext = Path(file_path).suffix.lower()
        file_name = Path(file_path).stem.lower()
        
        suggestions = []
        
        if category == SizeCategory.OPTIMAL:
            return "No action needed - file size is optimal", []
        elif category == SizeCategory.ACCEPTABLE:
            return "Monitor file growth", ["Consider refactoring if adding significant functionality"]
        
        # Generate specific suggestions based on file type and name
        if 'model' in file_name and file_ext == '.py':
            suggestions.extend([
                "Split into separate model files by domain (user_models.py, product_models.py)",
                "Extract shared base classes into base_models.py",
                "Move validation logic to separate validators module"
            ])
        elif 'api' in file_name or 'handler' in file_name:
            suggestions.extend([
                "Split endpoints by feature area into separate files",
                "Extract common middleware to shared module",
                "Move validation schemas to separate schemas file"
            ])
        elif 'util' in file_name or 'helper' in file_name:
            suggestions.extend([
                "Group related utilities into specialized modules",
                "Extract data processing functions to data_utils.py",
                "Move file operations to file_utils.py"
            ])
        elif file_ext == '.js' or file_ext == '.ts':
            suggestions.extend([
                "Split into smaller, feature-focused modules",
                "Extract shared utilities to separate files",
                "Consider using module federation for large components"
            ])
        
        # General suggestions based on severity
        if category == SizeCategory.WARNING:
            main_action = "Should be refactored soon"
            suggestions.insert(0, "Break file into 2-3 smaller, focused modules")
        elif category == SizeCategory.CRITICAL:
            main_action = "Requires refactoring within next sprint"
            suggestions.insert(0, "Urgent: Split into multiple files by responsibility")
        else:  # DANGEROUS
            main_action = "IMMEDIATE refactoring required"
            suggestions.insert(0, "Critical: File violates single responsibility principle")
            suggestions.append("Consider architectural review of this component")
        
        return main_action, suggestions
    
    def _calculate_complexity_indicators(self, lines: List[str], file_path: str) -> Dict[str, int]:
        """
        Calculate basic complexity indicators
        
        Args:
            lines: File lines
            file_path: Path to file for type-specific analysis
            
        Returns:
            Dictionary of complexity metrics
        """
        file_ext = Path(file_path).suffix.lower()
        
        complexity = {
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip()]),
            "comment_lines": 0,
            "function_count": 0,
            "class_count": 0,
            "max_nesting_depth": 0
        }
        
        current_nesting = 0
        max_nesting = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Count comments
            if file_ext == '.py' and (stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''")):
                complexity["comment_lines"] += 1
            elif file_ext in ['.js', '.ts'] and (stripped.startswith('//') or stripped.startswith('/*')):
                complexity["comment_lines"] += 1
            
            # Count functions and classes (basic pattern matching)
            if file_ext == '.py':
                if stripped.startswith('def '):
                    complexity["function_count"] += 1
                elif stripped.startswith('class '):
                    complexity["class_count"] += 1
                
                # Track nesting depth (simplified)
                if any(stripped.startswith(kw) for kw in ['if ', 'for ', 'while ', 'try:', 'with ']):
                    current_nesting += 1
                    max_nesting = max(max_nesting, current_nesting)
                elif stripped.startswith(('else:', 'elif ', 'except', 'finally:')):
                    pass  # Same level
                elif not stripped and current_nesting > 0:
                    current_nesting = max(0, current_nesting - 1)
            
            elif file_ext in ['.js', '.ts']:
                if 'function ' in stripped or '=>' in stripped:
                    complexity["function_count"] += 1
                elif 'class ' in stripped:
                    complexity["class_count"] += 1
        
        complexity["max_nesting_depth"] = max_nesting
        complexity["comment_ratio"] = (complexity["comment_lines"] / complexity["code_lines"]) * 100 if complexity["code_lines"] > 0 else 0
        
        return complexity
    
    def _compile_project_metrics(self, file_metrics: List[FileMetrics]) -> ProjectMetrics:
        """
        Compile individual file metrics into project-wide metrics
        
        Args:
            file_metrics: List of FileMetrics
            
        Returns:
            ProjectMetrics with aggregated data
        """
        if not file_metrics:
            return ProjectMetrics(total_files=0, average_file_size=0, largest_file=None)
        
        # Group files by category
        files_by_category = {category: [] for category in SizeCategory}
        for metrics in file_metrics:
            files_by_category[metrics.size_category].append(metrics)
        
        # Find problematic files (WARNING level and above)
        problematic_files = []
        for category in [SizeCategory.WARNING, SizeCategory.CRITICAL, SizeCategory.DANGEROUS]:
            problematic_files.extend(files_by_category[category])
        
        # Sort problematic files by line count (descending)
        problematic_files.sort(key=lambda x: x.line_count, reverse=True)
        
        # Calculate summary stats
        total_lines = sum(m.line_count for m in file_metrics)
        average_size = total_lines / len(file_metrics)
        largest_file = max(file_metrics, key=lambda x: x.line_count)
        
        summary_stats = {
            "total_files": len(file_metrics),
            "total_lines": total_lines,
            "optimal_files": len(files_by_category[SizeCategory.OPTIMAL]),
            "acceptable_files": len(files_by_category[SizeCategory.ACCEPTABLE]),
            "warning_files": len(files_by_category[SizeCategory.WARNING]),
            "critical_files": len(files_by_category[SizeCategory.CRITICAL]),
            "dangerous_files": len(files_by_category[SizeCategory.DANGEROUS]),
            "files_over_optimal": len(file_metrics) - len(files_by_category[SizeCategory.OPTIMAL]),
            "files_needing_action": len(problematic_files)
        }
        
        return ProjectMetrics(
            total_files=len(file_metrics),
            average_file_size=average_size,
            largest_file=largest_file,
            files_by_category=files_by_category,
            problematic_files=problematic_files,
            summary_stats=summary_stats
        )
    
    def _get_source_files(self, project_root: Path):
        """
        Generator for source files in project
        
        Args:
            project_root: Project root directory
            
        Yields:
            Path objects for source files
        """
        for root, dirs, files in os.walk(project_root):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self._is_source_file(str(file_path)):
                    yield file_path
    
    def _is_source_file(self, file_path: str) -> bool:
        """
        Check if file is a source file we should analyze
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file should be analyzed
        """
        file_path = Path(file_path)
        return (file_path.suffix.lower() in self.source_extensions and 
                file_path.stat().st_size > 0)  # Skip empty files


def format_file_size_summary(metrics: ProjectMetrics, show_all_files: bool = False) -> str:
    """
    Format file size analysis summary for console output
    
    Args:
        metrics: ProjectMetrics to format
        show_all_files: Whether to show all files or just problematic ones
        
    Returns:
        Formatted string for console output
    """
    if metrics.total_files == 0:
        return "No source files found for analysis."
    
    summary = f"""📊 File Size Analysis Complete!
✅ {metrics.summary_stats['optimal_files']} files within optimal range
⚠️  {metrics.summary_stats['files_needing_action']} files need attention
📈 Average file size: {metrics.average_file_size:.0f} lines
"""
    
    # Show problematic files explicitly
    if metrics.problematic_files:
        summary += "\n"
        
        # Group by severity
        dangerous_files = [f for f in metrics.problematic_files if f.size_category == SizeCategory.DANGEROUS]
        critical_files = [f for f in metrics.problematic_files if f.size_category == SizeCategory.CRITICAL]
        warning_files = [f for f in metrics.problematic_files if f.size_category == SizeCategory.WARNING]
        
        if dangerous_files:
            summary += "🚨 DANGEROUS FILES (>1200 lines) - IMMEDIATE ACTION REQUIRED:\n"
            summary += "━" * 60 + "\n"
            for file in dangerous_files:
                summary += f"• {file.relative_path} ({file.line_count} lines) - {file.lines_over_optimal} lines over optimal\n"
                summary += f"  └─ {file.suggested_action}\n"
            summary += "\n"
        
        if critical_files:
            summary += "🔥 CRITICAL FILES (800-1200 lines) - URGENT REFACTORING NEEDED:\n"
            summary += "━" * 60 + "\n"
            for file in critical_files:
                summary += f"• {file.relative_path} ({file.line_count} lines) - {file.lines_over_optimal} lines over optimal\n"
                summary += f"  └─ {file.suggested_action}\n"
            summary += "\n"
        
        if warning_files:
            summary += "⚠️  WARNING FILES (600-800 lines) - SHOULD BE REFACTORED:\n"
            summary += "━" * 60 + "\n"
            for file in warning_files:
                summary += f"• {file.relative_path} ({file.line_count} lines) - {file.lines_over_optimal} lines over optimal\n"
                summary += f"  └─ {file.suggested_action}\n"
        
        # Add refactoring suggestions for top 3 problematic files
        summary += "\n💡 TOP REFACTORING SUGGESTIONS:\n"
        for i, file in enumerate(metrics.problematic_files[:3], 1):
            summary += f"{i}. {file.relative_path}:\n"
            for suggestion in file.refactoring_suggestions[:2]:  # Show top 2 suggestions
                summary += f"   • {suggestion}\n"
    
    return summary


def generate_file_size_report_section(metrics: ProjectMetrics) -> str:
    """
    Generate markdown section for file size analysis
    
    Args:
        metrics: ProjectMetrics to format
        
    Returns:
        Markdown formatted section
    """
    if metrics.total_files == 0:
        return "## 📏 File Size Analysis\n\nNo source files found for analysis.\n"
    
    report = f"""## 📏 File Size Analysis

### Summary
- **Total Files Analyzed:** {metrics.total_files}
- **Average File Size:** {metrics.average_file_size:.0f} lines
- **Largest File:** {metrics.largest_file.relative_path} ({metrics.largest_file.line_count} lines)
- **Files Over Optimal (400+ lines):** {metrics.summary_stats['files_over_optimal']}
- **Files Requiring Action (600+ lines):** {metrics.summary_stats['files_needing_action']}

"""
    
    # Add problematic files tables
    if metrics.files_by_category[SizeCategory.DANGEROUS]:
        report += "### 🚨 Dangerous Files (>1200 lines)\n"
        report += "| File | Lines | Over Optimal | Action Required |\n"
        report += "|------|-------|--------------|------------------|\n"
        for file in metrics.files_by_category[SizeCategory.DANGEROUS]:
            report += f"| `{file.relative_path}` | {file.line_count} | +{file.lines_over_optimal} | {file.suggested_action} |\n"
        report += "\n"
    
    if metrics.files_by_category[SizeCategory.CRITICAL]:
        report += "### 🔥 Critical Files (800-1200 lines)\n"
        report += "| File | Lines | Over Optimal | Action Required |\n"
        report += "|------|-------|--------------|------------------|\n"
        for file in metrics.files_by_category[SizeCategory.CRITICAL]:
            report += f"| `{file.relative_path}` | {file.line_count} | +{file.lines_over_optimal} | {file.suggested_action} |\n"
        report += "\n"
    
    if metrics.files_by_category[SizeCategory.WARNING]:
        report += "### ⚠️ Warning Files (600-799 lines)\n"
        report += "| File | Lines | Over Optimal | Action Required |\n"
        report += "|------|-------|--------------|------------------|\n"
        for file in metrics.files_by_category[SizeCategory.WARNING]:
            report += f"| `{file.relative_path}` | {file.line_count} | +{file.lines_over_optimal} | {file.suggested_action} |\n"
        report += "\n"
    
    # File size distribution
    report += f"""### 📊 File Size Distribution
- **Optimal (≤400 lines):** {metrics.summary_stats['optimal_files']} files
- **Acceptable (401-600 lines):** {metrics.summary_stats['acceptable_files']} files  
- **Warning (601-800 lines):** {metrics.summary_stats['warning_files']} files
- **Critical (801-1200 lines):** {metrics.summary_stats['critical_files']} files
- **Dangerous (>1200 lines):** {metrics.summary_stats['dangerous_files']} files

"""
    
    return report
