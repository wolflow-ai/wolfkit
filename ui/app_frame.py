# ui\app_frame.py ===
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar, Radiobutton, Notebook, Style, Progressbar, Spinbox
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
from document_merger import check_document_merger_config, analyze_documents_in_folder, get_supported_document_types
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
        
        # Document merge variables
        self.selected_document_folder = None
        self.num_clusters = tk.IntVar(value=3)
        self.last_merge_report_path = None

        # Configure custom tab styling
        self._configure_tab_styling()

        # Create main notebook for tabs (using default style)
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=YES)

        # Create main workflow tab
        self.main_tab = Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main Workflow")

        # Create code review tab
        self.review_tab = Frame(self.notebook)
        self.notebook.add(self.review_tab, text="Code Review")
        
        # Create document merge tab
        self.merge_tab = Frame(self.notebook)
        self.notebook.add(self.merge_tab, text="Document Merge")

        self._setup_main_tab()
        self._setup_review_tab()
        self._setup_merge_tab()

    def _configure_tab_styling(self):
        """Configure custom styling for notebook tabs to show active/inactive states"""
        style = Style()
        
        # Get the current theme colors
        theme_colors = style.colors
        
        # Set the base configuration for default tab appearance
        style.configure(
            "TNotebook.Tab",
            background=theme_colors.light,
            foreground=theme_colors.secondary,
            padding=[12, 8],
            font=("TkDefaultFont", 10)
        )
        
        # Map the state-based color changes
        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", theme_colors.primary),
                ("active", theme_colors.info),
                ("", theme_colors.light)  # Use empty state instead of "!selected"
            ],
            foreground=[
                ("selected", "white"),
                ("active", theme_colors.dark),
                ("", theme_colors.secondary)  # Use empty state instead of "!selected"
            ]
        )

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
        """Setup the code review tab (existing functionality)"""
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
        self.check_config_btn.pack(side=LEFT, padx=(0, 10))

        self.clear_selection_btn = Button(file_buttons_frame, text="Clear Selection", bootstyle="secondary-outline", command=self.clear_file_selection)
        self.clear_selection_btn.pack(side=LEFT)

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

    def _setup_merge_tab(self):
        """Setup the document merge tab (new functionality)"""
        # Header info
        merge_header_frame = Frame(self.merge_tab)
        merge_header_frame.pack(fill=X, pady=(0, 10))

        merge_title = Label(merge_header_frame, text="📄 Document Clustering & Merge", font=("TkDefaultFont", 12, "bold"))
        merge_title.pack(anchor="w")

        merge_subtitle = Label(merge_header_frame, text="Semantically cluster and merge related documents using AI", font=("TkDefaultFont", 9))
        merge_subtitle.pack(anchor="w")

        # Supported formats info
        formats_text = f"Supported: {', '.join(get_supported_document_types())}"
        formats_label = Label(merge_header_frame, text=formats_text, font=("TkDefaultFont", 8), foreground="gray")
        formats_label.pack(anchor="w")

        # Folder selection section
        folder_section = Frame(self.merge_tab)
        folder_section.pack(fill=X, pady=(0, 10))

        folder_buttons_frame = Frame(folder_section)
        folder_buttons_frame.pack(fill=X, pady=(0, 5))

        self.select_document_folder_btn = Button(folder_buttons_frame, text="Select Document Folder", command=self.select_document_folder)
        self.select_document_folder_btn.pack(side=LEFT, padx=(0, 10))

        self.check_merge_config_btn = Button(folder_buttons_frame, text="Check Configuration", bootstyle="info-outline", command=self.check_merge_config)
        self.check_merge_config_btn.pack(side=LEFT, padx=(0, 10))

        self.clear_folder_btn = Button(folder_buttons_frame, text="Clear Folder", bootstyle="secondary-outline", command=self.clear_document_folder)
        self.clear_folder_btn.pack(side=LEFT)

        self.document_folder_label = Label(folder_section, text="No document folder selected", anchor="w")
        self.document_folder_label.pack(fill=X)

        # Clustering settings
        settings_frame = Frame(self.merge_tab)
        settings_frame.pack(fill=X, pady=(0, 10))

        Label(settings_frame, text="Number of clusters:").pack(side=LEFT)
        self.cluster_spinbox = Spinbox(settings_frame, from_=2, to=20, textvariable=self.num_clusters, width=5)
        self.cluster_spinbox.pack(side=LEFT, padx=(5, 10))

        auto_clusters_btn = Button(settings_frame, text="Auto", bootstyle="secondary-outline", command=self.auto_detect_clusters)
        auto_clusters_btn.pack(side=LEFT)

        # Analysis controls
        merge_controls_frame = Frame(self.merge_tab)
        merge_controls_frame.pack(fill=X, pady=(0, 10))

        self.analyze_documents_button = Button(merge_controls_frame, text="🔍 Analyze Documents", bootstyle="primary", command=self.analyze_documents)
        self.analyze_documents_button.pack(side=LEFT, padx=(0, 10))

        self.open_merge_report_button = Button(merge_controls_frame, text="📄 Open Last Report", bootstyle="success-outline", command=self.open_last_merge_report)
        self.open_merge_report_button.pack(side=LEFT, padx=(0, 10))
        self.open_merge_report_button.config(state="disabled")

        self.clear_merge_output_button = Button(merge_controls_frame, text="Clear Output", bootstyle="secondary", command=self.clear_merge_output)
        self.clear_merge_output_button.pack(side=LEFT)

        # Progress bar for long operations
        self.merge_progress = Progressbar(self.merge_tab, mode='indeterminate')
        self.merge_progress.pack(fill=X, pady=(0, 10))

        # Analysis output
        merge_output_label = Label(self.merge_tab, text="Analysis Output:")
        merge_output_label.pack(anchor="w", pady=(10, 0))

        merge_frame = Frame(self.merge_tab)
        merge_frame.pack(fill=BOTH, expand=YES)

        self.merge_text = Text(merge_frame, wrap="word", height=20)
        self.merge_text.pack(side=LEFT, fill=BOTH, expand=YES)

        merge_scrollbar = Scrollbar(merge_frame, command=self.merge_text.yview)
        merge_scrollbar.pack(side=RIGHT, fill=Y)
        self.merge_text.config(yscrollcommand=merge_scrollbar.set)

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

    # === Code Review Tab Methods (existing functionality) ===

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

    def clear_file_selection(self):
        """Clear the selected files for analysis"""
        self.selected_analysis_files = []
        self.analysis_files_label.config(text="No files selected for analysis")
        self._write_analysis("File selection cleared.")

    def _write_analysis(self, text):
        """Write text to the analysis output area"""
        self.analysis_text.config(state="normal")
        self.analysis_text.insert("end", text + "\n")
        self.analysis_text.see("end")
        self.analysis_text.config(state="disabled")

    # === Document Merge Tab Methods (new functionality) ===

    def select_document_folder(self):
        """Select folder containing documents to analyze"""
        folder_path = filedialog.askdirectory(title="Select Folder with Documents to Cluster")
        if folder_path:
            self.selected_document_folder = folder_path
            folder_name = os.path.basename(folder_path)
            self.document_folder_label.config(text=f"Selected: {folder_name} ({folder_path})")
            self._write_merge(f"Selected document folder: {folder_path}")
        else:
            self._write_merge("No folder selected.")

    def check_merge_config(self):
        """Check if document merger is properly configured"""
        success, message = check_document_merger_config()
        self._write_merge("Configuration Check:")
        self._write_merge(message)
        
        if success:
            self._write_merge("✅ Ready to analyze documents!")
        else:
            self._write_merge("❌ Configuration issues found. Please check your .env file and dependencies.")

    def clear_document_folder(self):
        """Clear the selected document folder"""
        self.selected_document_folder = None
        self.document_folder_label.config(text="No document folder selected")
        self._write_merge("Document folder selection cleared.")

    def auto_detect_clusters(self):
        """Automatically detect optimal number of clusters"""
        self.num_clusters.set(0)  # 0 means auto-detect
        self._write_merge("Set to auto-detect optimal number of clusters.")

    def analyze_documents(self):
        """Analyze and cluster documents in the selected folder"""
        if not self.selected_document_folder:
            self._write_merge("❌ No document folder selected. Please select a folder first.")
            return

        self._write_merge("🔍 Starting document analysis and clustering...")
        self._write_merge(f"Scanning folder: {self.selected_document_folder}")

        # Show progress and disable button
        self.merge_progress.start()
        self.analyze_documents_button.config(state="disabled", text="Analyzing...")

        # Use after to run analysis in background (pseudo-threading for demo)
        self.after(100, self._run_document_analysis)

    def _run_document_analysis(self):
        """Run the actual document analysis"""
        try:
            num_clusters = self.num_clusters.get() if self.num_clusters.get() > 0 else None
            
            success, report_path, message = analyze_documents_in_folder(
                self.selected_document_folder, 
                num_clusters
            )
            
            if success:
                self.last_merge_report_path = report_path
                self.open_merge_report_button.config(state="normal")
                self._write_merge(f"✅ {message}")
                self._write_merge(f"📄 Report saved to: {report_path}")
                self._write_merge("Click 'Open Last Report' to view the clustering analysis.")
            else:
                self._write_merge(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            self._write_merge(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable the analyze button and stop progress
            self.merge_progress.stop()
            self.analyze_documents_button.config(state="normal", text="🔍 Analyze Documents")

    def open_last_merge_report(self):
        """Open the last generated merge analysis report"""
        if not self.last_merge_report_path or not os.path.exists(self.last_merge_report_path):
            self._write_merge("❌ No report available to open.")
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(self.last_merge_report_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', self.last_merge_report_path])
            else:
                subprocess.run(['xdg-open', self.last_merge_report_path])
            
            self._write_merge(f"📄 Opened report: {os.path.basename(self.last_merge_report_path)}")
        except Exception as e:
            # Fallback: try to open with webbrowser
            try:
                webbrowser.open(f"file://{os.path.abspath(self.last_merge_report_path)}")
                self._write_merge(f"📄 Opened report in browser: {os.path.basename(self.last_merge_report_path)}")
            except Exception as e2:
                self._write_merge(f"❌ Failed to open report: {str(e2)}")

    def clear_merge_output(self):
        """Clear the merge analysis output text area"""
        self.merge_text.config(state="normal")
        self.merge_text.delete("1.0", "end")
        self.merge_text.config(state="disabled")

    def _write_merge(self, text):
        """Write text to the merge analysis output area"""
        self.merge_text.config(state="normal")
        self.merge_text.insert("end", text + "\n")
        self.merge_text.see("end")
        self.merge_text.config(state="disabled")