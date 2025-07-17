# ui/code_review_tab.py 
"""
Enhanced CodeReviewTab - AI-powered code analysis with multi-file support
Updated to support single-file, module, and project-level analysis
"""
import os
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Radiobutton, LabelFrame
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab

# Import enhanced code reviewer
from code_reviewer import CodeReviewer, AnalysisScope, check_reviewer_config


class CodeReviewTab(BaseTab):
    """Enhanced code review tab with multi-file analysis capabilities"""
    
    def __init__(self, parent, **kwargs):
        """Initialize Enhanced CodeReviewTab"""
        self.selected_analysis_files = []
        self.selected_project_directory = None
        self.last_report_path = None
        
        # Analysis scope selection
        self.analysis_scope = tk.StringVar(value="single")
        
        # Code reviewer instance
        self.code_reviewer = CodeReviewer()
        
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the enhanced code review tab UI"""
        # Header section
        header_frame = Frame(self)
        header_frame.pack(fill=X, pady=(0, 10))

        review_title = Label(
            header_frame, 
            text="🤖 AI Code Review", 
            font=("TkDefaultFont", 12, "bold")
        )
        review_title.pack(anchor="w")

        review_subtitle = Label(
            header_frame, 
            text="Enhanced with multi-file analysis and cross-file context awareness", 
            font=("TkDefaultFont", 9)
        )
        review_subtitle.pack(anchor="w")

        # Analysis scope selection
        self._create_analysis_scope_section()

        # File/Project selection section
        self._create_selection_section()

        # Analysis controls
        self._create_analysis_controls_section()

        # Analysis output console
        self.analysis_console = self.create_console_section("Analysis Output:", height=20)
        self.analysis_console.pack(fill=BOTH, expand=YES, pady=(10, 0))

        # Initialize with capability check
        self._check_capabilities()

    def _create_analysis_scope_section(self):
        """Create analysis scope selection section"""
        scope_frame = LabelFrame(self, text="📊 Analysis Scope")
        scope_frame.pack(fill=X, pady=(0, 10), padx=5)

        scope_inner = Frame(scope_frame)
        scope_inner.pack(fill=X, pady=5, padx=5)

        # Single file analysis
        single_radio = Radiobutton(
            scope_inner,
            text="Single File Analysis",
            variable=self.analysis_scope,
            value="single",
            command=self._on_scope_changed
        )
        single_radio.pack(side=LEFT, padx=(0, 15))

        # Module analysis
        module_radio = Radiobutton(
            scope_inner,
            text="Module Analysis",
            variable=self.analysis_scope,
            value="module",
            command=self._on_scope_changed
        )
        module_radio.pack(side=LEFT, padx=(0, 15))

        # Project analysis
        project_radio = Radiobutton(
            scope_inner,
            text="Project Analysis",
            variable=self.analysis_scope,
            value="project",
            command=self._on_scope_changed
        )
        project_radio.pack(side=LEFT)

        # Description
        desc_text = "Single: Traditional per-file analysis • Module: Cross-file analysis • Project: Architectural review"
        desc_label = Label(
            scope_frame,
            text=desc_text,
            font=("TkDefaultFont", 8),
            foreground="gray",
            wraplength=600
        )
        desc_label.pack(fill=X, padx=5, pady=(0, 5))

    def _create_selection_section(self):
        """Create file/project selection section"""
        selection_frame = LabelFrame(self, text="📁 Selection")
        selection_frame.pack(fill=X, pady=(0, 10), padx=5)

        # Selection buttons
        selection_buttons_frame = Frame(selection_frame)
        selection_buttons_frame.pack(fill=X, pady=5, padx=5)

        self.select_files_btn = Button(
            selection_buttons_frame, 
            text="Select Files to Analyze", 
            command=self.select_analysis_files
        )
        self.select_files_btn.pack(side=LEFT, padx=(0, 10))

        self.select_project_btn = Button(
            selection_buttons_frame, 
            text="Select Project Directory", 
            command=self.select_project_directory
        )
        self.select_project_btn.pack(side=LEFT, padx=(0, 10))

        clear_btn = Button(
            selection_buttons_frame, 
            text="Clear Selection", 
            bootstyle="secondary-outline", 
            command=self.clear_selection
        )
        clear_btn.pack(side=LEFT, padx=(0, 10))

        check_config_btn = Button(
            selection_buttons_frame, 
            text="Check Configuration", 
            bootstyle="info-outline", 
            command=self.check_analysis_config
        )
        check_config_btn.pack(side=LEFT)

        # Selection status
        self.selection_label = Label(
            selection_frame, 
            text="No files or project selected", 
            anchor="w",
            padding=(5, 2)
        )
        self.selection_label.pack(fill=X, padx=5, pady=(0, 5))

    def _create_analysis_controls_section(self):
        """Create analysis controls section"""
        controls_frame = Frame(self)
        controls_frame.pack(fill=X, pady=(0, 10))

        self.analyze_button = Button(
            controls_frame, 
            text="🔍 Analyze Code", 
            bootstyle="primary", 
            command=self.run_analysis
        )
        self.analyze_button.pack(side=LEFT, padx=(0, 10))

        self.open_report_button = Button(
            controls_frame, 
            text="📄 Open Last Report", 
            bootstyle="success-outline", 
            command=self.open_last_report
        )
        self.open_report_button.pack(side=LEFT, padx=(0, 10))
        self.open_report_button.config(state="disabled")

        # Analysis info
        self.analysis_info_label = Label(
            controls_frame,
            text="Ready for analysis",
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.analysis_info_label.pack(side=LEFT, padx=(10, 0))

    def _on_scope_changed(self):
        """Handle analysis scope change"""
        scope = self.analysis_scope.get()
        
        if scope == "project":
            self.select_files_btn.config(state="disabled")
            self.select_project_btn.config(state="normal")
            self.selection_label.config(text="Select project directory for architectural analysis")
        else:
            self.select_files_btn.config(state="normal")
            self.select_project_btn.config(state="disabled")
            if scope == "single":
                self.selection_label.config(text="Select files for individual analysis")
            else:  # module
                self.selection_label.config(text="Select files for module analysis with cross-file context")

    def select_analysis_files(self):
        """Select files for analysis"""
        filetypes = [
            ("All Code Files", "*.py *.js *.ts *.html *.css *.json *.md *.txt"),
            ("Python Files", "*.py"),
            ("JavaScript Files", "*.js"),
            ("TypeScript Files", "*.ts"),
            ("HTML Files", "*.html"),
            ("CSS Files", "*.css"),
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ]
        
        file_paths = self.select_files(
            title="Select Files for AI Analysis",
            filetypes=filetypes
        )
        
        if file_paths:
            self.selected_analysis_files = list(file_paths)
            self.selected_project_directory = None
            
            file_names = [os.path.basename(f) for f in file_paths]
            
            if len(file_names) <= 3:
                files_text = ", ".join(file_names)
            else:
                files_text = f"{', '.join(file_names[:3])} and {len(file_names) - 3} more"
            
            scope = self.analysis_scope.get()
            if scope == "module":
                self.selection_label.config(text=f"Module analysis: {files_text}")
            else:
                self.selection_label.config(text=f"Selected: {files_text}")
            
            self.analysis_console.write_info(f"Selected {len(file_paths)} files for {scope} analysis:")
            for file_path in file_paths:
                self.analysis_console.write_info(f"  • {os.path.basename(file_path)}", include_timestamp=False)
        else:
            self.analysis_console.write_warning("No files selected for analysis.")

    def select_project_directory(self):
        """Select project directory for analysis"""
        directory = self.select_directory(title="Select Project Directory for Analysis")
        
        if directory:
            self.selected_project_directory = directory
            self.selected_analysis_files = []
            
            dir_name = os.path.basename(directory)
            self.selection_label.config(text=f"Project analysis: {dir_name} ({directory})")
            
            self.analysis_console.write_info(f"Selected project directory: {directory}")
            
            # Quick directory analysis
            self._analyze_project_structure(directory)
        else:
            self.analysis_console.write_warning("No project directory selected.")

    def _analyze_project_structure(self, directory):
        """Perform quick analysis of project structure"""
        try:
            # Count files by type
            file_counts = {}
            total_files = 0
            
            for root, dirs, files in os.walk(directory):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if d not in {'node_modules', 'venv', '.git', '__pycache__'}]
                
                for file in files:
                    total_files += 1
                    ext = os.path.splitext(file)[1].lower()
                    file_counts[ext] = file_counts.get(ext, 0) + 1
            
            # Report structure
            self.analysis_console.write_info(f"Project structure analysis:")
            self.analysis_console.write_info(f"  Total files: {total_files}", include_timestamp=False)
            
            # Show top file types
            sorted_types = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:5]:  # Top 5 file types
                ext_display = ext if ext else "(no extension)"
                self.analysis_console.write_info(f"  {ext_display}: {count} files", include_timestamp=False)
            
            # Estimate analysis time
            estimated_time = min(max(total_files // 50, 10), 180)  # 10 seconds to 3 minutes
            self.analysis_console.write_info(f"  Estimated analysis time: ~{estimated_time} seconds")
            
        except Exception as e:
            self.analysis_console.write_error(f"Could not analyze project structure: {str(e)}")

    def clear_selection(self):
        """Clear file/project selection"""
        self.selected_analysis_files = []
        self.selected_project_directory = None
        self.selection_label.config(text="No files or project selected")
        self.analysis_console.write_info("Selection cleared.")

    def check_analysis_config(self):
        """Check if code analysis is properly configured"""
        try:
            success, message = check_reviewer_config()
            self.analysis_console.write_info("Configuration Check:")
            
            if success:
                self.analysis_console.write_success(message)
            else:
                self.analysis_console.write_error(message)
                
            # Also check capabilities
            capabilities = self.code_reviewer.get_analysis_capabilities()
            self.analysis_console.write_info("Analysis Capabilities:")
            
            if capabilities.get('ai_available'):
                self.analysis_console.write_success("  ✅ AI-powered analysis available")
                supported_scopes = capabilities.get('supported_scopes', [])
                self.analysis_console.write_info(f"  Supported scopes: {', '.join(supported_scopes)}")
            else:
                self.analysis_console.write_warning("  ⚠️ AI analysis limited - check API key configuration")
                
        except Exception as e:
            self.analysis_console.write_error(f"Error checking configuration: {str(e)}")

    def run_analysis(self):
        """Run analysis based on selected scope"""
        scope = self.analysis_scope.get()
        
        if scope == "project":
            if not self.selected_project_directory:
                self.analysis_console.write_error("❌ No project directory selected. Please select a project directory first.")
                return
            self._run_project_analysis()
        else:
            if not self.selected_analysis_files:
                self.analysis_console.write_error("❌ No files selected for analysis. Please select files first.")
                return
            self._run_file_analysis()

    def _run_file_analysis(self):
        """Run file-based analysis (single or module)"""
        scope = self.analysis_scope.get()
        scope_enum = AnalysisScope.SINGLE if scope == "single" else AnalysisScope.MODULE
        
        self.analysis_console.write_info(f"🔍 Starting {scope} analysis...")
        self.analysis_console.write_info(f"Analyzing {len(self.selected_analysis_files)} files...")
        
        # Update button state
        self.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            success, report_path, message = self.code_reviewer.analyze_files(
                self.selected_analysis_files, 
                scope_enum
            )
            
            if success:
                self.last_report_path = report_path
                self.open_report_button.config(state="normal")
                self.analysis_console.write_success(f"✅ {message}")
                self.analysis_console.write_success(f"📄 Report saved to: {report_path}")
                self.analysis_console.write_info("Click 'Open Last Report' to view the detailed analysis.")
            else:
                self.analysis_console.write_error(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            self.analysis_console.write_error(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable button
            self.analyze_button.config(state="normal", text="🔍 Analyze Code")

    def _run_project_analysis(self):
        """Run project-level analysis"""
        self.analysis_console.write_info("🔍 Starting project analysis...")
        self.analysis_console.write_info(f"Analyzing project: {self.selected_project_directory}")
        
        # Update button state
        self.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            success, report_path, message = self.code_reviewer.analyze_project(
                self.selected_project_directory
            )
            
            if success:
                self.last_report_path = report_path
                self.open_report_button.config(state="normal")
                self.analysis_console.write_success(f"✅ {message}")
                self.analysis_console.write_success(f"📄 Report saved to: {report_path}")
                self.analysis_console.write_info("Click 'Open Last Report' to view the detailed analysis.")
            else:
                self.analysis_console.write_error(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            self.analysis_console.write_error(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable button
            self.analyze_button.config(state="normal", text="🔍 Analyze Code")

    def open_last_report(self):
        """Open the last generated analysis report"""
        if not self.last_report_path or not os.path.exists(self.last_report_path):
            self.analysis_console.write_error("❌ No report available to open.")
            return

        if self.open_file(self.last_report_path):
            self.analysis_console.write_success(f"📄 Opened report: {os.path.basename(self.last_report_path)}")
        else:
            self.analysis_console.write_error("❌ Failed to open report.")

    def _check_capabilities(self):
        """Check and display initial capabilities"""
        try:
            capabilities = self.code_reviewer.get_analysis_capabilities()
            
            if capabilities.get('ai_available'):
                self.analysis_info_label.config(text="✅ AI analysis ready", foreground="green")
            else:
                self.analysis_info_label.config(text="⚠️ Limited analysis (check API key)", foreground="orange")
            
            # Set initial scope based on capabilities
            if not capabilities.get('ai_available'):
                # Disable multi-file options if AI not available
                pass  # For now, keep all options available
                
        except Exception as e:
            self.analysis_info_label.config(text="❌ Configuration error", foreground="red")

    def get_analysis_info(self):
        """Get information about the current analysis state"""
        scope = self.analysis_scope.get()
        
        if scope == "project":
            return {
                'analysis_scope': scope,
                'selected_project': self.selected_project_directory,
                'has_selection': self.selected_project_directory is not None,
                'has_report': self.last_report_path is not None and os.path.exists(self.last_report_path),
                'report_path': self.last_report_path
            }
        else:
            return {
                'analysis_scope': scope,
                'selected_files': len(self.selected_analysis_files),
                'file_list': [os.path.basename(f) for f in self.selected_analysis_files],
                'has_selection': len(self.selected_analysis_files) > 0,
                'has_report': self.last_report_path is not None and os.path.exists(self.last_report_path),
                'report_path': self.last_report_path
            }