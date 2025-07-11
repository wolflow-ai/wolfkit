# ui\app_frame.py ===
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar, Radiobutton, Notebook
from ttkbootstrap.constants import *
from controller import (
    stage_file,
    set_project_directory,
    get_project_directory,
    run_project_entry,
    open_static_web_page,
    revert_file,
    accept_file,
    accept_batch,
    revert_batch
)
from code_reviewer import analyze_files, check_reviewer_config
import webbrowser
import subprocess
import sys

class AppFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.last_batch = []
        self.launch_type = tk.StringVar(value="python")
        self.selected_analysis_files = []
        self.last_report_path = None

        # Create main notebook for tabs
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=YES)

        # Create main workflow tab
        self.main_tab = Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main Workflow")

        # Create code review tab
        self.review_tab = Frame(self.notebook)
        self.notebook.add(self.review_tab, text="Code Review")

        self._setup_main_tab()
        self._setup_review_tab()

    def _setup_main_tab(self):
        """Setup the main workflow tab (existing functionality)"""
        self.project_dir_label = Label(self.main_tab, text="📁 No project directory set", anchor="w")
        self.project_dir_label.pack(fill=X, pady=(0, 10))

        top_button_frame = Frame(self.main_tab)
        top_button_frame.pack(fill=X, pady=(0, 10))

        self.set_project_btn = Button(top_button_frame, text="Set Project Directory", command=self.select_project_directory)
        self.set_project_btn.pack(side=LEFT, padx=(0, 10))

        self.select_button = Button(top_button_frame, text="Select File(s) to Test", command=self.select_files)
        self.select_button.pack(side=LEFT)

        launch_mode_frame = Frame(self.main_tab)
        launch_mode_frame.pack(fill=X, pady=(0, 10))
        Label(launch_mode_frame, text="Launch Type:").pack(side=LEFT)
        Radiobutton(launch_mode_frame, text="Python App", variable=self.launch_type, value="python").pack(side=LEFT, padx=(5, 10))
        Radiobutton(launch_mode_frame, text="Static Web Page", variable=self.launch_type, value="web").pack(side=LEFT)

        self.file_label = Label(self.main_tab, text="No files selected", anchor="w")
        self.file_label.pack(fill=X, pady=(0, 10))

        button_frame = Frame(self.main_tab)
        button_frame.pack(fill=X, pady=(0, 10))

        self.run_button = Button(button_frame, text="Run Test", bootstyle="primary", command=self.run_test)
        self.run_button.pack(side=LEFT, padx=5)

        self.revert_button = Button(button_frame, text="Revert Batch", bootstyle="warning", command=self.revert_test_batch)
        self.revert_button.pack(side=LEFT, padx=5)

        self.accept_button = Button(button_frame, text="Accept Batch", bootstyle="success", command=self.accept_test_batch)
        self.accept_button.pack(side=LEFT, padx=5)

        self.clear_console_button = Button(button_frame, text="Clear Console", bootstyle="secondary", command=self.clear_console)
        self.clear_console_button.pack(side=LEFT, padx=5)

        output_label = Label(self.main_tab, text="Console Output:")
        output_label.pack(anchor="w")

        console_frame = Frame(self.main_tab)
        console_frame.pack(fill=BOTH, expand=YES)

        self.console_text = Text(console_frame, wrap="word", height=20)
        self.console_text.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text.config(yscrollcommand=scrollbar.set)

    def _setup_review_tab(self):
        """Setup the code review tab (new functionality)"""
        # Header info
        header_frame = Frame(self.review_tab)
        header_frame.pack(fill=X, pady=(0, 10))

        review_title = Label(header_frame, text="🤖 AI Code Review", font=("TkDefaultFont", 12, "bold"))
        review_title.pack(anchor="w")

        review_subtitle = Label(header_frame, text="Analyze code files for common issues before staging", font=("TkDefaultFont", 9))
        review_subtitle.pack(anchor="w")

        # File selection section
        file_section = Frame(self.review_tab)
        file_section.pack(fill=X, pady=(0, 10))

        file_buttons_frame = Frame(file_section)
        file_buttons_frame.pack(fill=X, pady=(0, 5))

        self.select_analysis_files_btn = Button(file_buttons_frame, text="Select Files to Analyze", command=self.select_analysis_files)
        self.select_analysis_files_btn.pack(side=LEFT, padx=(0, 10))

        self.check_config_btn = Button(file_buttons_frame, text="Check Configuration", bootstyle="info-outline", command=self.check_analysis_config)
        self.check_config_btn.pack(side=LEFT)

        self.analysis_files_label = Label(file_section, text="No files selected for analysis", anchor="w")
        self.analysis_files_label.pack(fill=X)

        # Analysis controls
        analysis_controls_frame = Frame(self.review_tab)
        analysis_controls_frame.pack(fill=X, pady=(0, 10))

        self.analyze_button = Button(analysis_controls_frame, text="🔍 Analyze Files", bootstyle="primary", command=self.analyze_selected_files)
        self.analyze_button.pack(side=LEFT, padx=(0, 10))

        self.open_report_button = Button(analysis_controls_frame, text="📄 Open Last Report", bootstyle="success-outline", command=self.open_last_report)
        self.open_report_button.pack(side=LEFT, padx=(0, 10))
        self.open_report_button.config(state="disabled")

        self.clear_analysis_button = Button(analysis_controls_frame, text="Clear Output", bootstyle="secondary", command=self.clear_analysis_output)
        self.clear_analysis_button.pack(side=LEFT)

        # Analysis output
        analysis_output_label = Label(self.review_tab, text="Analysis Output:")
        analysis_output_label.pack(anchor="w", pady=(10, 0))

        analysis_frame = Frame(self.review_tab)
        analysis_frame.pack(fill=BOTH, expand=YES)

        self.analysis_text = Text(analysis_frame, wrap="word", height=20)
        self.analysis_text.pack(side=LEFT, fill=BOTH, expand=YES)

        analysis_scrollbar = Scrollbar(analysis_frame, command=self.analysis_text.yview)
        analysis_scrollbar.pack(side=RIGHT, fill=Y)
        self.analysis_text.config(yscrollcommand=analysis_scrollbar.set)

    # === Main Tab Methods (existing functionality) ===

    def select_project_directory(self):
        directory = filedialog.askdirectory(title="Select Target Project Directory")
        if directory:
            resolved = set_project_directory(directory)
            self.project_dir_label.config(text=f"📁 Working on: {resolved}")
            self._write_console(f"Set project directory to: {resolved}")

    def select_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Test File(s)")
        if not file_paths:
            self._write_console("No files selected.")
            return

        self.last_batch = []
        self.file_label.config(text=f"Selected: {len(file_paths)} files")

        for path in file_paths:
            filename = os.path.basename(path)
            project_dir = get_project_directory()

            response = messagebox.askyesnocancel("Test File Action", f"Do you want to replace an existing file with {filename}?\n\nYes = Select file to replace\nNo = Add {filename} as new\nCancel = Skip")

            if response is None:
                self._write_console(f"Skipped: {filename}")
                continue
            elif response:
                target_file_path = filedialog.askopenfilename(title=f"Choose file in project to replace with {filename}", initialdir=project_dir)
                if not target_file_path:
                    self._write_console(f"Skipped: {filename}")
                    continue
                target_filename = os.path.relpath(target_file_path, project_dir)
            else:
                dir_path = filedialog.askdirectory(title=f"Select folder to add {filename} in", initialdir=project_dir)
                if not dir_path:
                    self._write_console(f"Skipped: {filename}")
                    continue
                target_filename = os.path.relpath(os.path.join(dir_path, filename), project_dir)

            success, message = stage_file(path, target_filename)
            self._write_console(message)
            if success:
                self.last_batch.append((path, target_filename))

    def run_test(self):
        mode = self.launch_type.get()
        if mode == "python":
            success, message = run_project_entry()
        elif mode == "web":
            success, message = open_static_web_page()
        else:
            success, message = False, "Unknown launch type selected."

        self._write_console(message)

    def revert_test_batch(self):
        if not self.last_batch:
            self._write_console("No test batch to revert.")
            return
        results = revert_batch(self.last_batch)
        for (_, msg) in results:
            self._write_console(msg)

    def accept_test_batch(self):
        if not self.last_batch:
            self._write_console("No test batch to accept.")
            return
        results = accept_batch(self.last_batch)
        for (_, msg) in results:
            self._write_console(msg)

    def _write_console(self, text):
        self.console_text.config(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.config(state="disabled")

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.config(state="disabled")

    # === Code Review Tab Methods (new functionality) ===

    def select_analysis_files(self):
        """Select files for AI analysis"""
        file_paths = filedialog.askopenfilenames(
            title="Select Files for AI Analysis",
            filetypes=[
                ("All Code Files", "*.py *.js *.ts *.html *.css *.json *.md *.txt"),
                ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"),
                ("TypeScript Files", "*.ts"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if file_paths:
            self.selected_analysis_files = list(file_paths)
            file_names = [os.path.basename(f) for f in file_paths]
            if len(file_names) <= 3:
                files_text = ", ".join(file_names)
            else:
                files_text = f"{', '.join(file_names[:3])} and {len(file_names) - 3} more"
            
            self.analysis_files_label.config(text=f"Selected: {files_text}")
            self._write_analysis(f"Selected {len(file_paths)} files for analysis:")
            for file_path in file_paths:
                self._write_analysis(f"  • {os.path.basename(file_path)}")
        else:
            self._write_analysis("No files selected for analysis.")

    def check_analysis_config(self):
        """Check if code analysis is properly configured"""
        success, message = check_reviewer_config()
        self._write_analysis("Configuration Check:")
        self._write_analysis(message)
        
        if success:
            self._write_analysis("✅ Ready to analyze code!")
        else:
            self._write_analysis("❌ Configuration issues found. Please check your .env file.")

    def analyze_selected_files(self):
        """Run AI analysis on selected files"""
        if not self.selected_analysis_files:
            self._write_analysis("❌ No files selected for analysis. Please select files first.")
            return

        self._write_analysis("🔍 Starting AI analysis...")
        self._write_analysis(f"Analyzing {len(self.selected_analysis_files)} files...")

        # Disable the analyze button during processing
        self.analyze_button.config(state="disabled", text="Analyzing...")

        try:
            success, report_path, message = analyze_files(self.selected_analysis_files)
            
            if success:
                self.last_report_path = report_path
                self.open_report_button.config(state="normal")
                self._write_analysis(f"✅ {message}")
                self._write_analysis(f"📄 Report saved to: {report_path}")
                self._write_analysis("Click 'Open Last Report' to view the detailed analysis.")
            else:
                self._write_analysis(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            self._write_analysis(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable the analyze button
            self.analyze_button.config(state="normal", text="🔍 Analyze Files")

    def open_last_report(self):
        """Open the last generated analysis report"""
        if not self.last_report_path or not os.path.exists(self.last_report_path):
            self._write_analysis("❌ No report available to open.")
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(self.last_report_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', self.last_report_path])
            else:
                subprocess.run(['xdg-open', self.last_report_path])
            
            self._write_analysis(f"📄 Opened report: {os.path.basename(self.last_report_path)}")
        except Exception as e:
            # Fallback: try to open with webbrowser
            try:
                webbrowser.open(f"file://{os.path.abspath(self.last_report_path)}")
                self._write_analysis(f"📄 Opened report in browser: {os.path.basename(self.last_report_path)}")
            except Exception as e2:
                self._write_analysis(f"❌ Failed to open report: {str(e2)}")

    def clear_analysis_output(self):
        """Clear the analysis output text area"""
        self.analysis_text.config(state="normal")
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.config(state="disabled")

    def _write_analysis(self, text):
        """Write text to the analysis output area"""
        self.analysis_text.config(state="normal")
        self.analysis_text.insert("end", text + "\n")
        self.analysis_text.see("end")
        self.analysis_text.config(state="disabled")
