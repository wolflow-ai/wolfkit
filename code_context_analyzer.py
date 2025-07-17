# code_context_analyzer.py
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
    
    def analyze_project_structure(self, project_path: str) -> ProjectContext:
        """
        Analyze entire project structure for comprehensive context
        
        Args:
            project_path: Path to the project root
            
        Returns:
            ProjectContext with complete project analysis
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
    
    def generate_context_prompt(self, context: ProjectContext) -> str:
        """
        Generate a comprehensive context prompt for AI analysis
        
        Args:
            context: ProjectContext object with analysis results
            
        Returns:
            Formatted prompt string with project context
        """
        prompt_parts = []
        
        # Header
        prompt_parts.append("=== PROJECT CONTEXT ===")
        prompt_parts.append(f"Analysis Scope: {context.analysis_scope}")
        prompt_parts.append(f"Project Path: {context.project_path}")
        
        # Framework information
        if context.detected_framework:
            prompt_parts.append(f"Framework: {context.detected_framework}")
            if context.framework_files:
                prompt_parts.append(f"Framework Files: {len(context.framework_files)}")
        
        # File structure
        prompt_parts.append(f"\nFILE STRUCTURE:")
        prompt_parts.append(f"Target Files: {len(context.target_files)}")
        prompt_parts.append(f"Total Context Files: {len(context.all_files)}")
        
        # Dependencies
        if context.external_dependencies:
            prompt_parts.append(f"\nEXTERNAL DEPENDENCIES:")
            for dep in sorted(context.external_dependencies):
                prompt_parts.append(f"- {dep}")
        
        if context.internal_dependencies:
            prompt_parts.append(f"\nINTERNAL DEPENDENCIES:")
            for dep in sorted(context.internal_dependencies):
                prompt_parts.append(f"- {dep}")
        
        # Missing imports (key insight for AI)
        if context.missing_imports:
            prompt_parts.append(f"\nPOTENTIAL MISSING IMPORTS:")
            for file_path, missing_list in context.missing_imports.items():
                rel_path = Path(file_path).relative_to(context.project_path)
                prompt_parts.append(f"In {rel_path}:")
                for missing in missing_list:
                    symbol = missing['symbol']
                    sources = missing['available_in']
                    source_names = [Path(s).name for s in sources]
                    prompt_parts.append(f"  - '{symbol}' available in: {', '.join(source_names)}")
        
        # Cross-file relationships
        if context.dependency_graph:
            prompt_parts.append(f"\nFILE RELATIONSHIPS:")
            for file_path, dependencies in context.dependency_graph.items():
                if dependencies:
                    rel_path = Path(file_path).relative_to(context.project_path)
                    dep_names = [Path(d).name for d in dependencies]
                    prompt_parts.append(f"{rel_path.name} depends on: {', '.join(dep_names)}")
        
        # Global symbols (functions/classes available across files)
        if context.global_symbols:
            prompt_parts.append(f"\nGLOBAL SYMBOLS:")
            for symbol, files in context.global_symbols.items():
                if len(files) > 1:  # Only show symbols in multiple files
                    file_names = [Path(f).name for f in files]
                    prompt_parts.append(f"'{symbol}' defined in: {', '.join(file_names)}")
        
        # Target file details
        prompt_parts.append(f"\nTARGET FILES ANALYSIS:")
        for file_path in context.target_files:
            rel_path = Path(file_path).relative_to(context.project_path)
            analysis = context.file_analyses.get(file_path)
            
            if analysis:
                prompt_parts.append(f"\n{rel_path}:")
                
                # Imports
                if analysis.imports:
                    prompt_parts.append(f"  Imports: {len(analysis.imports)}")
                    for imp in analysis.imports[:5]:  # Show first 5
                        if imp.is_from_import:
                            prompt_parts.append(f"    from {imp.module} import {', '.join(imp.names)}")
                        else:
                            prompt_parts.append(f"    import {imp.module}")
                    if len(analysis.imports) > 5:
                        prompt_parts.append(f"    ... and {len(analysis.imports) - 5} more")
                
                # Exports
                if analysis.exports:
                    prompt_parts.append(f"  Exports: {len(analysis.exports)}")
                    for exp in analysis.exports[:5]:  # Show first 5
                        if exp.type == 'function' and exp.signature:
                            prompt_parts.append(f"    {exp.signature}")
                        else:
                            prompt_parts.append(f"    {exp.type}: {exp.name}")
                    if len(analysis.exports) > 5:
                        prompt_parts.append(f"    ... and {len(analysis.exports) - 5} more")
        
        prompt_parts.append("\n=== END CONTEXT ===\n")
        
        return "\n".join(prompt_parts)
    
    def get_context_summary(self, context: ProjectContext) -> Dict[str, Any]:
        """
        Get a summary of the project context for UI display
        
        Args:
            context: ProjectContext object
            
        Returns:
            Summary dict with key metrics
        """
        return {
            'scope': context.analysis_scope,
            'framework': context.detected_framework,
            'target_files': len(context.target_files),
            'total_files': len(context.all_files),
            'external_deps': len(context.external_dependencies),
            'internal_deps': len(context.internal_dependencies),
            'missing_imports': sum(len(missing) for missing in context.missing_imports.values()),
            'cross_file_deps': sum(len(deps) for deps in context.dependency_graph.values()),
            'global_symbols': len(context.global_symbols)
        }
    
    def find_related_files(self, context: ProjectContext, target_file: str) -> List[str]:
        """
        Find files related to a target file based on imports and dependencies
        
        Args:
            context: ProjectContext object
            target_file: File to find relations for
            
        Returns:
            List of related file paths
        """
        related = set()
        
        # Files that import from target file
        for file_path, deps in context.dependency_graph.items():
            if target_file in deps:
                related.add(file_path)
        
        # Files that target file imports from
        if target_file in context.dependency_graph:
            related.update(context.dependency_graph[target_file])
        
        # Files in same directory
        target_dir = Path(target_file).parent
        for file_path in context.all_files:
            if Path(file_path).parent == target_dir and file_path != target_file:
                related.add(file_path)
        
        return sorted(related)
    
    def validate_context(self, context: ProjectContext) -> Dict[str, Any]:
        """
        Validate the completeness and accuracy of the context
        
        Args:
            context: ProjectContext to validate
            
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Check for empty target files
        if not context.target_files:
            issues.append("No target files specified")
        
        # Check for missing file analyses
        for file_path in context.target_files:
            if file_path not in context.file_analyses:
                issues.append(f"Missing analysis for {file_path}")
        
        # Check for potential circular dependencies
        for file_path, deps in context.dependency_graph.items():
            for dep in deps:
                if dep in context.dependency_graph and file_path in context.dependency_graph[dep]:
                    warnings.append(f"Circular dependency: {Path(file_path).name} ↔ {Path(dep).name}")
        
        # Check for orphaned files (no imports/exports)
        for file_path in context.target_files:
            analysis = context.file_analyses.get(file_path)
            if analysis and not analysis.imports and not analysis.exports:
                warnings.append(f"Orphaned file (no imports/exports): {Path(file_path).name}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'stats': self.get_context_summary(context)
        }