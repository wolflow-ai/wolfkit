# dependency_mapper.py (Complete Fixed Version)
"""
Dependency Mapper for Wolfkit - Enhanced with project-level analysis
Maps imports, exports, and dependencies across multiple files with project-wide analysis
"""
import os
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class DependencyInfo:
    """Information about a single dependency"""
    name: str
    source_file: str
    import_type: str  # 'import', 'from_import', 'function_call', 'class_instantiation'
    line_number: int
    is_local: bool = False
    is_external: bool = False
    module_path: str = ""


@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    file_path: str
    imports: List[DependencyInfo] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)  # Functions, classes, variables defined
    function_calls: List[DependencyInfo] = field(default_factory=list)
    undefined_symbols: List[str] = field(default_factory=list)
    syntax_errors: List[str] = field(default_factory=list)


@dataclass
class ProjectDependencyAnalysis:
    """Complete project dependency analysis"""
    files: Dict[str, FileAnalysis] = field(default_factory=dict)
    missing_imports: List[Tuple[str, str, str]] = field(default_factory=list)  # (file, symbol, suggested_source)
    circular_dependencies: List[List[str]] = field(default_factory=list)
    external_dependencies: Set[str] = field(default_factory=set)
    dependency_graph: Dict[str, Set[str]] = field(default_factory=dict)
    available_symbols: Dict[str, List[str]] = field(default_factory=dict)  # symbol -> [files_that_define_it]


class DependencyMapper:
    """
    Maps and analyzes dependencies across multiple Python files
    Enhanced with project-level analysis capabilities
    """
    
    def __init__(self):
        self.file_analyses: Dict[str, FileAnalysis] = {}
        self.global_symbols: Dict[str, List[str]] = defaultdict(list)  # symbol -> files that define it
        self.external_modules = {
            'os', 'sys', 'json', 'datetime', 'pathlib', 'typing', 'dataclasses',
            'tkinter', 'ttkbootstrap', 'numpy', 'pandas', 'requests', 'flask',
            'fastapi', 'django', 'sqlalchemy', 'openai', 'dotenv'
        }
    
    def analyze_files(self, file_paths: List[str]) -> ProjectDependencyAnalysis:
        """
        Analyze dependencies across multiple files
        
        Args:
            file_paths: List of Python file paths to analyze
            
        Returns:
            Complete dependency analysis with cross-file relationships
        """
        # Reset state
        self.file_analyses = {}
        self.global_symbols = defaultdict(list)
        
        # Phase 1: Analyze each file individually
        for file_path in file_paths:
            if file_path.endswith('.py'):
                analysis = self._analyze_single_file(file_path)
                if analysis:
                    self.file_analyses[file_path] = analysis
                    
                    # Build global symbol table
                    for export in analysis.exports:
                        self.global_symbols[export].append(file_path)
        
        # Phase 2: Find missing imports and circular dependencies
        missing_imports = self._find_missing_imports()
        circular_deps = self._detect_circular_dependencies()
        external_deps = self._collect_external_dependencies()
        dependency_graph = self._build_dependency_graph()
        
        return ProjectDependencyAnalysis(
            files=self.file_analyses,
            missing_imports=missing_imports,
            circular_dependencies=circular_deps,
            external_dependencies=external_deps,
            dependency_graph=dependency_graph,
            available_symbols=dict(self.global_symbols)
        )
    
    def analyze_project(self, project_path: str) -> ProjectDependencyAnalysis:
        """
        Analyze dependencies for an entire project directory
        
        Args:
            project_path: Path to the project root directory
            
        Returns:
            Complete project dependency analysis
        """
        python_files = []
        
        # Find all Python files in the project
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
        
        if not python_files:
            # Return empty analysis if no Python files found
            return ProjectDependencyAnalysis()
        
        # Analyze all found Python files
        return self.analyze_files(python_files)
    
    def _analyze_single_file(self, file_path: str) -> Optional[FileAnalysis]:
        """Analyze a single Python file for dependencies and exports"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content, filename=file_path)
            except SyntaxError as e:
                return FileAnalysis(
                    file_path=file_path,
                    syntax_errors=[f"Syntax error: {str(e)}"]
                )
            
            analysis = FileAnalysis(file_path=file_path)
            
            # Walk the AST
            for node in ast.walk(tree):
                self._process_ast_node(node, analysis, file_path)
            
            return analysis
            
        except Exception as e:
            return FileAnalysis(
                file_path=file_path,
                syntax_errors=[f"Analysis error: {str(e)}"]
            )
    
    def _process_ast_node(self, node: ast.AST, analysis: FileAnalysis, file_path: str):
        """Process a single AST node for dependency information"""
        # Import statements
        if isinstance(node, ast.Import):
            for alias in node.names:
                dep = DependencyInfo(
                    name=alias.name,
                    source_file=file_path,
                    import_type='import',
                    line_number=node.lineno,
                    is_external=alias.name.split('.')[0] in self.external_modules
                )
                analysis.imports.append(dep)
        
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ''
            for alias in node.names:
                dep = DependencyInfo(
                    name=alias.name,
                    source_file=file_path,
                    import_type='from_import',
                    line_number=node.lineno,
                    module_path=module_name,
                    is_external=module_name.split('.')[0] in self.external_modules if module_name else False
                )
                analysis.imports.append(dep)
        
        # Function and class definitions (exports)
        elif isinstance(node, ast.FunctionDef):
            analysis.exports.append(node.name)
        
        elif isinstance(node, ast.ClassDef):
            analysis.exports.append(node.name)
        
        # Variable assignments (potential exports)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Only consider module-level assignments as exports
                    if hasattr(node, 'col_offset') and node.col_offset == 0:
                        analysis.exports.append(target.id)
        
        # Function calls (potential missing dependencies)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                dep = DependencyInfo(
                    name=node.func.id,
                    source_file=file_path,
                    import_type='function_call',
                    line_number=node.lineno
                )
                analysis.function_calls.append(dep)
        
        # Name references (potential undefined symbols)
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):  # Variable being read
                # We'll check if this is undefined in the missing imports phase
                pass
    
    def _find_missing_imports(self) -> List[Tuple[str, str, str]]:
        """Find symbols that are used but not imported, but available in other files"""
        missing_imports = []
        
        for file_path, analysis in self.file_analyses.items():
            # Get all imported symbols for this file
            imported_symbols = set()
            for imp in analysis.imports:
                imported_symbols.add(imp.name)
            
            # Get all locally defined symbols
            local_symbols = set(analysis.exports)
            
            # Check function calls for missing imports
            for call in analysis.function_calls:
                symbol = call.name
                
                # Skip if already imported or defined locally
                if symbol in imported_symbols or symbol in local_symbols:
                    continue
                
                # Skip built-in functions
                if symbol in {'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip', 'open', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr'}:
                    continue
                
                # Check if available in other files
                if symbol in self.global_symbols:
                    for source_file in self.global_symbols[symbol]:
                        if source_file != file_path:
                            missing_imports.append((file_path, symbol, source_file))
                            break
        
        return missing_imports
    
    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies between files"""
        # Build import graph
        import_graph = defaultdict(set)
        
        for file_path, analysis in self.file_analyses.items():
            for imp in analysis.imports:
                if not imp.is_external and imp.module_path:
                    # Try to resolve module path to actual file
                    target_file = self._resolve_module_to_file(imp.module_path, file_path)
                    if target_file and target_file in self.file_analyses:
                        import_graph[file_path].add(target_file)
        
        # Find cycles using DFS
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in import_graph[node]:
                dfs(neighbor, path.copy())
            
            rec_stack.remove(node)
        
        for file_path in self.file_analyses:
            if file_path not in visited:
                dfs(file_path, [])
        
        return cycles
    
    def _resolve_module_to_file(self, module_path: str, current_file: str) -> Optional[str]:
        """Resolve a module import path to an actual file path"""
        # This is a simplified resolution - could be enhanced
        current_dir = os.path.dirname(current_file)
        
        # Handle relative imports
        if module_path.startswith('.'):
            # Relative import
            parts = module_path.lstrip('.').split('.')
            target_path = os.path.join(current_dir, *parts) + '.py'
            if os.path.exists(target_path):
                return target_path
        else:
            # Absolute import within project
            parts = module_path.split('.')
            target_path = os.path.join(current_dir, *parts) + '.py'
            if os.path.exists(target_path):
                return target_path
        
        return None
    
    def _collect_external_dependencies(self) -> Set[str]:
        """Collect all external dependencies from analyzed files"""
        external_deps = set()
        
        for analysis in self.file_analyses.values():
            for imp in analysis.imports:
                if imp.is_external:
                    # Get the top-level module name
                    top_level = imp.module_path.split('.')[0] if imp.module_path else imp.name.split('.')[0]
                    external_deps.add(top_level)
        
        return external_deps
    
    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build a dependency graph showing file relationships"""
        graph = defaultdict(set)
        
        for file_path, analysis in self.file_analyses.items():
            for imp in analysis.imports:
                if not imp.is_external and imp.module_path:
                    target_file = self._resolve_module_to_file(imp.module_path, file_path)
                    if target_file:
                        graph[file_path].add(target_file)
        
        return dict(graph)
    
    def get_dependency_summary(self) -> Dict[str, Any]:
        """Get a summary of dependency analysis results"""
        if not self.file_analyses:
            return {}
        
        total_imports = sum(len(analysis.imports) for analysis in self.file_analyses.values())
        total_exports = sum(len(analysis.exports) for analysis in self.file_analyses.values())
        files_with_errors = len([a for a in self.file_analyses.values() if a.syntax_errors])
        
        return {
            'total_files': len(self.file_analyses),
            'total_imports': total_imports,
            'total_exports': total_exports,
            'files_with_errors': files_with_errors,
            'external_dependencies': len(self._collect_external_dependencies()),
            'available_symbols': len(self.global_symbols)
        }


def analyze_file_dependencies(file_paths: List[str]) -> ProjectDependencyAnalysis:
    """Convenience function for analyzing file dependencies"""
    mapper = DependencyMapper()
    return mapper.analyze_files(file_paths)


def analyze_project_dependencies(project_path: str) -> ProjectDependencyAnalysis:
    """Convenience function for analyzing project dependencies"""
    mapper = DependencyMapper()
    return mapper.analyze_project(project_path)