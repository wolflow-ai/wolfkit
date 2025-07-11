# === code_reviewer.py ===
import os
import json
from datetime import datetime
from typing import List, Tuple, Dict
from pathlib import Path

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

class CodeReviewer:
    def __init__(self):
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.reports_dir = "./reports"
        self._setup_client()
        self._ensure_reports_dir()

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

    def analyze_files(self, file_paths: List[str]) -> Tuple[bool, str, str]:
        """
        Analyze multiple files and generate a markdown report
        
        Returns:
            success (bool): Whether analysis completed
            report_path (str): Path to generated report
            message (str): Status message
        """
        if not file_paths:
            return False, "", "No files provided for analysis"

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
        report_content = f"""# Wolfkit AI Code Review
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Files Analyzed:** {len(file_paths)}  
**Successful:** {successful_analyses}  
**Model Used:** {self.model}

---

"""

        # Add all analyses
        report_content += "\n\n---\n\n".join(analyses)

        try:
            # Write report to file
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            message = f"Analysis complete! {successful_analyses}/{len(file_paths)} files analyzed successfully."
            return True, report_path, message
            
        except Exception as e:
            return False, "", f"Failed to write report: {str(e)}"

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
        
        return True, "Code reviewer is properly configured and ready to use."


# Convenience functions for controller integration
def analyze_files(file_paths: List[str]) -> Tuple[bool, str, str]:
    """Convenience function for analyzing files"""
    reviewer = CodeReviewer()
    return reviewer.analyze_files(file_paths)

def check_reviewer_config() -> Tuple[bool, str]:
    """Convenience function for checking configuration"""
    reviewer = CodeReviewer()
    return reviewer.check_configuration()
