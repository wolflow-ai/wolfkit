# multi_file_analyzer.py (Complete Fixed Version)
"""
Multi-File Analysis Coordinator for Wolfkit
Orchestrates cross-file analysis with proper dependency mapper integration
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Local imports
from code_context_analyzer import CodeContextAnalyzer
from dependency_mapper import DependencyMapper, ProjectDependencyAnalysis

# Try to import file metrics analyzer, with graceful fallback
try:
    from file_metrics_analyzer import FileMetricsAnalyzer, FileSizeThresholds, FileMetrics
    FILE_METRICS_AVAILABLE = True
except ImportError:
    FILE_METRICS_AVAILABLE = False
    # Create dummy classes for graceful fallback
    class FileMetricsAnalyzer:
        def __init__(self, *args, **kwargs): 
            pass
        def analyze_files(self, files): 
            return None
        def analyze_project(self, path): 
            return None
    
    class FileSizeThresholds:
        def __init__(self, *args, **kwargs): 
            pass
    
    class FileMetrics:
        def __init__(self): 
            self.files_by_category = {}
            self.problematic_files = []


@dataclass
class AnalysisResult:
    """Complete analysis result with all components"""
    success: bool
    target_files: List[str]
    analysis_scope: str
    analysis_content: str
    context_summary: Dict[str, Any] = field(default_factory=dict)
    dependency_analysis: Optional[ProjectDependencyAnalysis] = None
    file_metrics: Optional[Any] = None  # FileMetrics type
    error_message: str = ""


class MultiFileAnalyzer:
    """
    Coordinates multi-file analysis with dependency mapping and file size monitoring
    """
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Initialize analysis components
        self.context_analyzer = CodeContextAnalyzer()
        self.dependency_mapper = DependencyMapper()
        
        # File size analysis components (optional)
        self.file_analyzer: Optional[FileMetricsAnalyzer] = None
        self.include_file_analysis = True
        self._setup_file_analysis()
    
    def _setup_file_analysis(self):
        """Setup file size analysis with default settings"""
        if FILE_METRICS_AVAILABLE:
            try:
                thresholds = FileSizeThresholds(preset="standard")
                self.file_analyzer = FileMetricsAnalyzer(thresholds)
            except Exception:
                self.file_analyzer = None
                self.include_file_analysis = False
        else:
            self.include_file_analysis = False
    
    def update_file_size_settings(self, preset: str = None, custom_thresholds: dict = None):
        """Update file size analysis settings"""
        if not FILE_METRICS_AVAILABLE:
            return
        
        try:
            if custom_thresholds:
                thresholds = FileSizeThresholds(custom_thresholds=custom_thresholds)
            else:
                thresholds = FileSizeThresholds(preset=preset or "standard")
            
            self.file_analyzer = FileMetricsAnalyzer(thresholds)
        except Exception as e:
            print(f"Warning: Could not update file size settings: {e}")
            self.file_analyzer = None
    
    def analyze_as_module(self, file_paths: List[str]) -> AnalysisResult:
        """
        Analyze files as a cohesive module with cross-file context
        
        Args:
            file_paths: List of file paths to analyze as a module
            
        Returns:
            Complete analysis result with cross-file insights
        """
        try:
            # Build context
            context = self.context_analyzer.build_context(file_paths)
            
            # Analyze dependencies - using the correct method
            dependency_analysis = self.dependency_mapper.analyze_files(file_paths)
            
            # Analyze file sizes if enabled
            file_metrics = None
            if self.include_file_analysis and self.file_analyzer:
                try:
                    file_metrics = self.file_analyzer.analyze_files(file_paths)
                except Exception as e:
                    print(f"Warning: File size analysis failed: {e}")
            
            # Generate AI analysis
            analysis_content = self._generate_module_analysis(
                file_paths, context, dependency_analysis, file_metrics
            )
            
            # Build context summary
            context_summary = self._build_context_summary(context, dependency_analysis, file_metrics)
            
            return AnalysisResult(
                success=True,
                target_files=file_paths,
                analysis_scope="Module",
                analysis_content=analysis_content,
                context_summary=context_summary,
                dependency_analysis=dependency_analysis,
                file_metrics=file_metrics
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                target_files=file_paths,
                analysis_scope="Module",
                analysis_content="",
                error_message=f"Module analysis failed: {str(e)}"
            )
    
    def analyze_as_project(self, project_path: str) -> AnalysisResult:
        """
        Analyze entire project for architectural review
        
        Args:
            project_path: Path to the project root directory
            
        Returns:
            Complete project analysis result
        """
        try:
            # Find Python files in project
            python_files = self._find_python_files(project_path)
            
            if not python_files:
                return AnalysisResult(
                    success=False,
                    target_files=[],
                    analysis_scope="Project",
                    analysis_content="",
                    error_message="No Python files found in project directory"
                )
            
            # Build project context
            context = self.context_analyzer.build_project_context(project_path)
            
            # Analyze project dependencies - using the correct method
            dependency_analysis = self.dependency_mapper.analyze_project(project_path)
            
            # Analyze file sizes if enabled
            file_metrics = None
            if self.include_file_analysis and self.file_analyzer:
                try:
                    file_metrics = self.file_analyzer.analyze_project(project_path)
                except Exception as e:
                    print(f"Warning: File size analysis failed: {e}")
            
            # Generate AI analysis
            analysis_content = self._generate_project_analysis(
                project_path, context, dependency_analysis, file_metrics
            )
            
            # Build context summary
            context_summary = self._build_context_summary(context, dependency_analysis, file_metrics)
            context_summary['total_files'] = len(python_files)
            
            return AnalysisResult(
                success=True,
                target_files=python_files,
                analysis_scope="Project",
                analysis_content=analysis_content,
                context_summary=context_summary,
                dependency_analysis=dependency_analysis,
                file_metrics=file_metrics
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                target_files=[],
                analysis_scope="Project",
                analysis_content="",
                error_message=f"Project analysis failed: {str(e)}"
            )
    
    def _find_python_files(self, project_path: str) -> List[str]:
        """Find all Python files in project directory"""
        python_files = []
        
        for root, dirs, files in os.walk(project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in {
                'venv', 'env', '.git', '__pycache__', 'node_modules',
                '.pytest_cache', 'dist', 'build', '.vscode', '.idea'
            }]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)
        
        return python_files
    
    def _generate_module_analysis(self, file_paths: List[str], context: Dict[str, Any], 
                                dependency_analysis: ProjectDependencyAnalysis,
                                file_metrics: Optional[Any]) -> str:
        """Generate AI analysis for module scope"""
        
        # Prepare context for AI
        module_info = {
            'files': [os.path.basename(f) for f in file_paths],
            'framework': context.get('framework', 'Unknown'),
            'missing_imports': len(dependency_analysis.missing_imports),
            'external_deps': len(dependency_analysis.external_dependencies),
            'circular_deps': len(dependency_analysis.circular_dependencies)
        }
        
        # Add file size context if available
        file_size_context = ""
        if file_metrics and hasattr(file_metrics, 'problematic_files'):
            problematic_count = len(file_metrics.problematic_files)
            if problematic_count > 0:
                file_size_context = f"\n- Files needing size attention: {problematic_count}"
                module_info['files_needing_attention'] = problematic_count
        
        prompt = f"""
You are analyzing a module consisting of {len(file_paths)} related Python files for code quality and architectural issues.

Module Information:
- Files: {', '.join(module_info['files'])}
- Framework: {module_info['framework']}
- Missing imports found: {module_info['missing_imports']}
- External dependencies: {module_info['external_deps']}
- Circular dependencies: {module_info['circular_deps']}{file_size_context}

Key Issues to Address:
"""
        
        # Add missing imports details
        if dependency_analysis.missing_imports:
            prompt += "\n**Missing Imports:**\n"
            for file_path, symbol, source_file in dependency_analysis.missing_imports[:5]:
                file_name = os.path.basename(file_path)
                source_name = os.path.basename(source_file)
                prompt += f"- {file_name}: '{symbol}' available in {source_name}\n"
        
        # Add circular dependency details
        if dependency_analysis.circular_dependencies:
            prompt += "\n**Circular Dependencies:**\n"
            for cycle in dependency_analysis.circular_dependencies[:3]:
                cycle_names = [os.path.basename(f) for f in cycle]
                prompt += f"- {' → '.join(cycle_names)}\n"
        
        # Add file size issues if present
        if file_metrics and hasattr(file_metrics, 'problematic_files') and file_metrics.problematic_files:
            prompt += "\n**File Size Issues:**\n"
            for file_metric in file_metrics.problematic_files[:3]:
                file_name = os.path.basename(file_metric.file_path)
                severity = "🚨" if file_metric.size_category.value == "dangerous" else "⚠️"
                prompt += f"- {severity} {file_name}: {file_metric.line_count} lines\n"
        
        prompt += """

Please provide a concise analysis focusing on:
1. Cross-file integration issues
2. Missing imports and how to resolve them
3. Architectural improvements
4. File size and maintainability concerns
5. Framework-specific best practices

Format your response as a professional code review with clear action items.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer specializing in multi-file Python analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis failed: {str(e)}\n\nFallback architectural assessment:\n- Project has {project_info['total_files']} Python files\n- Framework: {project_info['framework']}\n- Found {len(dependency_analysis.missing_imports)} integration issues\n- External dependencies: {len(dependency_analysis.external_dependencies)}"
    
    def _build_context_summary(self, context: Dict[str, Any], 
                             dependency_analysis: ProjectDependencyAnalysis,
                             file_metrics: Optional[Any]) -> Dict[str, Any]:
        """Build comprehensive context summary for reports"""
        summary = {
            'framework': context.get('framework'),
            'external_deps': len(dependency_analysis.external_dependencies),
            'missing_imports': len(dependency_analysis.missing_imports),
            'circular_deps': len(dependency_analysis.circular_dependencies)
        }
        
        # Add file size metrics if available
        if file_metrics:
            if hasattr(file_metrics, 'problematic_files'):
                summary['files_needing_action'] = len(file_metrics.problematic_files)
            
            # Determine architecture health based on file size distribution
            if hasattr(file_metrics, 'files_by_category'):
                dangerous_count = len(file_metrics.files_by_category.get('dangerous', []))
                critical_count = len(file_metrics.files_by_category.get('critical', []))
                
                if dangerous_count > 0:
                    summary['architecture_health'] = "CRITICAL"
                elif critical_count > 0:
                    summary['architecture_health'] = "CONCERNING"
                elif summary.get('files_needing_action', 0) > 0:
                    summary['architecture_health'] = "NEEDS_ATTENTION"
                else:
                    summary['architecture_health'] = "HEALTHY"
        
        return summary
    
    def get_analysis_capabilities(self) -> Dict[str, Any]:
        """Get current analysis capabilities"""
        capabilities = {
            'ai_available': self.client is not None,
            'supported_scopes': ['module', 'project'],
            'max_files_per_analysis': 50,  # Reasonable limit for AI analysis
            'dependency_analysis': True,
            'context_analysis': True,
            'file_size_analysis': FILE_METRICS_AVAILABLE and self.include_file_analysis
        }
        
        if FILE_METRICS_AVAILABLE and self.file_analyzer:
            capabilities.update({
                'file_size_presets': ['strict', 'standard', 'relaxed', 'legacy', 'custom'],
                'current_preset': getattr(self.file_analyzer.thresholds, 'preset_name', 'unknown')
            })
        else:
            capabilities.update({
                'file_size_presets': [],
                'current_preset': 'none'
            })
        
        return capabilities analysis failed: {str(e)}\n\nFallback analysis based on dependency analysis:\n- Found {len(dependency_analysis.missing_imports)} missing imports\n- Detected {len(dependency_analysis.circular_dependencies)} circular dependencies"
    
    def _generate_project_analysis(self, project_path: str, context: Dict[str, Any],
                                 dependency_analysis: ProjectDependencyAnalysis,
                                 file_metrics: Optional[Any]) -> str:
        """Generate AI analysis for project scope"""
        
        project_name = os.path.basename(project_path)
        
        # Prepare context for AI
        project_info = {
            'name': project_name,
            'total_files': len(dependency_analysis.files),
            'framework': context.get('framework', 'Unknown'),
            'missing_imports': len(dependency_analysis.missing_imports),
            'external_deps': len(dependency_analysis.external_dependencies),
            'circular_deps': len(dependency_analysis.circular_dependencies)
        }
        
        # Add file size context if available
        file_size_summary = ""
        if file_metrics:
            total_files = len(getattr(file_metrics, 'all_files', []))
            problematic_files = len(getattr(file_metrics, 'problematic_files', []))
            if total_files > 0:
                file_size_summary = f"\n- Total files analyzed for size: {total_files}"
                if problematic_files > 0:
                    file_size_summary += f"\n- Files needing size attention: {problematic_files}"
                    project_info['files_needing_attention'] = problematic_files
        
        prompt = f"""
You are conducting an architectural review of the "{project_name}" Python project.

Project Overview:
- Total Python files: {project_info['total_files']}
- Framework: {project_info['framework']}
- Missing imports: {project_info['missing_imports']}
- External dependencies: {project_info['external_deps']}
- Circular dependencies: {project_info['circular_deps']}{file_size_summary}

Architecture Assessment:
"""
        
        # Add key external dependencies
        if dependency_analysis.external_dependencies:
            prompt += f"\n**Key Dependencies:** {', '.join(list(dependency_analysis.external_dependencies)[:10])}\n"
        
        # Add critical issues
        critical_issues = []
        if dependency_analysis.missing_imports:
            critical_issues.append(f"{len(dependency_analysis.missing_imports)} missing imports")
        if dependency_analysis.circular_dependencies:
            critical_issues.append(f"{len(dependency_analysis.circular_dependencies)} circular dependencies")
        if file_metrics and hasattr(file_metrics, 'problematic_files'):
            problematic_count = len(file_metrics.problematic_files)
            if problematic_count > 0:
                critical_issues.append(f"{problematic_count} oversized files")
        
        if critical_issues:
            prompt += f"\n**Critical Issues:** {', '.join(critical_issues)}\n"
        
        prompt += """

Please provide an executive-level architectural assessment focusing on:
1. Overall code organization and structure
2. Dependency management and potential improvements
3. Framework adherence and best practices
4. File size distribution and maintainability
5. Scalability and maintenance recommendations

Format as a professional architectural review with strategic recommendations.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert software architect specializing in Python project analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI