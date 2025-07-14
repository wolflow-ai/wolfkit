# ui/main_workflow_tab.py
"""
MainWorkflowTab - Core file staging workflow functionality
Extracted from app_frame.py as part of Phase 2 refactoring
"""
import os
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Radiobutton
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab
from controller import (
    stage_file,
    set_project_directory,
    get_project_directory,
    run_project_entry,
    open_static_web_page,
    revert_batch,
    accept_batch
)


class MainWorkflowTab(BaseTab):
    """Main workflow tab for file staging, testing, and batch operations"""
    
    def __init__(self, parent, **kwargs):
        """Initialize MainWorkflowTab"""
        self.last_batch = []
        self.launch_type = tk.StringVar(value="python")
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the main workflow tab UI"""
        # Project directory section
        self.project_dir_label = Label(self, text="📁 No project directory set", anchor="w")
        self.project_dir_label.pack(fill=X, pady=(0, 10))

        # Top button frame
        top_button_frame = Frame(self)
        top_button_frame.pack(fill=X, pady=(0, 10))

        self.set_project_btn = Button(
            top_button_frame, 
            text="Set Project Directory", 
            command=self.select_project_directory
        )
        self.set_project_btn.pack(side=LEFT, padx=(0, 10))

        self.select_button = Button(
            top_button_frame, 
            text="Select File(s) to Test", 
            command=self.select_files_to_test
        )
        self.select_button.pack(side=LEFT)

        # Launch mode selection
        launch_mode_frame = Frame(self)
        launch_mode_frame.pack(fill=X, pady=(0, 10))
        
        Label(launch_mode_frame, text="Launch Type:").pack(side=LEFT)
        
        Radiobutton(
            launch_mode_frame, 
            text="Python App", 
            variable=self.launch_type, 
            value="python"
        ).pack(side=LEFT, padx=(5, 10))
        
        Radiobutton(
            launch_mode_frame, 
            text="Static Web Page", 
            variable=self.launch_type, 
            value="web"
        ).pack(side=LEFT)

        # File selection status
        self.file_label = Label(self, text="No files selected", anchor="w")
        self.file_label.pack(fill=X, pady=(0, 10))

        # Action buttons
        button_frame = Frame(self)
        button_frame.pack(fill=X, pady=(0, 10))

        self.run_button = Button(
            button_frame, 
            text="Run Test", 
            bootstyle="primary", 
            command=self.run_test
        )
        self.run_button.pack(side=LEFT, padx=5)

        self.revert_button = Button(
            button_frame, 
            text="Revert Batch", 
            bootstyle="warning", 
            command=self.revert_test_batch
        )
        self.revert_button.pack(side=LEFT, padx=5)

        self.accept_button = Button(
            button_frame, 
            text="Accept Batch", 
            bootstyle="success", 
            command=self.accept_test_batch
        )
        self.accept_button.pack(side=LEFT, padx=5)

        # Console output section
        self.console = self.create_console_section("Console Output:", height=20)
        self.console.pack(fill=BOTH, expand=YES, pady=(10, 0))

    def select_project_directory(self):
        """Handle project directory selection"""
        directory = self.select_directory(title="Select Target Project Directory")
        if directory:
            resolved = set_project_directory(directory)
            self.project_dir_label.config(text=f"📁 Working on: {resolved}")
            self.console.write_info(f"Set project directory to: {resolved}")

    def select_files_to_test(self):
        """Handle test file selection and staging"""
        file_paths = self.select_files(title="Select Test File(s)")
        if not file_paths:
            self.console.write_warning("No files selected.")
            return

        self.last_batch = []
        self.file_label.config(text=f"Selected: {len(file_paths)} files")

        for path in file_paths:
            filename = os.path.basename(path)
            project_dir = get_project_directory()

            if not project_dir:
                self.show_error("Error", "No project directory set. Please set a project directory first.")
                return

            # Ask user what to do with this file
            response = self.ask_yes_no_cancel(
                "Test File Action", 
                f"Do you want to replace an existing file with {filename}?\n\n"
                f"Yes = Select file to replace\n"
                f"No = Add {filename} as new\n"
                f"Cancel = Skip"
            )

            if response is None:  # Cancel
                self.console.write_warning(f"Skipped: {filename}")
                continue
            elif response:  # Yes - replace existing
                target_file_path = self.select_file(
                    title=f"Choose file in project to replace with {filename}",
                    initial_dir=project_dir
                )
                if not target_file_path:
                    self.console.write_warning(f"Skipped: {filename}")
                    continue
                target_filename = os.path.relpath(target_file_path, project_dir)
            else:  # No - add new
                dir_path = self.select_directory(
                    title=f"Select folder to add {filename} in",
                    initial_dir=project_dir
                )
                if not dir_path:
                    self.console.write_warning(f"Skipped: {filename}")
                    continue
                target_filename = os.path.relpath(os.path.join(dir_path, filename), project_dir)

            # Stage the file
            success, message = stage_file(path, target_filename)
            if success:
                self.console.write_success(message)
                self.last_batch.append((path, target_filename))
            else:
                self.console.write_error(message)

    def run_test(self):
        """Run the test based on selected launch type"""
        mode = self.launch_type.get()
        
        if mode == "python":
            success, message = run_project_entry()
        elif mode == "web":
            success, message = open_static_web_page()
        else:
            success, message = False, "Unknown launch type selected."

        if success:
            self.console.write_success(message)
        else:
            self.console.write_error(message)

    def revert_test_batch(self):
        """Revert all files in the current test batch"""
        if not self.last_batch:
            self.console.write_warning("No test batch to revert.")
            return
        
        self.console.write_info("Reverting test batch...")
        results = revert_batch(self.last_batch)
        
        for success, msg in results:
            if success:
                self.console.write_success(msg)
            else:
                self.console.write_error(msg)

    def accept_test_batch(self):
        """Accept all files in the current test batch"""
        if not self.last_batch:
            self.console.write_warning("No test batch to accept.")
            return
        
        self.console.write_info("Accepting test batch...")
        results = accept_batch(self.last_batch)
        
        for success, msg in results:
            if success:
                self.console.write_success(msg)
            else:
                self.console.write_error(msg)

    def get_batch_info(self):
        """Get information about the current batch"""
        return {
            'batch_size': len(self.last_batch),
            'files': [target for (_, target) in self.last_batch]
        }