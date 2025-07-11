# === controller.py ===
import os
import shutil
import subprocess
import sys
import webbrowser
from typing import List, Tuple

BACKUP_DIR = "./backups"
PROJECT_DIR = None

os.makedirs(BACKUP_DIR, exist_ok=True)

# === Existing Core Functions ===

def set_project_directory(path):
    global PROJECT_DIR
    PROJECT_DIR = os.path.abspath(path)
    return PROJECT_DIR

def get_project_directory():
    return PROJECT_DIR

def stage_file(test_file_path, target_filename):
    if not PROJECT_DIR:
        return False, "No project directory set."

    target_path = os.path.join(PROJECT_DIR, target_filename)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(PROJECT_DIR), target_filename + ".bak")

    try:
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        if not os.path.isfile(test_file_path):
            return False, "Selected test file does not exist."

        if os.path.exists(target_path):
            shutil.copy2(target_path, backup_path)
            response = f"Backup created: {target_filename}.bak"
        else:
            response = f"File '{target_filename}' does not exist in project. It will be added."

        shutil.copy2(test_file_path, target_path)

        return True, f"Staged: {os.path.basename(test_file_path)} → {target_filename}\n{response}"

    except Exception as e:
        return False, f"Error during staging: {str(e)}"

def run_project_entry():
    if not PROJECT_DIR:
        return False, "No project directory set."

    try:
        project_name = os.path.basename(PROJECT_DIR)
        main_path = os.path.join(PROJECT_DIR, "main.py")

        if not os.path.exists(main_path):
            return False, f"No main.py found in {project_name}"

        # Prefer local venv if found
        venv_python = os.path.join(PROJECT_DIR, "venv", "Scripts", "python.exe") if sys.platform.startswith("win") \
                      else os.path.join(PROJECT_DIR, "venv", "bin", "python")

        if os.path.exists(venv_python):
            python_exec = venv_python
            note = "Using project venv"
        else:
            python_exec = sys.executable
            note = "Using global Python"

        flags = subprocess.CREATE_NEW_CONSOLE if sys.platform.startswith("win") else 0
        subprocess.Popen([python_exec, "main.py"], cwd=PROJECT_DIR, creationflags=flags)

        return True, f"{note}: Launching {project_name} with {os.path.basename(python_exec)}"

    except Exception as e:
        return False, f"Failed to launch Python project: {str(e)}"

def open_static_web_page():
    if not PROJECT_DIR:
        return False, "No project directory set."

    index_path = os.path.join(PROJECT_DIR, "index.html")
    if not os.path.exists(index_path):
        return False, "No index.html found in project directory."

    try:
        webbrowser.open(f"file://{index_path}")
        return True, "Opening index.html in web browser."
    except Exception as e:
        return False, f"Failed to open web page: {str(e)}"

def revert_file(target_filename):
    if not PROJECT_DIR:
        return False, "No project directory set."

    target_path = os.path.join(PROJECT_DIR, target_filename)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(PROJECT_DIR), target_filename + ".bak")

    if os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, target_path)
            return True, f"Reverted {target_filename} to backup version. Backup retained."
        except Exception as e:
            return False, f"Failed to revert {target_filename}: {str(e)}"
    elif os.path.exists(target_path):
        try:
            os.remove(target_path)
            return True, f"Removed newly added file {target_filename} (no backup existed)."
        except Exception as e:
            return False, f"Failed to remove new file {target_filename}: {str(e)}"
    else:
        return False, f"No backup or current file found for {target_filename}."

def accept_file(target_filename):
    if not PROJECT_DIR:
        return False, "No project directory set."

    backup_path = os.path.join(BACKUP_DIR, os.path.basename(PROJECT_DIR), target_filename + ".bak")

    if not os.path.exists(backup_path):
        return False, f"No backup exists for {target_filename}."

    try:
        os.remove(backup_path)
        return True, f"Accepted test version of {target_filename}. Backup removed."
    except Exception as e:
        return False, f"Failed to delete backup: {str(e)}"

def accept_batch(batch):
    return [accept_file(target) for (_, target) in batch]

def revert_batch(batch):
    return [revert_file(target) for (_, target) in batch]

# === NEW: Code Review Integration Functions ===

def analyze_code_files(file_paths: List[str]) -> Tuple[bool, str, str]:
    """
    Analyze code files using AI and generate a report
    
    Args:
        file_paths: List of file paths to analyze
        
    Returns:
        Tuple of (success, report_path, message)
    """
    try:
        from code_reviewer import analyze_files
        return analyze_files(file_paths)
    except ImportError as e:
        return False, "", f"Code review module not available: {str(e)}"
    except Exception as e:
        return False, "", f"Failed to analyze files: {str(e)}"

def check_code_review_config() -> Tuple[bool, str]:
    """
    Check if code review functionality is properly configured
    
    Returns:
        Tuple of (success, message)
    """
    try:
        from code_reviewer import check_reviewer_config
        return check_reviewer_config()
    except ImportError:
        return False, "Code review module not available. Please install required dependencies:\npip install openai python-dotenv"
    except Exception as e:
        return False, f"Error checking configuration: {str(e)}"

def get_project_files_for_analysis() -> List[str]:
    """
    Get a list of common code files in the current project directory
    Useful for quick selection of project files for analysis
    
    Returns:
        List of file paths found in the project
    """
    if not PROJECT_DIR:
        return []
    
    # Common code file extensions to look for
    code_extensions = {'.py', '.js', '.ts', '.html', '.css', '.json', '.md', '.txt'}
    
    project_files = []
    
    try:
        for root, dirs, files in os.walk(PROJECT_DIR):
            # Skip common directories that usually don't contain source code
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.vscode', '.idea', 'venv', 'env'}]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in code_extensions:
                    # Make path relative to project directory for cleaner display
                    relative_path = os.path.relpath(file_path, PROJECT_DIR)
                    project_files.append(file_path)
        
        return sorted(project_files)
        
    except Exception as e:
        return []

def analyze_project_files() -> Tuple[bool, str, str]:
    """
    Analyze all code files in the current project directory
    
    Returns:
        Tuple of (success, report_path, message)
    """
    if not PROJECT_DIR:
        return False, "", "No project directory set."
    
    project_files = get_project_files_for_analysis()
    
    if not project_files:
        return False, "", "No code files found in project directory."
    
    return analyze_code_files(project_files)

def get_reports_directory() -> str:
    """
    Get the path to the reports directory
    Creates it if it doesn't exist
    
    Returns:
        Path to reports directory
    """
    reports_dir = "./reports"
    os.makedirs(reports_dir, exist_ok=True)
    return os.path.abspath(reports_dir)

def list_recent_reports(limit: int = 10) -> List[Tuple[str, str]]:
    """
    Get a list of recent analysis reports
    
    Args:
        limit: Maximum number of reports to return
        
    Returns:
        List of tuples (filename, full_path) sorted by modification time (newest first)
    """
    reports_dir = get_reports_directory()
    
    try:
        report_files = []
        for file in os.listdir(reports_dir):
            if file.startswith("wolfkit_analysis_") and file.endswith(".md"):
                file_path = os.path.join(reports_dir, file)
                mtime = os.path.getmtime(file_path)
                report_files.append((mtime, file, file_path))
        
        # Sort by modification time (newest first) and return limited results
        report_files.sort(reverse=True)
        return [(filename, filepath) for (_, filename, filepath) in report_files[:limit]]
        
    except Exception:
        return []

# === Convenience Functions for GUI Integration ===

def quick_analyze_files(file_paths: List[str]) -> Tuple[bool, str]:
    """
    Quick analysis function that returns just success and message
    Suitable for simple status updates
    """
    success, report_path, message = analyze_code_files(file_paths)
    return success, message

def get_analysis_status() -> str:
    """
    Get a status string about code review configuration
    """
    success, message = check_code_review_config()
    if success:
        return "✅ Code review ready"
    else:
        return "❌ Code review not configured"
