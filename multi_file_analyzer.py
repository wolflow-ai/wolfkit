# multi_file_analyzer.py
"""
Multi-File Analyzer for Wolfkit Code Review Enhancement
Coordinates analysis of multiple files with comprehensive context awareness
"""
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from code_context_analyzer import CodeContextAnalyzer, ProjectContext
from dependency_mapper import DependencyMapper


@dataclass
class AnalysisResult:
    """Result of multi-file analysis"""
    success: bool
    analysis_content: str
    context_summary: Dict[str, Any]
    analysis_scope: str
    target_files: List[str]
    error_message: str = ""


class MultiFileAnalyzer:
    """
    Coordinates multi-file analysis with comprehensive context awareness
    """
    
    def __init__(self, openai_client=None):
        """
        Initialize the multi-file analyzer
        
        Args:
            openai_client: OpenAI client for AI analysis
        """
        self.client = openai_client
        self.context_analyzer = CodeContextAnalyzer()
        self.dependency_mapper = DependencyMapper()
    
    def analyze_as_module(self, file_paths: List[str]) -> AnalysisResult:
        """
        Analyze a set of files as a cohesive module
        
        Args:
            file_paths: List of file paths to analyze together
            
        Returns:
            AnalysisResult with module-level analysis
        """
        if not file_paths:
            return AnalysisResult(
                success=False,
                analysis_content="",
                context_summary={},
                analysis_scope="module",
                target_files=[],
                error_message="No files provided for module analysis"
            )
        
        try:
            # Build comprehensive context
            context = self.context_analyzer.build_context_for_files(file_paths)
            
            # Generate analysis
            analysis_content = self._perform_module_analysis(context)
            
            return AnalysisResult(
                success=True,
                analysis_content=analysis_content,
                context_summary=self.context_analyzer.get_context_summary(context),
                analysis_scope="module",
                target_files=file_paths
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                analysis_content="",
                context_summary={},
                analysis_scope="module",
                target_files=file_paths,
                error_message=f"Module analysis failed: {str(e)}"
            )
    
    def analyze_as_project(self, project_path: str) -> AnalysisResult:
        """
        Analyze an entire project for comprehensive review
        
        Args:
            project_path: Path to the project root directory
            
        Returns:
            AnalysisResult with project-level analysis
        """
        if not os.path.exists(project_path):
            return AnalysisResult(
                success=False,
                analysis_content="",
                context_summary={},
                analysis_scope="project",
                target_files=[],
                error_message=f"Project path does not exist: {project_path}"
            )
        
        try:
            # Build comprehensive project context
            context = self.context_analyzer.analyze_project_structure(project_path)
            
            # Generate analysis
            analysis_content = self._perform_project_analysis(context)
            
            return AnalysisResult(
                success=True,
                analysis_content=analysis_content,
                context_summary=self.context_analyzer.get_context_summary(context),
                analysis_scope="project",
                target_files=context.target_files
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                analysis_content="",
                context_summary={},
                analysis_scope="project",
                target_files=[],
                error_message=f"Project analysis failed: {str(e)}"
            )
    
    def _perform_module_analysis(self, context: ProjectContext) -> str:
        """
        Perform AI-powered analysis of a module with full context
        
        Args:
            context: ProjectContext with module information
            
        Returns:
            Formatted analysis content
        """
        if not self.client:
            return self._generate_local_analysis(context)
        
        # Generate context-aware prompt
        context_prompt = self.context_analyzer.generate_context_prompt(context)
        
        # Read target file contents
        file_contents = self._read_target_files(context.target_files)
        
        # Create comprehensive analysis prompt
        analysis_prompt = self._create_module_analysis_prompt(context, context_prompt, file_contents)
        
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer specializing in multi-file analysis with cross-file context awareness."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis failed: {str(e)}\n\n{self._generate_local_analysis(context)}"
    
    def _perform_project_analysis(self, context: ProjectContext) -> str:
        """
        Perform AI-powered analysis of entire project
        
        Args:
            context: ProjectContext with project information
            
        Returns:
            Formatted analysis content
        """
        if not self.client:
            return self._generate_local_analysis(context)
        
        # For project-level analysis, we need to be selective about which files to analyze
        # Focus on key files and representative samples
        key_files = self._select_key_files_for_analysis(context)
        
        # Generate context-aware prompt
        context_prompt = self.context_analyzer.generate_context_prompt(context)
        
        # Read key file contents
        file_contents = self._read_target_files(key_files)
        
        # Create comprehensive project analysis prompt
        analysis_prompt = self._create_project_analysis_prompt(context, context_prompt, file_contents)
        
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert code architect specializing in project-level analysis and architectural review."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis failed: {str(e)}\n\n{self._generate_local_analysis(context)}"
    
    def _create_module_analysis_prompt(self, context: ProjectContext, context_prompt: str, file_contents: Dict[str, str]) -> str:
        """Create analysis prompt for module-level review"""
        
        prompt = f"""You are analyzing a module of {len(context.target_files)} files with full project context.

{context_prompt}

ANALYSIS INSTRUCTIONS:
1. **Cross-File Integration**: Check if imports and function calls work across files
2. **Missing Dependencies**: Identify any missing imports that are available in other files
3. **Module Cohesion**: Evaluate if the files work together as a cohesive module
4. **Interface Consistency**: Check function signatures and data flow between files
5. **Architecture Issues**: Identify any structural problems or improvements

Focus on issues that would be missed in single-file analysis but become apparent with multi-file context.

FILES TO ANALYZE:
"""
        
        for file_path, content in file_contents.items():
            rel_path = Path(file_path).relative_to(context.project_path)
            prompt += f"\n--- {rel_path} ---\n{content}\n"
        
        prompt += """
ANALYSIS FORMAT:
### Module Analysis Results

**Overall Assessment:** [Brief summary of module health]

**Cross-File Issues Found:**
- ❌ [Critical Issue]: Description with file references
- ⚠️ [Warning]: Description with file references  
- ✅ [Good Practice]: Description with file references

**Integration Summary:**
Brief assessment of how well the files work together.

**Recommendations:**
Specific actions to improve module cohesion and fix issues.
"""
        
        return prompt
    
    def _create_project_analysis_prompt(self, context: ProjectContext, context_prompt: str, file_contents: Dict[str, str]) -> str:
        """Create analysis prompt for project-level review"""
        
        prompt = f"""You are analyzing an entire project with {len(context.all_files)} files across the codebase.

{context_prompt}

ANALYSIS INSTRUCTIONS:
1. **Architecture Review**: Evaluate overall project structure and organization
2. **Dependency Analysis**: Check for circular dependencies and coupling issues
3. **Framework Compliance**: Verify adherence to detected framework best practices
4. **Scalability Issues**: Identify potential bottlenecks or architectural concerns
5. **Code Quality**: Assess consistency and maintainability across the project

Focus on high-level architectural issues and project-wide patterns.

KEY FILES ANALYZED:
"""
        
        for file_path, content in file_contents.items():
            rel_path = Path(file_path).relative_to(context.project_path)
            # Truncate very long files for project-level analysis
            if len(content) > 2000:
                content = content[:2000] + "\n... [truncated for analysis]"
            prompt += f"\n--- {rel_path} ---\n{content}\n"
        
        prompt += """
ANALYSIS FORMAT:
### Project Architecture Analysis

**Overall Assessment:** [Brief summary of project health and architecture]

**Architecture Issues:**
- ❌ [Critical]: Description with architectural impact
- ⚠️ [Warning]: Description with recommendations
- ✅ [Strength]: Positive architectural decisions

**Framework Compliance:**
Assessment of adherence to framework best practices.

**Scalability Concerns:**
Potential issues that could impact growth or maintenance.

**Recommendations:**
High-level architectural improvements and refactoring suggestions.
"""
        
        return prompt
    
    def _select_key_files_for_analysis(self, context: ProjectContext) -> List[str]:
        """Select key files for project-level analysis to stay within token limits"""
        key_files = []
        
        # Always include framework files
        key_files.extend(context.framework_files[:3])  # Top 3 framework files
        
        # Include main entry points
        for file_path in context.all_files:
            file_name = Path(file_path).name.lower()
            if file_name in ['main.py', 'app.py', 'index.js', 'index.html', '__init__.py']:
                if file_path not in key_files:
                    key_files.append(file_path)
        
        # Include files with most dependencies
        file_dep_counts = [(f, len(context.dependency_graph.get(f, []))) for f in context.all_files]
        file_dep_counts.sort(key=lambda x: x[1], reverse=True)
        
        for file_path, _ in file_dep_counts[:5]:  # Top 5 most connected files
            if file_path not in key_files:
                key_files.append(file_path)
        
        # Include files with most exports (likely important interfaces)
        file_export_counts = []
        for file_path in context.all_files:
            analysis = context.file_analyses.get(file_path)
            if analysis:
                file_export_counts.append((file_path, len(analysis.exports)))
        
        file_export_counts.sort(key=lambda x: x[1], reverse=True)
        for file_path, _ in file_export_counts[:3]:  # Top 3 files with most exports
            if file_path not in key_files:
                key_files.append(file_path)
        
        # Limit to reasonable number for analysis
        return key_files[:10]
    
    def _read_target_files(self, file_paths: List[str]) -> Dict[str, str]:
        """Read contents of target files"""
        file_contents = {}
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Truncate extremely long files
                    if len(content) > 8000:
                        content = content[:8000] + "\n... [file truncated for analysis]"
                    
                    file_contents[file_path] = content
                    
            except Exception as e:
                file_contents[file_path] = f"Error reading file: {str(e)}"
        
        return file_contents
    
    def _generate_local_analysis(self, context: ProjectContext) -> str:
        """Generate local analysis when AI is not available"""
        
        analysis_parts = []
        
        # Header
        analysis_parts.append(f"### Local Analysis ({context.analysis_scope.title()} Level)")
        analysis_parts.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        analysis_parts.append(f"**Files Analyzed:** {len(context.target_files)}")
        
        if context.detected_framework:
            analysis_parts.append(f"**Framework:** {context.detected_framework}")
        
        # Missing imports analysis
        if context.missing_imports:
            analysis_parts.append("\n**Potential Missing Imports:**")
            for file_path, missing_list in context.missing_imports.items():
                rel_path = Path(file_path).relative_to(context.project_path)
                analysis_parts.append(f"- {rel_path}:")
                for missing in missing_list:
                    symbol = missing['symbol']
                    sources = missing['available_in']
                    source_names = [Path(s).name for s in sources]
                    analysis_parts.append(f"  ❌ '{symbol}' may need import from: {', '.join(source_names)}")
        
        # Dependency analysis
        if context.dependency_graph:
            analysis_parts.append("\n**File Dependencies:**")
            for file_path, deps in context.dependency_graph.items():
                if deps:
                    rel_path = Path(file_path).relative_to(context.project_path)
                    dep_names = [Path(d).name for d in deps]
                    analysis_parts.append(f"- {rel_path.name} depends on: {', '.join(dep_names)}")
        
        # External dependencies
        if context.external_dependencies:
            analysis_parts.append(f"\n**External Dependencies:** {len(context.external_dependencies)}")
            for dep in sorted(context.external_dependencies):
                analysis_parts.append(f"- {dep}")
        
        # Summary
        analysis_parts.append("\n**Summary:**")
        analysis_parts.append("Local analysis complete. For detailed code review with AI insights,")
        analysis_parts.append("please configure OpenAI API key in your .env file.")
        
        return "\n".join(analysis_parts)
    
    def generate_multi_file_prompt(self, context: ProjectContext) -> str:
        """
        Generate a prompt optimized for multi-file analysis
        
        Args:
            context: ProjectContext with analysis information
            
        Returns:
            Formatted prompt for multi-file analysis
        """
        return self.context_analyzer.generate_context_prompt(context)
    
    def get_analysis_capabilities(self) -> Dict[str, Any]:
        """
        Get information about analysis capabilities
        
        Returns:
            Dict with capability information
        """
        return {
            'ai_available': self.client is not None,
            'supported_scopes': ['module', 'project'],
            'max_files_per_analysis': 50,
            'supported_extensions': list(self.context_analyzer.source_extensions),
            'framework_detection': list(self.context_analyzer.framework_patterns.keys())
        }
