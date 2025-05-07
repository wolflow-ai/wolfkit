# === controller.py ===
import os
import shutil
import subprocess
import sys
import webbrowser

BACKUP_DIR = "./backups"
PROJECT_DIR = None

os.makedirs(BACKUP_DIR, exist_ok=True)

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