# multi_file_analyzer.py (Enhanced with File Size Analysis - Fixed)
"""
Enhanced Multi-File Analyzer for Wolfkit - Now with integrated file size analysis
Coordinates multi-file analysis with comprehensive file metrics
"""
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Import our new file metrics analyzer
from file_metrics_analyzer import (
    FileMetricsAnalyzer, 
    FileSizeThresholds, 
    ProjectMetrics,
    format_file_size_summary,
    generate_file_size_report_section
)

# Import existing components
from code_context_analyzer import CodeContextAnalyzer
from dependency_mapper import DependencyMapper


class AnalysisScope(Enum):
    """Analysis scope options"""
    SINGLE = "single"
    MODULE = "module" 
    PROJECT = "project"


@dataclass
class AnalysisResult:
    """Enhanced analysis result with file size metrics"""
    success: bool
    target_files: List[str]
    analysis_scope: str
    analysis_content: str
    context_summary: Dict = field(default_factory=dict)
    file_metrics: Optional[ProjectMetrics] = None  # NEW: File size analysis
    error_message: str = ""


class MultiFileAnalyzer:
    """
    Enhanced multi-file analyzer with integrated file size analysis
    """
    
    def __init__(self, openai_client, include_file_analysis: bool = True, 
                 file_size_preset: str = "standard"):
        """
        Initialize enhanced multi-file analyzer
        
        Args:
            openai_client: OpenAI client for AI analysis
            include_file_analysis: Whether to include file size analysis
            file_size_preset: File size threshold preset ("strict", "standard", "relaxed", "legacy")
        """
        self.client = openai_client
        self.context_analyzer = CodeContextAnalyzer()
        self.dependency_mapper = DependencyMapper()
        
        # NEW: File metrics components
        self.include_file_analysis = include_file_analysis
        self.file_thresholds = FileSizeThresholds(preset=file_size_preset)
        self.file_analyzer = FileMetricsAnalyzer(self.file_thresholds)
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def analyze_as_module(self, file_paths: List[str]) -> AnalysisResult:
        """
        Analyze files as a cohesive module with file size analysis
        
        Args:
            file_paths: List of file paths to analyze as module
            
        Returns:
            Enhanced AnalysisResult with file metrics
        """
        try:
            # Step 1: Build context for the module (FIXED METHOD CALL)
            context = self.context_analyzer.analyze_file_relationships(file_paths)
            
            # Step 2: Map dependencies within the module (FIXED METHOD CALL)
            dependencies = self.dependency_mapper.analyze_files(file_paths)
            
            # Step 3: NEW - Analyze file sizes
            file_metrics = None
            if self.include_file_analysis:
                file_metrics = self.file_analyzer.analyze_files(file_paths)
            
            # Step 4: Generate AI analysis with enhanced context
            analysis_content = self._generate_module_analysis(
                file_paths, context, dependencies, file_metrics
            )
            
            # Step 5: Create context summary
            context_summary = self._create_context_summary(context, dependencies, file_metrics)
            
            return AnalysisResult(
                success=True,
                target_files=file_paths,
                analysis_scope="module",
                analysis_content=analysis_content,
                context_summary=context_summary,
                file_metrics=file_metrics
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                target_files=file_paths,
                analysis_scope="module",
                analysis_content="",
                error_message=f"Module analysis failed: {str(e)}"
            )
    
    def analyze_as_project(self, project_path: str) -> AnalysisResult:
        """
        Analyze entire project with comprehensive file size analysis
        
        Args:
            project_path: Path to project root
            
        Returns:
            Enhanced AnalysisResult with comprehensive metrics
        """
        try:
            # Step 1: Discover all relevant files in project
            project_files = self._discover_project_files(project_path)
            
            # Step 2: Build project context (unchanged - this method exists)
            context = self.context_analyzer.analyze_project_structure(project_path)
            
            # Step 3: Map project dependencies (FIXED METHOD CALL)
            dependencies = self.dependency_mapper.analyze_project(project_path)
            
            # Step 4: NEW - Comprehensive file size analysis
            file_metrics = None
            if self.include_file_analysis:
                file_metrics = self.file_analyzer.analyze_project(project_path)
            
            # Step 5: Generate AI analysis with full project context
            analysis_content = self._generate_project_analysis(
                project_path, context, dependencies, file_metrics
            )
            
            # Step 6: Create comprehensive context summary
            context_summary = self._create_context_summary(context, dependencies, file_metrics)
            context_summary['project_path'] = project_path
            context_summary['total_files'] = len(project_files)
            
            return AnalysisResult(
                success=True,
                target_files=project_files,
                analysis_scope="project",
                analysis_content=analysis_content,
                context_summary=context_summary,
                file_metrics=file_metrics
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                target_files=[],
                analysis_scope="project",
                analysis_content="",
                error_message=f"Project analysis failed: {str(e)}"
            )
    
    def _generate_module_analysis(self, file_paths: List[str], context: Dict, 
                                 dependencies: Dict, file_metrics: Optional[ProjectMetrics]) -> str:
        """
        Generate AI analysis for module with file size considerations
        """
        # Prepare context for AI
        module_context = self._prepare_module_context(file_paths, context, dependencies)
        
        # NEW: Add file size context if available
        file_size_context = ""
        if file_metrics and file_metrics.problematic_files:
            file_size_context = f"""

FILE SIZE ANALYSIS:
- {len(file_metrics.problematic_files)} files exceed optimal size limits
- Largest file: {file_metrics.largest_file.relative_path} ({file_metrics.largest_file.line_count} lines)
- Files needing attention: {', '.join([f.relative_path for f in file_metrics.problematic_files])}
"""
        
        prompt = f"""You are an expert code reviewer analyzing a module of related files. 

ANALYSIS CONTEXT:
{module_context}{file_size_context}

Please provide a comprehensive module analysis covering:

1. **Cross-File Integration**: How well do these files work together?
2. **Missing Dependencies**: Any imports/functions that are undefined but might be available?
3. **Module Cohesion**: Does this group of files form a logical, cohesive module?
4. **Architecture Assessment**: Is the module structure sound and maintainable?
5. **File Size Considerations**: Comment on any oversized files and refactoring opportunities
6. **Recommendations**: Specific actionable improvements

Format your response as a clear, professional analysis with specific examples and actionable recommendations.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert software architect and code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            ai_analysis = response.choices[0].message.content
            
            # Combine AI analysis with file size summary
            if file_metrics:
                file_size_summary = format_file_size_summary(file_metrics)
                return f"{ai_analysis}\n\n---\n\n{file_size_summary}"
            
            return ai_analysis
            
        except Exception as e:
            return f"AI analysis failed: {str(e)}"
    
    def _generate_project_analysis(self, project_path: str, context: Dict, 
                                  dependencies: Dict, file_metrics: Optional[ProjectMetrics]) -> str:
        """
        Generate AI analysis for entire project with comprehensive file metrics
        """
        # Prepare project context
        project_context = self._prepare_project_context(project_path, context, dependencies)
        
        # NEW: Add comprehensive file size analysis
        file_size_context = ""
        if file_metrics:
            file_size_context = f"""

COMPREHENSIVE FILE SIZE ANALYSIS:
- Total files: {file_metrics.total_files}
- Average file size: {file_metrics.average_file_size:.0f} lines
- Files needing immediate action: {len(file_metrics.problematic_files)}
- Largest file: {file_metrics.largest_file.relative_path} ({file_metrics.largest_file.line_count} lines)
- Architecture health: {'CONCERNING' if len(file_metrics.problematic_files) > file_metrics.total_files * 0.2 else 'GOOD'}
"""
        
        prompt = f"""You are a senior software architect conducting a comprehensive project review.

PROJECT CONTEXT:
{project_context}{file_size_context}

Please provide a thorough architectural analysis covering:

1. **Overall Architecture**: Is the project well-structured and maintainable?
2. **File Organization**: Are files appropriately sized and organized?
3. **Dependency Health**: Are there concerning dependency patterns or cycles?
4. **Scalability Assessment**: Can this codebase handle growth effectively?
5. **Technical Debt**: What are the main areas of concern?
6. **Refactoring Priorities**: Which files/areas need immediate attention?
7. **Best Practices**: How well does the project follow industry standards?

Provide specific, actionable recommendations with priority levels.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior software architect with expertise in code quality and maintainability."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=3000
            )
            
            ai_analysis = response.choices[0].message.content
            
            # Combine AI analysis with detailed file size analysis
            if file_metrics:
                file_size_summary = format_file_size_summary(file_metrics)
                return f"{ai_analysis}\n\n---\n\n{file_size_summary}"
            
            return ai_analysis
            
        except Exception as e:
            return f"AI analysis failed: {str(e)}"
    
    def _prepare_module_context(self, file_paths: List[str], context: Dict, dependencies: Dict) -> str:
        """Prepare context summary for module analysis"""
        context_lines = []
        
        # Basic file info
        context_lines.append(f"MODULE FILES ({len(file_paths)}):")
        for file_path in file_paths:
            context_lines.append(f"- {os.path.basename(file_path)}")
        
        # Framework detection
        if context.get('framework'):
            context_lines.append(f"\nFRAMEWORK: {context['framework']}")
        
        # Dependency summary
        if dependencies.get('missing_imports'):
            context_lines.append(f"\nMISSING IMPORTS DETECTED:")
            for missing in dependencies['missing_imports'][:5]:  # Top 5
                context_lines.append(f"- {missing}")
        
        # Cross-file relationships
        if dependencies.get('cross_file_refs'):
            context_lines.append(f"\nCROSS-FILE REFERENCES: {len(dependencies['cross_file_refs'])}")
        
        return "\n".join(context_lines)
    
    def _prepare_project_context(self, project_path: str, context: Dict, dependencies: Dict) -> str:
        """Prepare context summary for project analysis"""
        context_lines = []
        
        # Basic project info
        project_name = os.path.basename(project_path)
        context_lines.append(f"PROJECT: {project_name}")
        
        # Framework and tech stack
        if context.get('framework'):
            context_lines.append(f"FRAMEWORK: {context['framework']}")
        if context.get('database'):
            context_lines.append(f"DATABASE: {context['database']}")
        
        # Architecture overview
        if context.get('file_structure'):
            context_lines.append(f"MAJOR COMPONENTS: {', '.join(context['file_structure'].keys())}")
        
        # Dependency health
        if dependencies.get('circular_deps'):
            context_lines.append(f"CIRCULAR DEPENDENCIES: {len(dependencies['circular_deps'])} detected")
        
        if dependencies.get('external_deps'):
            context_lines.append(f"EXTERNAL DEPENDENCIES: {len(dependencies['external_deps'])}")
        
        return "\n".join(context_lines)
    
    def _create_context_summary(self, context: Dict, dependencies: Dict, 
                               file_metrics: Optional[ProjectMetrics]) -> Dict:
        """Create enhanced context summary with file metrics"""
        summary = {
            'framework': context.get('framework'),
            'database': context.get('database'),
            'external_deps': len(dependencies.get('external_deps', [])),
            'missing_imports': len(dependencies.get('missing_imports', [])),
            'circular_deps': len(dependencies.get('circular_deps', []))
        }
        
        # NEW: Add file size metrics to summary
        if file_metrics:
            summary.update({
                'total_files': file_metrics.total_files,
                'average_file_size': file_metrics.average_file_size,
                'largest_file': file_metrics.largest_file.relative_path if file_metrics.largest_file else None,
                'largest_file_size': file_metrics.largest_file.line_count if file_metrics.largest_file else 0,
                'files_needing_action': len(file_metrics.problematic_files),
                'files_over_optimal': file_metrics.summary_stats.get('files_over_optimal', 0),
                'architecture_health': self._assess_architecture_health(file_metrics)
            })
        
        return summary
    
    def _assess_architecture_health(self, file_metrics: ProjectMetrics) -> str:
        """Assess overall architecture health based on file metrics"""
        if file_metrics.total_files == 0:
            return "UNKNOWN"
        
        problematic_ratio = len(file_metrics.problematic_files) / file_metrics.total_files
        
        if problematic_ratio > 0.3:
            return "POOR"
        elif problematic_ratio > 0.15:
            return "CONCERNING" 
        elif problematic_ratio > 0.05:
            return "FAIR"
        else:
            return "EXCELLENT"
    
    def _discover_project_files(self, project_path: str) -> List[str]:
        """Discover all relevant source files in project"""
        source_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
            '.json', '.md', '.txt', '.yml', '.yaml'
        }
        
        skip_dirs = {
            'node_modules', 'venv', 'env', '.git', '__pycache__',
            '.pytest_cache', 'dist', 'build', '.vscode', '.idea'
        }
        
        files = []
        for root, dirs, filenames in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if Path(file_path).suffix.lower() in source_extensions:
                    files.append(file_path)
        
        return files
    
    def get_analysis_capabilities(self) -> Dict[str, any]:
        """Get enhanced analysis capabilities including file metrics"""
        base_capabilities = {
            'ai_available': self.client is not None,
            'supported_scopes': ['single', 'module', 'project'],
            'max_files_per_analysis': 50,  # Reasonable limit
            'context_aware': True,
            'dependency_mapping': True
        }
        
        # NEW: File analysis capabilities
        base_capabilities.update({
            'file_size_analysis': self.include_file_analysis,
            'file_size_presets': list(FileSizeThresholds.PRESETS.keys()),
            'current_preset': self._get_current_preset(),
            'refactoring_suggestions': True,
            'architecture_assessment': True
        })
        
        return base_capabilities
    
    def _get_current_preset(self) -> str:
        """Get current file size preset name"""
        current_thresholds = self.file_thresholds.thresholds
        
        for preset_name, preset_thresholds in FileSizeThresholds.PRESETS.items():
            if preset_thresholds == current_thresholds:
                return preset_name
        
        return "custom"
    
    def update_file_size_settings(self, preset: str = None, custom_thresholds: Dict = None):
        """
        Update file size analysis settings
        
        Args:
            preset: New preset name
            custom_thresholds: Custom threshold values
        """
        if custom_thresholds:
            self.file_thresholds = FileSizeThresholds(custom_thresholds=custom_thresholds)
        elif preset:
            self.file_thresholds = FileSizeThresholds(preset=preset)
        
        # Update the analyzer with new thresholds
        self.file_analyzer = FileMetricsAnalyzer(self.file_thresholds)
    
    def generate_enhanced_report_section(self, result: AnalysisResult) -> str:
        """
        Generate enhanced report section with file size analysis
        
        Args:
            result: AnalysisResult containing file metrics
            
        Returns:
            Markdown formatted report section
        """
        if not result.file_metrics:
            return ""
        
        return generate_file_size_report_section(result.file_metrics)