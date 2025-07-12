# ui\app_frame.py ===
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar, Radiobutton, Notebook, Style, Progressbar, Spinbox, LabelFrame
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
from document_merger import (
    check_document_merger_config, 
    analyze_documents_in_folder, 
    merge_document_cluster,
    get_supported_document_types,
    DocumentCluster
)
import webbrowser
import subprocess
import sys
from pathlib import Path

class ClusterCard(LabelFrame):
    """Custom widget to display a document cluster with merge options"""
    
    def __init__(self, parent, cluster: DocumentCluster, on_merge_callback, **kwargs):
        super().__init__(parent, text=f"Cluster {cluster.cluster_id + 1}", **kwargs)
        
        self.cluster = cluster
        self.on_merge_callback = on_merge_callback
        self.expanded = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the cluster card UI elements"""
        # Header with similarity score and document count
        header_frame = Frame(self)
        header_frame.pack(fill=X, padx=5, pady=5)
        
        similarity_text = f"{self.cluster.similarity_score:.1%} similar • {len(self.cluster.documents)} documents"
        self.similarity_label = Label(
            header_frame, 
            text=similarity_text, 
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.similarity_label.pack(side=LEFT)
        
        # Suggested merge name
        name_frame = Frame(self)
        name_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        Label(name_frame, text="Suggested name:", font=("TkDefaultFont", 8)).pack(side=LEFT)
        self.name_var = tk.StringVar(value=self.cluster.suggested_merge_name)
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, width=30)
        self.name_entry.pack(side=LEFT, padx=(5, 0))
        
        # Document list (collapsible)
        self.documents_frame = Frame(self)
        self.documents_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        # Show first 3 documents, with option to expand
        docs_to_show = self.cluster.documents[:3]
        remaining_count = len(self.cluster.documents) - 3
        
        for doc in docs_to_show:
            doc_label = Label(
                self.documents_frame, 
                text=f"• {Path(doc).name}", 
                font=("TkDefaultFont", 8),
                anchor="w"
            )
            doc_label.pack(fill=X)
        
        if remaining_count > 0:
            self.expand_button = Button(
                self.documents_frame,
                text=f"+ {remaining_count} more documents",
                bootstyle="link",
                command=self._toggle_documents
            )
            self.expand_button.pack(anchor="w")
            
            # Hidden documents (shown when expanded)
            self.hidden_docs_frame = Frame(self.documents_frame)
            for doc in self.cluster.documents[3:]:
                doc_label = Label(
                    self.hidden_docs_frame,
                    text=f"• {Path(doc).name}",
                    font=("TkDefaultFont", 8),
                    anchor="w"
                )
                doc_label.pack(fill=X)
        
        # Preview section (collapsible)
        preview_frame = Frame(self)
        preview_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        self.preview_button = Button(
            preview_frame,
            text="▼ Show Preview",
            bootstyle="link",
            command=self._toggle_preview
        )
        self.preview_button.pack(anchor="w")
        
        self.preview_text_frame = Frame(preview_frame)
        self.preview_text = Text(
            self.preview_text_frame,
            height=4,
            wrap="word",
            font=("TkDefaultFont", 8),
            state="disabled"
        )
        
        preview_scroll = Scrollbar(self.preview_text_frame, command=self.preview_text.yview)
        self.preview_text.config(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side=LEFT, fill=BOTH, expand=YES)
        preview_scroll.pack(side=RIGHT, fill=Y)
        
        # Load preview content
        self._load_preview()
        
        # Action buttons
        button_frame = Frame(self)
        button_frame.pack(fill=X, padx=5, pady=5)
        
        self.merge_button = Button(
            button_frame,
            text="🔄 Merge This Cluster",
            bootstyle="primary",
            command=self._on_merge_clicked
        )
        self.merge_button.pack(side=LEFT, padx=(0, 5))
        
        self.preview_only_button = Button(
            button_frame,
            text="👁 Preview Only",
            bootstyle="info-outline",
            command=self._on_preview_clicked
        )
        self.preview_only_button.pack(side=LEFT, padx=(0, 5))
        
        self.skip_button = Button(
            button_frame,
            text="❌ Skip",
            bootstyle="secondary-outline",
            command=self._on_skip_clicked
        )
        self.skip_button.pack(side=LEFT)
    
    def _toggle_documents(self):
        """Toggle showing all documents in the cluster"""
        if not self.expanded:
            self.hidden_docs_frame.pack(fill=X, after=self.expand_button)
            self.expand_button.config(text="▲ Show fewer documents")
            self.expanded = True
        else:
            self.hidden_docs_frame.pack_forget()
            remaining_count = len(self.cluster.documents) - 3
            self.expand_button.config(text=f"+ {remaining_count} more documents")
            self.expanded = False
    
    def _toggle_preview(self):
        """Toggle showing the merge preview"""
        if self.preview_text_frame.winfo_viewable():
            self.preview_text_frame.pack_forget()
            self.preview_button.config(text="▼ Show Preview")
        else:
            self.preview_text_frame.pack(fill=BOTH, expand=YES, after=self.preview_button)
            self.preview_button.config(text="▲ Hide Preview")
    
    def _load_preview(self):
        """Load the merge preview into the text widget"""
        if self.cluster.merge_preview:
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", "end")
            
            # Show a truncated version for the card
            preview_content = self.cluster.merge_preview[:1000]
            if len(self.cluster.merge_preview) > 1000:
                preview_content += "\n\n[... Content truncated. Full preview available after merge ...]"
            
            self.preview_text.insert("1.0", preview_content)
            self.preview_text.config(state="disabled")
        else:
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", "Preview will be generated during merge...")
            self.preview_text.config(state="disabled")
    
    def _on_merge_clicked(self):
        """Handle merge button click"""
        custom_name = self.name_var.get()
        self.on_merge_callback(self.cluster, "merge", custom_name)
    
    def _on_preview_clicked(self):
        """Handle preview only button click"""
        self.on_merge_callback(self.cluster, "preview", None)
    
    def _on_skip_clicked(self):
        """Handle skip button click"""
        self.on_merge_callback(self.cluster, "skip", None)

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
        self.current_clusters = []  # Store clusters for UI display

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
        
        # Create documentation tab
        self.docs_tab = Frame(self.notebook)
        self.notebook.add(self.docs_tab, text="Documentation")

        self._setup_main_tab()
        self._setup_review_tab()
        self._setup_merge_tab()
        self._setup_docs_tab()

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
        """Setup the document merge tab with enhanced cluster viewer"""
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
        auto_clusters_btn.pack(side=LEFT, padx=(0, 10))

        self.analyze_documents_button = Button(settings_frame, text="🔍 Analyze Documents", bootstyle="primary", command=self.analyze_documents)
        self.analyze_documents_button.pack(side=LEFT, padx=(10, 0))

        # Progress bar for long operations
        self.merge_progress = Progressbar(self.merge_tab, mode='indeterminate')
        self.merge_progress.pack(fill=X, pady=(0, 10))

        # Cluster results area (scrollable)
        results_label = Label(self.merge_tab, text="Cluster Analysis Results:")
        results_label.pack(anchor="w", pady=(10, 5))

        # Create scrollable frame for cluster cards
        self.clusters_canvas = tk.Canvas(self.merge_tab, height=400)
        self.clusters_scrollbar = Scrollbar(self.merge_tab, orient="vertical", command=self.clusters_canvas.yview)
        self.clusters_scrollable_frame = Frame(self.clusters_canvas)

        self.clusters_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.clusters_canvas.configure(scrollregion=self.clusters_canvas.bbox("all"))
        )

        self.clusters_canvas.create_window((0, 0), window=self.clusters_scrollable_frame, anchor="nw")
        self.clusters_canvas.configure(yscrollcommand=self.clusters_scrollbar.set)

        self.clusters_canvas.pack(side="left", fill="both", expand=True)
        self.clusters_scrollbar.pack(side="right", fill="y")

        # Initially show placeholder
        self.no_clusters_label = Label(
            self.clusters_scrollable_frame, 
            text="No clusters to display. Select a folder and analyze documents to see results here.",
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.no_clusters_label.pack(pady=20)

        # Status area at bottom
        status_frame = Frame(self.merge_tab)
        status_frame.pack(fill=X, pady=(10, 0))

        self.merge_status_label = Label(status_frame, text="Ready to analyze documents.", anchor="w")
        self.merge_status_label.pack(fill=X)

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

    # === Document Merge Tab Methods (enhanced with cluster viewer) ===

    def select_document_folder(self):
        """Select folder containing documents to analyze"""
        folder_path = filedialog.askdirectory(title="Select Folder with Documents to Cluster")
        if folder_path:
            self.selected_document_folder = folder_path
            folder_name = os.path.basename(folder_path)
            self.document_folder_label.config(text=f"Selected: {folder_name} ({folder_path})")
            self._update_merge_status(f"Selected document folder: {folder_path}")
            # Clear any existing clusters
            self._clear_cluster_display()
        else:
            self._update_merge_status("No folder selected.")

    def check_merge_config(self):
        """Check if document merger is properly configured"""
        success, message = check_document_merger_config()
        self._update_merge_status(f"Configuration Check: {message}")

    def clear_document_folder(self):
        """Clear the selected document folder"""
        self.selected_document_folder = None
        self.document_folder_label.config(text="No document folder selected")
        self._update_merge_status("Document folder selection cleared.")
        self._clear_cluster_display()

    def auto_detect_clusters(self):
        """Automatically detect optimal number of clusters"""
        self.num_clusters.set(0)  # 0 means auto-detect
        self._update_merge_status("Set to auto-detect optimal number of clusters.")

    def analyze_documents(self):
        """Analyze and cluster documents in the selected folder"""
        if not self.selected_document_folder:
            self._update_merge_status("❌ No document folder selected. Please select a folder first.")
            return

        self._update_merge_status("🔍 Starting document analysis and clustering...")

        # Show progress and disable button
        self.merge_progress.start()
        self.analyze_documents_button.config(state="disabled", text="Analyzing...")

        # Use after to run analysis in background (pseudo-threading for demo)
        self.after(100, self._run_document_analysis)

    def _run_document_analysis(self):
        """Run the actual document analysis"""
        try:
            num_clusters = self.num_clusters.get() if self.num_clusters.get() > 0 else None
            
            success, clusters, message = analyze_documents_in_folder(
                self.selected_document_folder, 
                num_clusters
            )
            
            if success:
                self.current_clusters = clusters
                self._display_clusters(clusters)
                self._update_merge_status(f"✅ {message}")
            else:
                self._update_merge_status(f"❌ Analysis failed: {message}")
                self._clear_cluster_display()
                
        except Exception as e:
            self._update_merge_status(f"❌ Unexpected error during analysis: {str(e)}")
            self._clear_cluster_display()
        
        finally:
            # Re-enable the analyze button and stop progress
            self.merge_progress.stop()
            self.analyze_documents_button.config(state="normal", text="🔍 Analyze Documents")

    def _display_clusters(self, clusters: list):
        """Display clusters in the scrollable area using cluster cards"""
        # Clear existing display
        self._clear_cluster_display()
        
        if not clusters:
            no_results_label = Label(
                self.clusters_scrollable_frame,
                text="No clusters found. Try adjusting the number of clusters or check document similarity.",
                font=("TkDefaultFont", 9),
                foreground="gray"
            )
            no_results_label.pack(pady=20)
            return
        
        # Create cluster cards
        for i, cluster in enumerate(clusters):
            cluster_card = ClusterCard(
                self.clusters_scrollable_frame,
                cluster,
                self._handle_cluster_action,
                bootstyle="info",
                padding=10
            )
            cluster_card.pack(fill=X, padx=5, pady=5)
        
        # Update scroll region
        self.clusters_scrollable_frame.update_idletasks()
        self.clusters_canvas.configure(scrollregion=self.clusters_canvas.bbox("all"))

    def _clear_cluster_display(self):
        """Clear all cluster cards from display"""
        for widget in self.clusters_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Show placeholder
        self.no_clusters_label = Label(
            self.clusters_scrollable_frame, 
            text="No clusters to display. Select a folder and analyze documents to see results here.",
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.no_clusters_label.pack(pady=20)

    def _handle_cluster_action(self, cluster: DocumentCluster, action: str, custom_name: str):
        """Handle actions from cluster cards"""
        if action == "merge":
            self._perform_cluster_merge(cluster, custom_name)
        elif action == "preview":
            self._show_cluster_preview(cluster)
        elif action == "skip":
            self._update_merge_status(f"Skipped Cluster {cluster.cluster_id + 1}")

    def _perform_cluster_merge(self, cluster: DocumentCluster, custom_name: str):
        """Actually perform the merge operation"""
        # Ask user where to save the merged file
        output_dir = filedialog.askdirectory(
            title="Select Output Directory for Merged File",
            initialdir=self.selected_document_folder
        )
        
        if not output_dir:
            self._update_merge_status("Merge cancelled - no output directory selected.")
            return
        
        try:
            self._update_merge_status(f"Merging Cluster {cluster.cluster_id + 1}...")
            
            success, output_path, message = merge_document_cluster(cluster, output_dir, custom_name)
            
            if success:
                self._update_merge_status(f"✅ {message}")
                # Offer to open the merged file
                if messagebox.askyesno("Merge Complete", f"{message}\n\nWould you like to open the merged file?"):
                    self._open_file(output_path)
            else:
                self._update_merge_status(f"❌ Merge failed: {message}")
                
        except Exception as e:
            self._update_merge_status(f"❌ Error during merge: {str(e)}")

    def _show_cluster_preview(self, cluster: DocumentCluster):
        """Show a detailed preview of the cluster merge in a popup window"""
        preview_window = tk.Toplevel(self)
        preview_window.title(f"Cluster {cluster.cluster_id + 1} Preview")
        preview_window.geometry("800x600")
        
        # Create text widget with scroll
        text_frame = Frame(preview_window)
        text_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        preview_text = Text(text_frame, wrap="word")
        preview_scroll = Scrollbar(text_frame, command=preview_text.yview)
        preview_text.config(yscrollcommand=preview_scroll.set)
        
        preview_text.pack(side=LEFT, fill=BOTH, expand=YES)
        preview_scroll.pack(side=RIGHT, fill=Y)
        
        # Load content
        if cluster.merge_preview:
            preview_text.insert("1.0", cluster.merge_preview)
        else:
            preview_text.insert("1.0", "Preview not available. Try generating the merge first.")
        
        preview_text.config(state="disabled")
        
        # Close button
        Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=5)

    def _open_file(self, file_path: str):
        """Open a file using the system default application"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            # Fallback: try to open with webbrowser
            try:
                webbrowser.open(f"file://{os.path.abspath(file_path)}")
            except Exception:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def _update_merge_status(self, message: str):
        """Update the status label at the bottom of the merge tab"""
        self.merge_status_label.config(text=message)

    def _setup_docs_tab(self):
        """Setup the documentation tab with comprehensive instructions"""
        # Create scrollable text area for documentation
        docs_frame = Frame(self.docs_tab)
        docs_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Quick navigation section
        nav_frame = Frame(docs_frame)
        nav_frame.pack(fill=X, pady=(0, 10))

        nav_title = Label(nav_frame, text="📖 Wolfkit Documentation", font=("TkDefaultFont", 14, "bold"))
        nav_title.pack(anchor="w")

        nav_subtitle = Label(nav_frame, text="Complete guide to using Wolfkit's Try, Test, Trust workflow", font=("TkDefaultFont", 10))
        nav_subtitle.pack(anchor="w", pady=(0, 10))

        # Quick links
        links_frame = Frame(nav_frame)
        links_frame.pack(fill=X, pady=(0, 10))

        Label(links_frame, text="Quick Links:", font=("TkDefaultFont", 10, "bold")).pack(side=LEFT)

        self.jump_main_btn = Button(links_frame, text="Main Workflow", bootstyle="link", command=lambda: self._jump_to_section("main"))
        self.jump_main_btn.pack(side=LEFT, padx=(10, 5))

        self.jump_review_btn = Button(links_frame, text="Code Review", bootstyle="link", command=lambda: self._jump_to_section("review"))
        self.jump_review_btn.pack(side=LEFT, padx=5)

        self.jump_merge_btn = Button(links_frame, text="Document Merge", bootstyle="link", command=lambda: self._jump_to_section("merge"))
        self.jump_merge_btn.pack(side=LEFT, padx=5)

        self.jump_setup_btn = Button(links_frame, text="Setup Guide", bootstyle="link", command=lambda: self._jump_to_section("setup"))
        self.jump_setup_btn.pack(side=LEFT, padx=5)

        # Main documentation text area
        text_frame = Frame(docs_frame)
        text_frame.pack(fill=BOTH, expand=YES)

        self.docs_text = Text(text_frame, wrap="word", font=("TkDefaultFont", 10), state="disabled")
        docs_scrollbar = Scrollbar(text_frame, command=self.docs_text.yview)
        self.docs_text.config(yscrollcommand=docs_scrollbar.set)

        self.docs_text.pack(side=LEFT, fill=BOTH, expand=YES)
        docs_scrollbar.pack(side=RIGHT, fill=Y)

        # Load documentation content
        self._load_documentation()

    def _jump_to_section(self, section: str):
        """Jump to a specific section in the documentation"""
        section_marks = {
            "main": "MAIN_WORKFLOW_SECTION",
            "review": "CODE_REVIEW_SECTION", 
            "merge": "DOCUMENT_MERGE_SECTION",
            "setup": "SETUP_SECTION"
        }
        
        if section in section_marks:
            mark = section_marks[section]
            try:
                self.docs_text.see(mark)
                # Highlight the section briefly
                start_line = self.docs_text.index(f"{mark} linestart")
                end_line = self.docs_text.index(f"{mark} linestart +3l")
                self.docs_text.tag_add("highlight", start_line, end_line)
                self.docs_text.tag_config("highlight", background="yellow")
                self.after(2000, lambda: self.docs_text.tag_delete("highlight"))
            except tk.TclError:
                pass  # Mark not found

    def _load_documentation(self):
        """Load the complete documentation content"""
        docs_content = """🐺 WOLFKIT DOCUMENTATION
================================

Try, Test, Trust - Your AI-Powered Development Workflow

Wolfkit helps developers safely test AI-generated code and intelligently organize documents using a powerful backup/rollback system with AI analysis.

VERSION: v1.2.0+ with Document Merge


📋 TABLE OF CONTENTS
===================

1. SETUP GUIDE - Getting Started
2. MAIN WORKFLOW - Core File Staging 
3. CODE REVIEW - AI-Powered Analysis
4. DOCUMENT MERGE - Intelligent Clustering
5. TROUBLESHOOTING - Common Issues
6. TIPS & BEST PRACTICES


🚀 SETUP GUIDE
===============

INITIAL SETUP:
1. Ensure Python 3.8+ is installed
2. Install dependencies: pip install -r requirements.txt
3. Create .env file in project root
4. Add your OpenAI API key: OPENAI_API_KEY=sk-your-key-here

OPENAI API KEY:
• Get key from: https://platform.openai.com/api-keys
• Required for Code Review and Document Merge features
• Estimated cost: $0.002-0.05 per analysis (very affordable!)

OPTIONAL SETTINGS:
• OPENAI_MODEL=gpt-4o-mini (default, recommended for cost)
• OPENAI_MODEL=gpt-4o (premium quality, 15x more expensive)

VERIFICATION:
• Use "Check Configuration" buttons in Code Review and Document Merge tabs
• Should show ✅ Ready messages when properly configured


📁 MAIN WORKFLOW - Core File Staging
====================================

PURPOSE: Safely test AI-generated files in real projects with instant rollback

WORKFLOW:
1. SET PROJECT DIRECTORY
   • Click "Set Project Directory"
   • Choose your target project folder
   • Wolfkit will work within this directory

2. SELECT TEST FILES
   • Click "Select File(s) to Test"
   • Choose one or more files to test
   • For each file, decide:
     - REPLACE: Choose existing project file to replace
     - ADD NEW: Choose folder to add file to

3. CHOOSE LAUNCH TYPE
   • Python App: Runs main.py in project directory
   • Static Web Page: Opens index.html in browser

4. RUN TEST
   • Click "Run Test" to launch your project
   • Test the new functionality
   • Check console output for any issues

5. DECISION TIME
   • ACCEPT BATCH: Keep all test files, delete backups
   • REVERT BATCH: Restore original files, remove test files

SAFETY FEATURES:
• Automatic backups before any file replacement
• Batch operations (accept/revert multiple files at once)
• Auto-detects project virtual environments
• All operations logged to console

EXAMPLE WORKFLOW:
Project: my-web-app/
Test file: new-component.js
Action: Replace src/components/old-component.js
Result: old-component.js backed up, new-component.js staged
Test: Launch app, verify new component works
Decision: Accept (keep new) or Revert (restore old)


🤖 CODE REVIEW - AI-Powered Analysis  
====================================

PURPOSE: Catch issues in AI-generated code before deployment

WORKFLOW:
1. CONFIGURATION CHECK
   • Click "Check Configuration" to verify OpenAI API setup
   • Must show ✅ Ready before proceeding

2. SELECT FILES FOR ANALYSIS
   • Click "Select Files to Analyze"
   • Choose code files (Python, JavaScript, HTML, CSS, etc.)
   • Supports multiple file selection

3. ANALYZE FILES
   • Click "🔍 Analyze Files"
   • AI will examine code for:
     - Syntax errors
     - Missing imports
     - Logic gaps
     - Undefined functions
     - Best practice violations

4. REVIEW RESULTS
   • Analysis appears in output area
   • Professional markdown report saved to /reports/
   • Click "📄 Open Last Report" to view full analysis

5. TAKE ACTION
   • Fix any issues found
   • Re-analyze if needed
   • Proceed to Main Workflow for staging

SUPPORTED FILE TYPES:
• Python (.py)
• JavaScript (.js), TypeScript (.ts)
• HTML (.html), CSS (.css)
• JSON (.json)
• Markdown (.md), Text (.txt)

COST ESTIMATE:
• ~$0.002-0.005 per file using gpt-4o-mini
• ~100 file analyses = $0.20-0.50
• No subscription required!

BEST PRACTICES:
• Analyze files BEFORE staging them
• Review generated reports for insights
• Use "Clear Selection" to reset between batches
• Keep reports for project documentation


📄 DOCUMENT MERGE - Intelligent Clustering
==========================================

PURPOSE: Automatically cluster and merge related documents using AI

WORKFLOW:
1. CONFIGURATION CHECK
   • Click "Check Configuration" 
   • Verify OpenAI API setup (same as Code Review)

2. SELECT DOCUMENT FOLDER
   • Click "Select Document Folder"
   • Choose folder containing documents to organize
   • Supports: PDF, Word, Text, Markdown, Code files

3. CONFIGURE CLUSTERING
   • Set number of clusters manually (2-20)
   • OR click "Auto" for automatic detection
   • Auto uses smart algorithms to find optimal groupings

4. ANALYZE DOCUMENTS
   • Click "🔍 Analyze Documents"
   • AI will:
     - Extract content from all documents
     - Generate semantic embeddings
     - Cluster similar documents together
     - Create merge previews

5. REVIEW CLUSTER CARDS
   Each cluster shows:
   • Similarity percentage
   • List of documents (expandable)
   • Suggested merge filename (editable)
   • Content preview (expandable)

6. MERGE CLUSTERS
   • Edit merge filename if desired
   • Click "🔄 Merge This Cluster"
   • Choose output directory
   • AI creates merged document
   • Option to open result immediately

CLUSTER CARD ACTIONS:
• 🔄 Merge This Cluster: Perform the merge
• 👁 Preview Only: View full merge content in popup
• ❌ Skip: Ignore this cluster

SUPPORTED FORMATS:
• PDF documents (.pdf)
• Microsoft Word (.docx, .doc)
• Text files (.txt, .md)
• Code files (.py, .js, .html, .css)

AUTO-CLUSTERING LOGIC:
• Analyzes document similarity using AI embeddings
• Calculates optimal cluster count based on content
• May create fewer clusters if documents are very similar
• Minimum 2 clusters, scales with document count

COST ESTIMATE:
• ~$0.01-0.05 per document batch for clustering
• ~$0.02-0.10 per merged document
• Depends on document size and complexity

EXAMPLE SCENARIO:
Folder: "Research Papers" (15 documents)
Result: 3 clusters found
- Cluster 1: "Machine Learning" (6 docs, 82% similar)
- Cluster 2: "Data Analysis" (5 docs, 78% similar)  
- Cluster 3: "Statistics" (4 docs, 85% similar)
Action: Merge each cluster into consolidated papers

USE CASES:
• Consolidate multiple resume versions
• Merge related research papers
• Organize meeting notes by topic
• Combine code documentation
• Clean up duplicate project files


🔧 TROUBLESHOOTING
==================

COMMON ISSUES:

"No OpenAI API key found"
• Create .env file in project root
• Add: OPENAI_API_KEY=your-actual-key
• Restart Wolfkit

"Analysis failed" / "Merge failed"
• Check internet connection
• Verify API key is valid
• Try smaller batch of files
• Check OpenAI API usage limits

"No project directory set"
• Click "Set Project Directory" in Main Workflow
• Choose a valid folder with your project files

"No files selected"
• Use file selection buttons before running operations
• Ensure files exist and are accessible

Virtual Environment Issues
• Wolfkit auto-detects venv in project directory
• Manually activate venv if needed: venv/Scripts/activate
• Check Python path in console output

File Permission Errors
• Ensure Wolfkit has read/write access to project folder
• Run as administrator if needed (Windows)
• Check file locks (close editors/IDEs)

Large Document Processing
• Very large PDFs may timeout
• Break into smaller batches
• Check available system memory

API Rate Limits
• OpenAI has usage limits per minute/day
• Wait a moment and retry
• Consider upgrading API plan for heavy usage


💡 TIPS & BEST PRACTICES
========================

MAIN WORKFLOW TIPS:
• Always set project directory first
• Test with one file before batch operations
• Use descriptive commit messages in git before testing
• Keep console output visible for feedback

CODE REVIEW TIPS:
• Analyze before staging - catch issues early
• Save reports for documentation
• Review AI suggestions carefully
• Use for learning - understand common patterns

DOCUMENT MERGE TIPS:
• Organize files in folders by topic first
• Review cluster suggestions before merging
• Edit merge filenames to be descriptive
• Keep original files as backup

COST OPTIMIZATION:
• Use gpt-4o-mini for most tasks (recommended)
• Batch similar files together
• Review/edit files before AI analysis
• Monitor usage on OpenAI dashboard

WORKFLOW INTEGRATION:
1. Code Review → Find issues
2. Fix issues manually
3. Main Workflow → Stage and test
4. Document Merge → Organize outputs

SAFETY PRACTICES:
• Always backup projects before major changes
• Test in isolated project copies first
• Use version control (git) alongside Wolfkit
• Review all AI-generated content manually

PROJECT ORGANIZATION:
• Keep test files in separate folder
• Use consistent naming conventions
• Document your Wolfkit workflow in README
• Share cluster reports with team

Remember: Wolfkit enhances your workflow but doesn't replace good development practices. Always review AI suggestions and test thoroughly!


🐺 HAPPY CODING WITH WOLFKIT!
=============================

For more information, visit: https://github.com/your-username/wolfkit
Report issues: https://github.com/your-username/wolfkit/issues

"The best code review is the one that happens before you deploy." 🐺

"""

        # Load content and create section marks for navigation
        self.docs_text.config(state="normal")
        self.docs_text.delete("1.0", "end")
        
        lines = docs_content.split('\n')
        for i, line in enumerate(lines):
            if "🚀 SETUP GUIDE" in line:
                self.docs_text.mark_set("SETUP_SECTION", f"{i+1}.0")
            elif "📁 MAIN WORKFLOW" in line:
                self.docs_text.mark_set("MAIN_WORKFLOW_SECTION", f"{i+1}.0")
            elif "🤖 CODE REVIEW" in line:
                self.docs_text.mark_set("CODE_REVIEW_SECTION", f"{i+1}.0")
            elif "📄 DOCUMENT MERGE" in line:
                self.docs_text.mark_set("DOCUMENT_MERGE_SECTION", f"{i+1}.0")
            
            self.docs_text.insert("end", line + "\n")
        
        self.docs_text.config(state="disabled")