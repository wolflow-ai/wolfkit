# code_reviewer.py (Enhanced)
"""
Enhanced Code Reviewer for Wolfkit - Now with multi-file analysis capabilities
Maintains backward compatibility while adding module and project-level analysis
"""
import os
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional
from pathlib import Path
from enum import Enum

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Import our new multi-file analysis modules
from multi_file_analyzer import MultiFileAnalyzer, AnalysisResult
from code_context_analyzer import CodeContextAnalyzer
from dependency_mapper import DependencyMapper


class AnalysisScope(Enum):
    """Enumeration of analysis scopes"""
    SINGLE = "single"
    MODULE = "module"
    PROJECT = "project"


class CodeReviewer:
    """
    Enhanced code reviewer with multi-file analysis capabilities
    """
    
    def __init__(self):
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.reports_dir = "./reports"
        self.multi_file_analyzer = None
        self.context_analyzer = None
        self.dependency_mapper = None
        
        self._setup_client()
        self._ensure_reports_dir()
        self._setup_multi_file_components()

    def _setup_client(self):
        """Initialize OpenAI client with API key from environment"""
        if not OPENAI_AVAILABLE:
            return
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")

    def _ensure_reports_dir(self):
        """Create reports directory if it doesn't exist"""
        os.makedirs(self.reports_dir, exist_ok=True)

    def _setup_multi_file_components(self):
        """Initialize multi-file analysis components"""
        if self.client:
            self.multi_file_analyzer = MultiFileAnalyzer(self.client)
            self.context_analyzer = CodeContextAnalyzer()
            self.dependency_mapper = DependencyMapper()

    # === ENHANCED ANALYSIS METHODS ===

    def analyze_files(self, file_paths: List[str], scope: AnalysisScope = AnalysisScope.SINGLE) -> Tuple[bool, str, str]:
        """
        Enhanced file analysis with configurable scope
        
        Args:
            file_paths: List of file paths to analyze
            scope: Analysis scope (SINGLE, MODULE, or PROJECT)
            
        Returns:
            Tuple of (success, report_path, message)
        """
        if not file_paths:
            return False, "", "No files provided for analysis"

        if scope == AnalysisScope.SINGLE:
            return self._analyze_files_individually(file_paths)
        elif scope == AnalysisScope.MODULE:
            return self._analyze_files_as_module(file_paths)
        elif scope == AnalysisScope.PROJECT:
            # For project analysis, use the parent directory of the files
            project_path = self._determine_project_path(file_paths)
            return self._analyze_entire_project(project_path)
        else:
            return False, "", f"Unknown analysis scope: {scope}"

    def analyze_module(self, file_paths: List[str]) -> Tuple[bool, str, str]:
        """
        Analyze multiple files as a cohesive module
        
        Args:
            file_paths: List of file paths to analyze as a module
            
        Returns:
            Tuple of (success, report_path, message)
        """
        return self.analyze_files(file_paths, AnalysisScope.MODULE)

    def analyze_project(self, project_path: str) -> Tuple[bool, str, str]:
        """
        Analyze entire project for comprehensive review
        
        Args:
            project_path: Path to the project root directory
            
        Returns:
            Tuple of (success, report_path, message)
        """
        if not os.path.exists(project_path):
            return False, "", f"Project path does not exist: {project_path}"
        
        return self._analyze_entire_project(project_path)

    # === IMPLEMENTATION METHODS ===

    def _analyze_files_individually(self, file_paths: List[str]) -> Tuple[bool, str, str]:
        """Original single-file analysis method"""
        if not self.client:
            return False, "", "OpenAI client not available. Please check your .env file contains OPENAI_API_KEY."

        # Generate timestamp for report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"wolfkit_analysis_{timestamp}.md"
        report_path = os.path.join(self.reports_dir, report_filename)

        analyses = []
        successful_analyses = 0
        
        for file_path in file_paths:
            success, result = self._analyze_single_file(file_path)
            if success:
                analyses.append(result)
                successful_analyses += 1
            else:
                analyses.append(f"### Error analyzing `{os.path.basename(file_path)}`\n\n❌ {result}\n\n---\n")

        # Generate report header
        report_content = f"""# Wolfkit AI Code Review (Individual Files)
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Files Analyzed:** {len(file_paths)}  
**Successful:** {successful_analyses}  
**Model Used:** {self.model}
**Analysis Scope:** Individual file analysis

---

"""

        # Add all analyses
        report_content += "\n\n---\n\n".join(analyses)

        try:
            # Write report to file
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            message = f"Individual analysis complete! {successful_analyses}/{len(file_paths)} files analyzed successfully."
            return True, report_path, message
            
        except Exception as e:
            return False, "", f"Failed to write report: {str(e)}"

    def _analyze_files_as_module(self, file_paths: List[str]) -> Tuple[bool, str, str]:
        """Analyze files as a cohesive module"""
        if not self.multi_file_analyzer:
            return False, "", "Multi-file analysis not available. Please check your .env file contains OPENAI_API_KEY."

        try:
            # Perform module analysis
            result = self.multi_file_analyzer.analyze_as_module(file_paths)
            
            if not result.success:
                return False, "", result.error_message
            
            # Generate report
            report_path = self._generate_multi_file_report(result, "Module")
            
            return True, report_path, f"Module analysis complete! {len(file_paths)} files analyzed as cohesive module."
            
        except Exception as e:
            return False, "", f"Module analysis failed: {str(e)}"

    def _analyze_entire_project(self, project_path: str) -> Tuple[bool, str, str]:
        """Analyze entire project"""
        if not self.multi_file_analyzer:
            return False, "", "Project analysis not available. Please check your .env file contains OPENAI_API_KEY."

        try:
            # Perform project analysis
            result = self.multi_file_analyzer.analyze_as_project(project_path)
            
            if not result.success:
                return False, "", result.error_message
            
            # Generate report
            report_path = self._generate_multi_file_report(result, "Project")
            
            total_files = result.context_summary.get('total_files', 0)
            return True, report_path, f"Project analysis complete! {total_files} files analyzed for architectural review."
            
        except Exception as e:
            return False, "", f"Project analysis failed: {str(e)}"

    def _generate_multi_file_report(self, result: AnalysisResult, analysis_type: str) -> str:
        """Generate report for multi-file analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"wolfkit_{analysis_type.lower()}_analysis_{timestamp}.md"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        # Build report content
        report_content = f"""# Wolfkit AI Code Review ({analysis_type} Analysis)
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Analysis Type:** {analysis_type}  
**Model Used:** {self.model}

## Analysis Summary
- **Target Files:** {len(result.target_files)}
- **Analysis Scope:** {result.analysis_scope}
"""

        # Add context summary
        if result.context_summary:
            summary = result.context_summary
            if summary.get('framework'):
                report_content += f"- **Framework:** {summary['framework']}\n"
            if summary.get('total_files'):
                report_content += f"- **Total Context Files:** {summary['total_files']}\n"
            if summary.get('external_deps'):
                report_content += f"- **External Dependencies:** {summary['external_deps']}\n"
            if summary.get('missing_imports'):
                report_content += f"- **Missing Imports Found:** {summary['missing_imports']}\n"

        report_content += f"""
---

## Target Files
"""
        
        # List target files
        for file_path in result.target_files:
            rel_path = Path(file_path).name
            report_content += f"- `{rel_path}`\n"

        report_content += f"""
---

{result.analysis_content}

---

*This {analysis_type.lower()} analysis was generated by Wolfkit's enhanced code review system with cross-file context awareness.*
"""

        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path

    def _determine_project_path(self, file_paths: List[str]) -> str:
        """Determine project root path from file paths"""
        if not file_paths:
            return os.getcwd()
        
        # Find common parent directory
        common_path = Path(os.path.commonpath(file_paths))
        
        # If common path is a file, use its parent
        if common_path.is_file():
            common_path = common_path.parent
        
        return str(common_path)

    # === ORIGINAL METHODS (PRESERVED FOR BACKWARD COMPATIBILITY) ===

    def _get_file_type_prompt(self, file_extension: str) -> str:
        """Return file-type specific analysis prompt"""
        
        base_prompt = """You are an expert code reviewer. Analyze the provided code file and identify:

1. **Syntax Errors**: Any obvious syntax issues
2. **Missing Dependencies**: Undefined variables, functions, or imports
3. **Logic Issues**: Common programming mistakes or inconsistencies
4. **Structure Problems**: Missing entry points, circular references
5. **Best Practices**: Simple improvements that could prevent issues

Focus on issues that would prevent the code from running or cause immediate problems.
Be concise but specific. Use clear categories and bullet points.

Return your analysis in this markdown format:

### Analysis of `{filename}`

**File Type:** [language]  
**Syntax Check:** ✅ Valid / ❌ Issues found  

**Issues Found:**
- ❌ [Critical Issue]: Description
- ⚠️ [Warning]: Description  
- ✅ [Good Practice Found]: Description

**Summary:**
Brief overall assessment and main recommendations.

---
"""

        prompts = {
            '.py': base_prompt + """
Pay special attention to:
- Import statements and module availability
- Function definitions vs calls
- Indentation and Python syntax
- Missing main() blocks or entry points
""",
            '.js': base_prompt + """
Pay special attention to:
- Variable declarations (let, const, var)
- Function definitions vs calls
- Missing semicolons or brackets
- Async/await usage
""",
            '.ts': base_prompt + """
Pay special attention to:
- TypeScript type annotations
- Interface definitions
- Import/export statements
- Type mismatches
""",
            '.html': base_prompt + """
Pay special attention to:
- Tag structure and nesting
- Missing closing tags
- Script and link references
- Form structure
""",
            '.css': base_prompt + """
Pay special attention to:
- Selector syntax
- Property names and values
- Missing semicolons or brackets
- CSS rule structure
""",
            '.json': base_prompt + """
Pay special attention to:
- JSON syntax validity
- Proper quotation marks
- Comma placement
- Bracket/brace matching
"""
        }
        
        return prompts.get(file_extension.lower(), base_prompt)

    def _analyze_single_file(self, file_path: str) -> Tuple[bool, str]:
        """Analyze a single file with LLM"""
        if not self.client:
            return False, "OpenAI client not available. Check API key in .env file."

        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path)
            file_extension = Path(file_path).suffix
            
            # Get appropriate prompt for file type
            prompt = self._get_file_type_prompt(file_extension)
            
            # Prepare the full prompt
            full_prompt = f"{prompt}\n\nFile to analyze: `{filename}`\n\n```{file_extension[1:]}\n{content}\n```"
            
            # Send to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer focused on finding issues that prevent code from running."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.1
            )
            
            analysis = response.choices[0].message.content
            return True, analysis.replace("{filename}", filename)
            
        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        except Exception as e:
            return False, f"Error analyzing {file_path}: {str(e)}"

    def check_configuration(self) -> Tuple[bool, str]:
        """Check if the reviewer is properly configured"""
        issues = []
        
        if not OPENAI_AVAILABLE:
            issues.append("OpenAI package not installed (pip install openai)")
        
        if not DOTENV_AVAILABLE:
            issues.append("python-dotenv package not installed (pip install python-dotenv)")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            issues.append("OPENAI_API_KEY not found in .env file")
        elif not api_key.startswith("sk-"):
            issues.append("OPENAI_API_KEY appears to be invalid")
        
        if not self.client:
            issues.append("OpenAI client failed to initialize")
        
        if issues:
            return False, "Configuration issues found:\n" + "\n".join(f"- {issue}" for issue in issues)
        
        # Check multi-file capabilities
        capabilities = []
        if self.multi_file_analyzer:
            capabilities.append("✅ Multi-file analysis ready")
            capabilities.append("✅ Module analysis ready")
            capabilities.append("✅ Project analysis ready")
        else:
            capabilities.append("⚠️ Multi-file analysis limited (check API key)")
        
        return True, "Code reviewer is properly configured and ready to use.\n" + "\n".join(capabilities)

    def get_analysis_capabilities(self) -> Dict[str, any]:
        """Get information about available analysis capabilities"""
        base_capabilities = {
            'single_file': True,
            'openai_available': OPENAI_AVAILABLE,
            'client_configured': self.client is not None
        }
        
        if self.multi_file_analyzer:
            multi_file_caps = self.multi_file_analyzer.get_analysis_capabilities()
            base_capabilities.update(multi_file_caps)
        else:
            base_capabilities.update({
                'ai_available': False,
                'supported_scopes': ['single'],
                'max_files_per_analysis': 1
            })
        
        return base_capabilities


# === CONVENIENCE FUNCTIONS FOR CONTROLLER INTEGRATION ===

def analyze_files(file_paths: List[str]) -> Tuple[bool, str, str]:
    """Convenience function for single-file analysis (backward compatibility)"""
    reviewer = CodeReviewer()
    return reviewer.analyze_files(file_paths, AnalysisScope.SINGLE)

def analyze_module(file_paths: List[str]) -> Tuple[bool, str, str]:
    """Convenience function for module analysis"""
    reviewer = CodeReviewer()
    return reviewer.analyze_module(file_paths)

def analyze_project(project_path: str) -> Tuple[bool, str, str]:
    """Convenience function for project analysis"""
    reviewer = CodeReviewer()
    return reviewer.analyze_project(project_path)

def check_reviewer_config() -> Tuple[bool, str]:
    """Convenience function for checking configuration"""
    reviewer = CodeReviewer()
    return reviewer.check_configuration()

def get_reviewer_capabilities() -> Dict[str, any]:
    """Convenience function for getting capabilities"""
    reviewer = CodeReviewer()
    return reviewer.get_analysis_capabilities()