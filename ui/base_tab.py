# ui/base_tab.py
"""
BaseTab - Common functionality for all Wolfkit tabs
Created as part of Phase 2 refactoring
"""
import os
import sys
import subprocess
import webbrowser
from abc import ABC, abstractmethod
from ttkbootstrap import Frame
from ui.widgets import ConsoleOutput, ProgressTracker, StatusOnlyTracker


class BaseTab(Frame, ABC):
    """Base class for all Wolfkit tabs providing common functionality"""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize BaseTab
        
        Args:
            parent: Parent notebook widget
            **kwargs: Additional keyword arguments for Frame
        """
        super().__init__(parent, **kwargs)
        
        # Common state
        self.parent = parent
        self._initialized = False
        
        # Call abstract method to setup the specific tab
        self.setup_tab()
        self._initialized = True
    
    @abstractmethod
    def setup_tab(self):
        """Abstract method to setup the specific tab UI - must be implemented by subclasses"""
        pass
    
    def get_project_directory(self):
        """Get the current project directory from the main app state"""
        # This will be implemented to communicate with the main app frame
        # For now, import from controller
        from controller import get_project_directory
        return get_project_directory()
    
    def open_file(self, file_path):
        """
        Open a file using the system default application
        
        Args:
            file_path: Path to the file to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
            return True
        except Exception:
            # Fallback: try to open with webbrowser
            try:
                webbrowser.open(f"file://{os.path.abspath(file_path)}")
                return True
            except Exception:
                return False
    
    def create_console_section(self, title="Console Output:", height=20):
        """
        Create a console output section with consistent styling
        
        Args:
            title: Title for the console section
            height: Height in lines for the console
            
        Returns:
            ConsoleOutput: The created console widget
        """
        console = ConsoleOutput(self, title=title, height=height)
        return console
    
    def create_progress_section(self):
        """
        Create a progress tracker section
        
        Returns:
            ProgressTracker: The created progress tracker widget
        """
        progress = ProgressTracker(self)
        return progress
    
    def create_status_section(self, initial_message="Ready"):
        """
        Create a status-only tracker section
        
        Args:
            initial_message: Initial status message
            
        Returns:
            StatusOnlyTracker: The created status tracker widget
        """
        status = StatusOnlyTracker(self, initial_message=initial_message)
        return status
    
    def show_error(self, title, message):
        """
        Show an error message dialog
        
        Args:
            title: Dialog title
            message: Error message
        """
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def show_warning(self, title, message):
        """
        Show a warning message dialog
        
        Args:
            title: Dialog title
            message: Warning message
        """
        from tkinter import messagebox
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message):
        """
        Show an info message dialog
        
        Args:
            title: Dialog title
            message: Info message
        """
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    def ask_yes_no(self, title, message):
        """
        Show a yes/no question dialog
        
        Args:
            title: Dialog title
            message: Question message
            
        Returns:
            bool: True for yes, False for no
        """
        from tkinter import messagebox
        return messagebox.askyesno(title, message)
    
    def ask_yes_no_cancel(self, title, message):
        """
        Show a yes/no/cancel question dialog
        
        Args:
            title: Dialog title
            message: Question message
            
        Returns:
            bool or None: True for yes, False for no, None for cancel
        """
        from tkinter import messagebox
        return messagebox.askyesnocancel(title, message)
    
    def select_file(self, title="Select File", filetypes=None, initial_dir=None):
        """
        Show file selection dialog
        
        Args:
            title: Dialog title
            filetypes: List of file type tuples
            initial_dir: Initial directory
            
        Returns:
            str or None: Selected file path or None if cancelled
        """
        from tkinter import filedialog
        return filedialog.askopenfilename(
            title=title, 
            filetypes=filetypes or [("All Files", "*.*")],
            initialdir=initial_dir
        )
    
    def select_files(self, title="Select Files", filetypes=None, initial_dir=None):
        """
        Show multiple file selection dialog
        
        Args:
            title: Dialog title
            filetypes: List of file type tuples
            initial_dir: Initial directory
            
        Returns:
            tuple: Selected file paths or empty tuple if cancelled
        """
        from tkinter import filedialog
        return filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes or [("All Files", "*.*")],
            initialdir=initial_dir
        )
    
    def select_directory(self, title="Select Directory", initial_dir=None):
        """
        Show directory selection dialog
        
        Args:
            title: Dialog title
            initial_dir: Initial directory
            
        Returns:
            str or None: Selected directory path or None if cancelled
        """
        from tkinter import filedialog
        return filedialog.askdirectory(title=title, initialdir=initial_dir)
    
    def is_initialized(self):
        """Check if the tab has been fully initialized"""
        return self._initialized