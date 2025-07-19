# dependency_mapper.py
"""
Dependency Mapper for Wolfkit Code Review Enhancement
Analyzes import/export patterns and builds dependency graphs across files
"""
import re
import ast
import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ImportInfo:
    """Information about an import statement"""
    module: str
    names: List[str]
    alias: Optional[str] = None
    is_from_import: bool = False
    line_number: int = 0


@dataclass
class ExportInfo:
    """Information about exported functions/classes"""
    name: str
    type: str  # 'function', 'class', 'variable'
    line_number: int
    signature: Optional[str] = None


@dataclass
class FileAnalysis:
    """Complete analysis of a single file"""
    file_path: str
    imports: List[ImportInfo]
    exports: List[ExportInfo]
    local_definitions: List[str]
    dependencies: Set[str]


class DependencyMapper:
    """
    Analyzes import/export patterns and builds dependency graphs
    """
    
    def __init__(self):
        self.python_stdlib = self._load_python_stdlib()
        self.file_analyses: Dict[str, FileAnalysis] = {}
    
    def _load_python_stdlib(self) -> Set[str]:
        """Load common Python standard library modules"""
        # Common stdlib modules - in a real implementation, this could be more comprehensive
        return {
            'os', 'sys', 'json', 'datetime', 'pathlib', 'typing', 'collections',
            'itertools', 'functools', 'operator', 'math', 'random', 'string',
            'urllib', 'http', 'sqlite3', 'logging', 'argparse', 'configparser',
            'csv', 'xml', 'html', 'base64', 'hashlib', 'hmac', 'secrets',
            'threading', 'multiprocessing', 'asyncio', 'concurrent', 'queue',
            'socket', 'ssl', 'email', 'unittest', 'doctest', 'pdb', 'profile',
            'time', 'calendar', 'locale', 'gettext', 'pickle', 'shelve',
            'dbm', 'sqlite3', 'zlib', 'gzip', 'bz2', 'lzma', 'zipfile',
            'tarfile', 'tempfile', 'shutil', 'glob', 'fnmatch', 'linecache',
            'fileinput', 'stat', 'filecmp', 'subprocess', 'signal', 'platform'
        }
    
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """
        Analyze a single file for imports and exports
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            FileAnalysis object with import/export information
        """
        if file_path in self.file_analyses:
            return self.file_analyses[file_path]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            # Return empty analysis if file can't be read
            return FileAnalysis(
                file_path=file_path,
                imports=[],
                exports=[],
                local_definitions=[],
                dependencies=set()
            )
        
        # Determine file type and analyze accordingly
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.py':
            analysis = self._analyze_python_file(file_path, content)
        elif file_ext in ['.js', '.ts', '.jsx', '.tsx']:
            analysis = self._analyze_javascript_file(file_path, content)
        else:
            # Default to simple text analysis
            analysis = self._analyze_generic_file(file_path, content)
        
        self.file_analyses[file_path] = analysis
        return analysis
    
    def _analyze_python_file(self, file_path: str, content: str) -> FileAnalysis:
        """Analyze Python file using AST parsing"""
        imports = []
        exports = []
        local_definitions = []
        dependencies = set()
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_info = ImportInfo(
                            module=alias.name,
                            names=[alias.name],
                            alias=alias.asname,
                            is_from_import=False,
                            line_number=node.lineno
                        )
                        imports.append(import_info)
                        
                        # Add to dependencies if not stdlib
                        if not self._is_stdlib_module(alias.name):
                            dependencies.add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        names = [alias.name for alias in node.names]
                        import_info = ImportInfo(
                            module=node.module,
                            names=names,
                            is_from_import=True,
                            line_number=node.lineno
                        )
                        imports.append(import_info)
                        
                        # Add to dependencies if not stdlib
                        if not self._is_stdlib_module(node.module):
                            dependencies.add(node.module)
                
                elif isinstance(node, ast.FunctionDef):
                    signature = self._get_function_signature(node)
                    export_info = ExportInfo(
                        name=node.name,
                        type='function',
                        line_number=node.lineno,
                        signature=signature
                    )
                    exports.append(export_info)
                    local_definitions.append(node.name)
                
                elif isinstance(node, ast.ClassDef):
                    export_info = ExportInfo(
                        name=node.name,
                        type='class',
                        line_number=node.lineno
                    )
                    exports.append(export_info)
                    local_definitions.append(node.name)
                
                elif isinstance(node, ast.Assign):
                    # Handle variable assignments at module level
                    if isinstance(node.targets[0], ast.Name):
                        var_name = node.targets[0].id
                        export_info = ExportInfo(
                            name=var_name,
                            type='variable',
                            line_number=node.lineno
                        )
                        exports.append(export_info)
                        local_definitions.append(var_name)
        
        except SyntaxError:
            # Fallback to regex-based analysis if AST parsing fails
            return self._analyze_python_file_regex(file_path, content)
        
        return FileAnalysis(
            file_path=file_path,
            imports=imports,
            exports=exports,
            local_definitions=local_definitions,
            dependencies=dependencies
        )
    
    def _analyze_python_file_regex(self, file_path: str, content: str) -> FileAnalysis:
        """Fallback regex-based Python analysis"""
        imports = []
        exports = []
        local_definitions = []
        dependencies = set()
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Import statements
            import_match = re.match(r'import\s+(\w+(?:\.\w+)*)', line)
            if import_match:
                module = import_match.group(1)
                imports.append(ImportInfo(
                    module=module,
                    names=[module],
                    line_number=i
                ))
                if not self._is_stdlib_module(module):
                    dependencies.add(module)
            
            # From imports
            from_import_match = re.match(r'from\s+(\w+(?:\.\w+)*)\s+import\s+(.+)', line)
            if from_import_match:
                module = from_import_match.group(1)
                names = [name.strip() for name in from_import_match.group(2).split(',')]
                imports.append(ImportInfo(
                    module=module,
                    names=names,
                    is_from_import=True,
                    line_number=i
                ))
                if not self._is_stdlib_module(module):
                    dependencies.add(module)
            
            # Function definitions
            func_match = re.match(r'def\s+(\w+)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                exports.append(ExportInfo(
                    name=func_name,
                    type='function',
                    line_number=i
                ))
                local_definitions.append(func_name)
            
            # Class definitions
            class_match = re.match(r'class\s+(\w+)', line)
            if class_match:
                class_name = class_match.group(1)
                exports.append(ExportInfo(
                    name=class_name,
                    type='class',
                    line_number=i
                ))
                local_definitions.append(class_name)
        
        return FileAnalysis(
            file_path=file_path,
            imports=imports,
            exports=exports,
            local_definitions=local_definitions,
            dependencies=dependencies
        )
    
    def _analyze_javascript_file(self, file_path: str, content: str) -> FileAnalysis:
        """Analyze JavaScript/TypeScript file using regex patterns"""
        imports = []
        exports = []
        local_definitions = []
        dependencies = set()
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # ES6 import statements
            import_match = re.match(r'import\s+.*from\s+[\'"]([^\'"]+)[\'"]', line)
            if import_match:
                module = import_match.group(1)
                imports.append(ImportInfo(
                    module=module,
                    names=[module],
                    line_number=i
                ))
                if not module.startswith('./') and not module.startswith('../'):
                    dependencies.add(module)
            
            # Function declarations
            func_match = re.match(r'function\s+(\w+)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                exports.append(ExportInfo(
                    name=func_name,
                    type='function',
                    line_number=i
                ))
                local_definitions.append(func_name)
            
            # Class declarations
            class_match = re.match(r'class\s+(\w+)', line)
            if class_match:
                class_name = class_match.group(1)
                exports.append(ExportInfo(
                    name=class_name,
                    type='class',
                    line_number=i
                ))
                local_definitions.append(class_name)
        
        return FileAnalysis(
            file_path=file_path,
            imports=imports,
            exports=exports,
            local_definitions=local_definitions,
            dependencies=dependencies
        )
    
    def _analyze_generic_file(self, file_path: str, content: str) -> FileAnalysis:
        """Generic file analysis for unsupported file types"""
        return FileAnalysis(
            file_path=file_path,
            imports=[],
            exports=[],
            local_definitions=[],
            dependencies=set()
        )
    
    def _is_stdlib_module(self, module_name: str) -> bool:
        """Check if a module is part of Python standard library"""
        base_module = module_name.split('.')[0]
        return base_module in self.python_stdlib
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature from AST node"""
        args = []
        
        # Regular arguments
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Add defaults if any
        if node.args.defaults:
            defaults_start = len(args) - len(node.args.defaults)
            for i, default in enumerate(node.args.defaults):
                args[defaults_start + i] += "=..."
        
        return f"{node.name}({', '.join(args)})"
    
    def build_dependency_graph(self, file_paths: List[str]) -> Dict[str, Set[str]]:
        """
        Build a dependency graph showing file relationships
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dict mapping file paths to their dependencies
        """
        graph = defaultdict(set)
        
        # Analyze all files first
        analyses = {}
        for file_path in file_paths:
            analyses[file_path] = self.analyze_file(file_path)
        
        # Build relationships
        for file_path, analysis in analyses.items():
            for import_info in analysis.imports:
                # Check if this import refers to another file in our set
                for other_file in file_paths:
                    if other_file != file_path:
                        other_analysis = analyses[other_file]
                        
                        # Check if the import matches exports from other file
                        if self._import_matches_file(import_info, other_analysis):
                            graph[file_path].add(other_file)
        
        return dict(graph)
    
    def _import_matches_file(self, import_info: ImportInfo, file_analysis: FileAnalysis) -> bool:
        """Check if an import statement matches exports from a file"""
        # Simple heuristic: check if module name matches file name or exports
        file_name = Path(file_analysis.file_path).stem
        
        # Check if importing by filename
        if import_info.module == file_name:
            return True
        
        # Check if any imported names match exports
        for name in import_info.names:
            if name in file_analysis.local_definitions:
                return True
        
        return False
    
    def resolve_cross_file_references(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Resolve cross-file references and missing imports
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dict containing resolution information
        """
        analyses = {fp: self.analyze_file(fp) for fp in file_paths}
        
        # Build a global symbol table
        global_symbols = {}
        for file_path, analysis in analyses.items():
            for definition in analysis.local_definitions:
                if definition not in global_symbols:
                    global_symbols[definition] = []
                global_symbols[definition].append(file_path)
        
        # Find missing imports
        missing_imports = {}
        for file_path, analysis in analyses.items():
            missing = []
            
            # Simple heuristic: look for undefined names in code
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find potential undefined references
            words = re.findall(r'\b[a-zA-Z_]\w*\b', content)
            for word in set(words):
                if (word not in analysis.local_definitions and 
                    word not in [imp.module for imp in analysis.imports] and
                    word not in ['if', 'else', 'for', 'while', 'def', 'class', 'return', 'import', 'from'] and
                    word in global_symbols):
                    
                    # This might be a missing import
                    potential_sources = global_symbols[word]
                    if file_path not in potential_sources:
                        missing.append({
                            'symbol': word,
                            'available_in': potential_sources
                        })
            
            if missing:
                missing_imports[file_path] = missing
        
        return {
            'global_symbols': global_symbols,
            'missing_imports': missing_imports,
            'dependency_graph': self.build_dependency_graph(file_paths)
        }
    
    def get_import_summary(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Get a summary of imports across all files
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Summary of import information
        """
        all_imports = []
        external_deps = set()
        internal_deps = set()
        
        for file_path in file_paths:
            analysis = self.analyze_file(file_path)
            all_imports.extend(analysis.imports)
            external_deps.update(analysis.dependencies)
        
        # Classify dependencies
        file_names = {Path(fp).stem for fp in file_paths}
        for dep in list(external_deps):
            if dep in file_names:
                internal_deps.add(dep)
                external_deps.remove(dep)
        
        return {
            'total_imports': len(all_imports),
            'external_dependencies': sorted(external_deps),
            'internal_dependencies': sorted(internal_deps),
            'import_details': [
                {
                    'file': imp.module,
                    'names': imp.names,
                    'is_from_import': imp.is_from_import
                }
                for imp in all_imports
            ]
        }
