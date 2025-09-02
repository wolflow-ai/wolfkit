# code_context_analyzer.py (FIXED) test
"""
Code Context Analyzer for Wolfkit Code Review Enhancement
Builds comprehensive project context for multi-file analysis
"""
import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

from dependency_mapper import DependencyMapper, FileAnalysis, ImportInfo, ExportInfo


@dataclass
class ProjectContext:
    """
    Comprehensive context about a project or module for AI analysis
    """
    project_path: str
    analysis_scope: str  # 'single', 'module', 'project'
    target_files: List[str] = field(default_factory=list)
    all_files: List[str] = field(default_factory=list)
    
    # File analysis results
    file_analyses: Dict[str, FileAnalysis] = field(default_factory=dict)
    
    # Dependency information
    dependency_graph: Dict[str, Set[str]] = field(default_factory=dict)
    global_symbols: Dict[str, List[str]] = field(default_factory=dict)
    missing_imports: Dict[str, List[Dict]] = field(default_factory=dict)
    
    # Project structure
    project_structure: Dict[str, Any] = field(default_factory=dict)
    external_dependencies: Set[str] = field(default_factory=set)
    internal_dependencies: Set[str] = field(default_factory=set)
    
    # Framework detection
    detected_framework: Optional[str] = None
    framework_files: List[str] = field(default_factory=list)


class CodeContextAnalyzer:
    """
    Analyzes project structure and builds comprehensive context for AI analysis
    """
    
    def __init__(self):
        self.dependency_mapper = DependencyMapper()
        
        # File extensions to analyze
        self.source_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
            '.json', '.md', '.txt', '.yml', '.yaml'
        }
        
        # Directories to skip
        self.skip_dirs = {
            'node_modules', 'venv', 'env', '.git', '__pycache__',
            '.pytest_cache', 'dist', 'build', '.vscode', '.idea',
            'coverage', '.coverage', 'htmlcov', '.tox', 'migrations'
        }
        
        # Framework detection patterns
        self.framework_patterns = {
            'fastapi': ['fastapi', 'FastAPI', '@app.get', '@app.post'],
            'flask': ['flask', 'Flask', '@app.route', 'request.'],
            'django': ['django', 'Django', 'models.Model', 'HttpResponse'],
            'react': ['react', 'React', 'useState', 'useEffect', 'jsx'],
            'vue': ['vue', 'Vue', 'createApp', 'ref', 'reactive'],
            'express': ['express', 'app.get', 'app.post', 'req.', 'res.'],
            'nextjs': ['next', 'Next', 'getServerSideProps', 'getStaticProps']
        }
    
    def analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze entire project structure for comprehensive context
        Returns dictionary format expected by MultiFileAnalyzer
        
        Args:
            project_path: Path to the project root
            
        Returns:
            Dictionary with complete project analysis (not ProjectContext object)
        """
        # Get the full ProjectContext
        context = self._analyze_project_structure_full(project_path)
        
        # Convert to dictionary format expected by MultiFileAnalyzer
        return {
            'framework': context.detected_framework,
            'database': getattr(context, 'database_type', None),
            'framework_files': context.framework_files,
            'project_structure': context.project_structure,
            'file_structure': context.project_structure,  # Alias
            'dependency_graph': context.dependency_graph,
            'global_symbols': context.global_symbols,
            'missing_imports': context.missing_imports,
            'external_dependencies': list(context.external_dependencies),
            'internal_dependencies': list(context.internal_dependencies),
            'total_files': len(context.all_files),
            'target_files': len(context.target_files)
        }
    
    def _analyze_project_structure_full(self, project_path: str) -> ProjectContext:
        """
        Internal method that returns full ProjectContext object
        """
        project_path = Path(project_path).resolve()
        
        # Scan all source files
        all_files = self._scan_source_files(project_path)
        
        # Build context
        context = ProjectContext(
            project_path=str(project_path),
            analysis_scope='project',
            target_files=all_files,
            all_files=all_files
        )
        
        # Analyze all files
        context.file_analyses = self._analyze_all_files(all_files)
        
        # Build dependency information
        dependency_info = self.dependency_mapper.resolve_cross_file_references(all_files)
        context.dependency_graph = dependency_info['dependency_graph']
        context.global_symbols = dependency_info['global_symbols']
        context.missing_imports = dependency_info['missing_imports']
        
        # Analyze project structure
        context.project_structure = self._build_project_structure(project_path, all_files)
        
        # Get dependency summary
        import_summary = self.dependency_mapper.get_import_summary(all_files)
        context.external_dependencies = set(import_summary['external_dependencies'])
        context.internal_dependencies = set(import_summary['internal_dependencies'])
        
        # Detect framework
        context.detected_framework = self._detect_framework(all_files, context.file_analyses)
        context.framework_files = self._find_framework_files(all_files, context.detected_framework)
        
        return context
    
    def build_context_for_files(self, file_paths: List[str]) -> ProjectContext:
        """
        Build context for a specific set of files (module analysis)
        
        Args:
            file_paths: List of files to analyze as a module
            
        Returns:
            ProjectContext focused on the specified files
        """
        if not file_paths:
            raise ValueError("No files provided for analysis")
        
        # Determine project root (common parent directory)
        project_path = Path(os.path.commonpath(file_paths)).resolve()
        if project_path.is_file():
            project_path = project_path.parent
        
        # Scan broader context (nearby files)
        all_files = self._scan_source_files(project_path)
        
        # Build context
        context = ProjectContext(
            project_path=str(project_path),
            analysis_scope='module',
            target_files=file_paths,
            all_files=all_files
        )
        
        # Analyze all files (for context) but focus on target files
        context.file_analyses = self._analyze_all_files(all_files)
        
        # Build dependency information
        dependency_info = self.dependency_mapper.resolve_cross_file_references(all_files)
        context.dependency_graph = dependency_info['dependency_graph']
        context.global_symbols = dependency_info['global_symbols']
        context.missing_imports = dependency_info['missing_imports']
        
        # Focus on target files for structure analysis
        context.project_structure = self._build_focused_structure(file_paths, all_files)
        
        # Get dependency summary for target files
        import_summary = self.dependency_mapper.get_import_summary(file_paths)
        context.external_dependencies = set(import_summary['external_dependencies'])
        context.internal_dependencies = set(import_summary['internal_dependencies'])
        
        # Detect framework
        context.detected_framework = self._detect_framework(file_paths, context.file_analyses)
        context.framework_files = self._find_framework_files(file_paths, context.detected_framework)
        
        return context
    
    def analyze_file_relationships(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Analyze relationships between files (expected by MultiFileAnalyzer)
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Context dictionary with file relationship information
        """
        # This is a wrapper around the existing build_context_for_files method
        context = self.build_context_for_files(file_paths)
        
        # Extract the relevant information that MultiFileAnalyzer expects
        # Convert ProjectContext object to dictionary format
        return {
            'framework': context.detected_framework,
            'database': getattr(context, 'database_type', None),  # Safe access
            'framework_files': context.framework_files,
            'project_structure': context.project_structure,
            'file_structure': context.project_structure,  # Alias for compatibility
            'file_relationships': context.dependency_graph,
            'global_symbols': context.global_symbols,
            'missing_imports': context.missing_imports,
            'external_dependencies': list(context.external_dependencies),
            'internal_dependencies': list(context.internal_dependencies)
        }
    
    def _scan_source_files(self, project_path: Path) -> List[str]:
        """Scan directory for source files"""
        source_files = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip unwanted directories
                dirs[:] = [d for d in dirs if d not in self.skip_dirs]
                
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in self.source_extensions:
                        source_files.append(str(file_path))
                        
                # Limit depth to prevent excessive scanning
                if len(source_files) > 500:  # Reasonable limit
                    break
                        
        except PermissionError:
            # Skip directories we can't access
            pass
        
        return sorted(source_files)
    
    def _analyze_all_files(self, file_paths: List[str]) -> Dict[str, FileAnalysis]:
        """Analyze all files using dependency mapper"""
        analyses = {}
        
        for file_path in file_paths:
            try:
                analyses[file_path] = self.dependency_mapper.analyze_file(file_path)
            except Exception as e:
                # Create empty analysis for problematic files
                analyses[file_path] = FileAnalysis(
                    file_path=file_path,
                    imports=[],
                    exports=[],
                    local_definitions=[],
                    dependencies=set()
                )
        
        return analyses
    
    def _build_project_structure(self, project_path: Path, all_files: List[str]) -> Dict[str, Any]:
        """Build project structure information"""
        structure = {
            'root': str(project_path),
            'total_files': len(all_files),
            'by_extension': defaultdict(int),
            'by_directory': defaultdict(int),
            'key_files': [],
            'directory_tree': {}
        }
        
        # Analyze file distribution
        for file_path in all_files:
            path = Path(file_path)
            
            # Count by extension
            ext = path.suffix.lower()
            structure['by_extension'][ext] += 1
            
            # Count by directory
            rel_dir = path.relative_to(project_path).parent
            structure['by_directory'][str(rel_dir)] += 1
            
            # Identify key files
            if path.name in ['main.py', 'app.py', 'index.js', 'index.html', 'package.json', 'requirements.txt']:
                structure['key_files'].append(str(path))
        
        # Convert defaultdicts to regular dicts
        structure['by_extension'] = dict(structure['by_extension'])
        structure['by_directory'] = dict(structure['by_directory'])
        
        return structure
    
    def _build_focused_structure(self, target_files: List[str], all_files: List[str]) -> Dict[str, Any]:
        """Build structure focused on target files"""
        structure = {
            'target_files': len(target_files),
            'total_context_files': len(all_files),
            'target_extensions': defaultdict(int),
            'related_files': []
        }
        
        # Analyze target files
        for file_path in target_files:
            path = Path(file_path)
            ext = path.suffix.lower()
            structure['target_extensions'][ext] += 1
        
        # Find related files (same directory or similar names)
        target_dirs = {Path(f).parent for f in target_files}
        for file_path in all_files:
            if file_path not in target_files:
                path = Path(file_path)
                if path.parent in target_dirs:
                    structure['related_files'].append(str(path))
        
        structure['target_extensions'] = dict(structure['target_extensions'])
        return structure
    
    def _detect_framework(self, file_paths: List[str], analyses: Dict[str, FileAnalysis]) -> Optional[str]:
        """Detect the primary framework used"""
        framework_scores = defaultdict(int)
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Check for framework patterns
                for framework, patterns in self.framework_patterns.items():
                    for pattern in patterns:
                        if pattern.lower() in content:
                            framework_scores[framework] += content.count(pattern.lower())
                
                # Also check imports
                analysis = analyses.get(file_path)
                if analysis:
                    for import_info in analysis.imports:
                        module_lower = import_info.module.lower()
                        for framework, patterns in self.framework_patterns.items():
                            if any(pattern.lower() in module_lower for pattern in patterns):
                                framework_scores[framework] += 5  # Higher weight for imports
            
            except Exception:
                continue
        
        if framework_scores:
            return max(framework_scores, key=framework_scores.get)
        
        return None
    
    def _find_framework_files(self, file_paths: List[str], framework: Optional[str]) -> List[str]:
        """Find files that are specific to the detected framework"""
        if not framework:
            return []
        
        framework_files = []
        patterns = self.framework_patterns.get(framework, [])
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file contains framework-specific code
                if any(pattern in content for pattern in patterns):
                    framework_files.append(file_path)
                    
            except Exception:
                continue
        
        return framework_files