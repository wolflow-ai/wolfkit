# ui/code_review_tab.py (Enhanced with File Size Analysis - FIXED)
"""
Enhanced CodeReviewTab - AI-powered code analysis with integrated file size monitoring
Now includes configurable file size thresholds and explicit problematic file identification
FIXED: Combobox event binding issue
"""
import os
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Radiobutton, LabelFrame, Combobox, Checkbutton, Spinbox
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab

# Import enhanced code reviewer with file size analysis
from code_reviewer import CodeReviewer, AnalysisScope, check_reviewer_config

# Try to import file size thresholds, with graceful fallback
try:
    from file_metrics_analyzer import FileSizeThresholds
    FILE_METRICS_AVAILABLE = True
except ImportError:
    FILE_METRICS_AVAILABLE = False
    # Create a dummy class for fallback
    class FileSizeThresholds:
        PRESETS = {
            "strict": {"optimal": 250, "acceptable": 400, "warning": 500, "critical": 700},
            "standard": {"optimal": 400, "acceptable": 600, "warning": 800, "critical": 1200},
            "relaxed": {"optimal": 600, "acceptable": 800, "warning": 1000, "critical": 1500},
            "legacy": {"optimal": 800, "acceptable": 1200, "warning": 1500, "critical": 2000}
        }


class CodeReviewTab(BaseTab):
    """Enhanced code review tab with comprehensive file size analysis"""
    
    def __init__(self, parent, **kwargs):
        """Initialize Enhanced CodeReviewTab with file size settings"""
        self.selected_analysis_files = []
        self.selected_project_directory = None
        self.last_report_path = None
        
        # Analysis scope selection
        self.analysis_scope = tk.StringVar(value="single")
        
        # NEW: File size analysis settings
        self.include_file_analysis = tk.BooleanVar(value=True)
        self.file_size_preset = tk.StringVar(value="standard")
        self.custom_optimal = tk.IntVar(value=400)
        self.custom_warning = tk.IntVar(value=800)
        self.custom_critical = tk.IntVar(value=1200)
        
        # Code reviewer instance
        self.code_reviewer = CodeReviewer()
        
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the enhanced code review tab UI with file size controls"""
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
            text="Enhanced with multi-file analysis, cross-file context awareness, and file size monitoring", 
            font=("TkDefaultFont", 9)
        )
        review_subtitle.pack(anchor="w")

        # Analysis scope selection
        self._create_analysis_scope_section()

        # NEW: File size analysis settings (only if available)
        if FILE_METRICS_AVAILABLE:
            self._create_file_size_settings_section()

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
        desc_text = "Single: Traditional per-file analysis • Module: Cross-file analysis • Project: Architectural review with file size metrics"
        desc_label = Label(
            scope_frame,
            text=desc_text,
            font=("TkDefaultFont", 8),
            foreground="gray",
            wraplength=600
        )
        desc_label.pack(fill=X, padx=5, pady=(0, 5))

    def _create_file_size_settings_section(self):
        """NEW: Create file size analysis settings section"""
        size_frame = LabelFrame(self, text="📏 File Size Analysis Settings")
        size_frame.pack(fill=X, pady=(0, 10), padx=5)

        # Enable/disable file size analysis
        enable_frame = Frame(size_frame)
        enable_frame.pack(fill=X, pady=5, padx=5)

        enable_check = Checkbutton(
            enable_frame,
            text="Include file size analysis",
            variable=self.include_file_analysis,
            command=self._on_file_analysis_toggled
        )
        enable_check.pack(side=LEFT)

        # Threshold presets
        preset_frame = Frame(size_frame)
        preset_frame.pack(fill=X, pady=(0, 5), padx=5)

        Label(preset_frame, text="Size thresholds:").pack(side=LEFT, padx=(0, 5))
        
        # FIXED: Use proper Combobox configuration
        self.preset_combo = Combobox(
            preset_frame,
            textvariable=self.file_size_preset,
            values=["strict", "standard", "relaxed", "legacy", "custom"],
            state="readonly",
            width=12
        )
        self.preset_combo.pack(side=LEFT, padx=(0, 15))
        
        # FIXED: Bind to the proper event instead of using command parameter
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_changed)

        # Custom threshold inputs (initially hidden)
        self.custom_frame = Frame(preset_frame)
        
        Label(self.custom_frame, text="Optimal:").pack(side=LEFT, padx=(10, 2))
        self.optimal_spinbox = Spinbox(
            self.custom_frame,
            from_=100, to=1000, increment=50,
            textvariable=self.custom_optimal,
            width=6
        )
        self.optimal_spinbox.pack(side=LEFT, padx=(0, 10))
        
        Label(self.custom_frame, text="Warning:").pack(side=LEFT, padx=(0, 2))
        self.warning_spinbox = Spinbox(
            self.custom_frame,
            from_=400, to=2000, increment=100,
            textvariable=self.custom_warning,
            width=6
        )
        self.warning_spinbox.pack(side=LEFT, padx=(0, 10))
        
        Label(self.custom_frame, text="Critical:").pack(side=LEFT, padx=(0, 2))
        self.critical_spinbox = Spinbox(
            self.custom_frame,
            from_=800, to=3000, increment=200,
            textvariable=self.custom_critical,
            width=6
        )
        self.critical_spinbox.pack(side=LEFT)

        # Preset descriptions
        preset_descriptions = {
            "strict": "Optimal ≤250, Warning 500+, Critical 700+ lines",
            "standard": "Optimal ≤400, Warning 800+, Critical 1200+ lines (Recommended)",
            "relaxed": "Optimal ≤600, Warning 1000+, Critical 1500+ lines",
            "legacy": "Optimal ≤800, Warning 1500+, Critical 2000+ lines",
            "custom": "Define your own thresholds"
        }
        
        self.preset_description_label = Label(
            size_frame,
            text=preset_descriptions["standard"],
            font=("TkDefaultFont", 8),
            foreground="gray"
        )
        self.preset_description_label.pack(fill=X, padx=5, pady=(0, 5))

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

        # NEW: Quick file size check button (only if file metrics available)
        if FILE_METRICS_AVAILABLE:
            self.quick_size_check_button = Button(
                controls_frame,
                text="📏 Quick Size Check",
                bootstyle="info-outline",
                command=self.run_quick_size_check
            )
            self.quick_size_check_button.pack(side=LEFT, padx=(0, 10))

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
            if FILE_METRICS_AVAILABLE and hasattr(self, 'quick_size_check_button'):
                self.quick_size_check_button.config(state="normal")
            self.selection_label.config(text="Select project directory for architectural analysis with file metrics")
        else:
            self.select_files_btn.config(state="normal")
            self.select_project_btn.config(state="disabled")
            if scope == "single":
                if FILE_METRICS_AVAILABLE and hasattr(self, 'quick_size_check_button'):
                    self.quick_size_check_button.config(state="disabled")
                self.selection_label.config(text="Select files for individual analysis")
            else:  # module
                if FILE_METRICS_AVAILABLE and hasattr(self, 'quick_size_check_button'):
                    self.quick_size_check_button.config(state="normal")
                self.selection_label.config(text="Select files for module analysis with cross-file context and size metrics")

    def _on_file_analysis_toggled(self):
        """Handle file analysis enable/disable"""
        if not FILE_METRICS_AVAILABLE:
            return
            
        enabled = self.include_file_analysis.get()
        
        # Enable/disable file size controls
        state = "normal" if enabled else "disabled"
        self.preset_combo.config(state="readonly" if enabled else "disabled")
        
        for widget in [self.optimal_spinbox, self.warning_spinbox, self.critical_spinbox]:
            widget.config(state=state)
        
        # Update quick size check button
        if enabled:
            scope = self.analysis_scope.get()
            if scope != "single" and hasattr(self, 'quick_size_check_button'):
                self.quick_size_check_button.config(state="normal")
        else:
            if hasattr(self, 'quick_size_check_button'):
                self.quick_size_check_button.config(state="disabled")
        
        # Update code reviewer settings
        self._update_code_reviewer_settings()

    def _on_preset_changed(self, event=None):
        """Handle file size preset change"""
        if not FILE_METRICS_AVAILABLE:
            return
            
        preset = self.file_size_preset.get()
        
        # Show/hide custom controls
        if preset == "custom":
            self.custom_frame.pack(side=LEFT, padx=(10, 0))
        else:
            self.custom_frame.pack_forget()
            
            # Update threshold values from preset
            if preset in FileSizeThresholds.PRESETS:
                thresholds = FileSizeThresholds.PRESETS[preset]
                self.custom_optimal.set(thresholds["optimal"])
                self.custom_warning.set(thresholds["warning"])
                self.custom_critical.set(thresholds["critical"])
        
        # Update description
        preset_descriptions = {
            "strict": "Optimal ≤250, Warning 500+, Critical 700+ lines",
            "standard": "Optimal ≤400, Warning 800+, Critical 1200+ lines (Recommended)",
            "relaxed": "Optimal ≤600, Warning 1000+, Critical 1500+ lines",
            "legacy": "Optimal ≤800, Warning 1500+, Critical 2000+ lines",
            "custom": "Define your own thresholds"
        }
        
        description = preset_descriptions.get(preset, "Custom thresholds")
        if preset == "custom":
            description += f" (Currently: ≤{self.custom_optimal.get()}, {self.custom_warning.get()}+, {self.custom_critical.get()}+)"
        
        self.preset_description_label.config(text=description)
        
        # Update code reviewer settings
        self._update_code_reviewer_settings()

    def _update_code_reviewer_settings(self):
        """Update code reviewer with current file size settings"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get():
            return
        
        preset = self.file_size_preset.get()
        
        try:
            if preset == "custom":
                custom_thresholds = {
                    "optimal": self.custom_optimal.get(),
                    "acceptable": int(self.custom_optimal.get() * 1.5),  # 50% more than optimal
                    "warning": self.custom_warning.get(),
                    "critical": self.custom_critical.get()
                }
                if hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                    self.code_reviewer.multi_file_analyzer.update_file_size_settings(
                        custom_thresholds=custom_thresholds
                    )
            else:
                if hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                    self.code_reviewer.multi_file_analyzer.update_file_size_settings(preset=preset)
        except Exception as e:
            # Silently handle cases where multi_file_analyzer isn't available yet
            pass

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
            
            # Show file size preview if enabled and available
            if FILE_METRICS_AVAILABLE and self.include_file_analysis.get() and len(file_paths) <= 10:
                self._show_file_size_preview(file_paths)
        else:
            self.analysis_console.write_warning("No files selected for analysis.")

    def _show_file_size_preview(self, file_paths):
        """Show quick file size preview for selected files"""
        if not FILE_METRICS_AVAILABLE:
            return
            
        try:
            from file_metrics_analyzer import FileMetricsAnalyzer
            
            # Create temporary analyzer with current settings
            if self.file_size_preset.get() == "custom":
                from file_metrics_analyzer import FileSizeThresholds
                custom_thresholds = {
                    "optimal": self.custom_optimal.get(),
                    "acceptable": int(self.custom_optimal.get() * 1.5),
                    "warning": self.custom_warning.get(),
                    "critical": self.custom_critical.get()
                }
                thresholds = FileSizeThresholds(custom_thresholds=custom_thresholds)
            else:
                from file_metrics_analyzer import FileSizeThresholds
                thresholds = FileSizeThresholds(preset=self.file_size_preset.get())
            
            analyzer = FileMetricsAnalyzer(thresholds)
            metrics = analyzer.analyze_files(file_paths)
            
            if metrics.problematic_files:
                self.analysis_console.write_warning(f"⚠️ {len(metrics.problematic_files)} files exceed size thresholds:")
                for file_metrics in metrics.problematic_files[:3]:  # Show top 3
                    severity_icon = "🚨" if file_metrics.size_category.value == "dangerous" else "⚠️"
                    self.analysis_console.write_warning(
                        f"  {severity_icon} {os.path.basename(file_metrics.file_path)}: {file_metrics.line_count} lines",
                        include_timestamp=False
                    )
            else:
                self.analysis_console.write_success("✅ All selected files are within size thresholds")
                
        except Exception as e:
            self.analysis_console.write_error(f"Could not analyze file sizes: {str(e)}")

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
        """Perform quick analysis of project structure with file size preview"""
        try:
            # Count files by type
            file_counts = {}
            total_files = 0
            large_files = 0
            
            for root, dirs, files in os.walk(directory):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if d not in {'node_modules', 'venv', '.git', '__pycache__'}]
                
                for file in files:
                    total_files += 1
                    ext = os.path.splitext(file)[1].lower()
                    file_counts[ext] = file_counts.get(ext, 0) + 1
                    
                    # Quick file size check if file analysis enabled
                    if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                line_count = len([line for line in f if line.strip()])
                            if line_count > self.custom_warning.get():
                                large_files += 1
                        except:
                            pass  # Skip files we can't read
            
            # Report structure
            self.analysis_console.write_info(f"Project structure analysis:")
            self.analysis_console.write_info(f"  Total files: {total_files}", include_timestamp=False)
            
            # Show top file types
            sorted_types = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:5]:  # Top 5 file types
                ext_display = ext if ext else "(no extension)"
                self.analysis_console.write_info(f"  {ext_display}: {count} files", include_timestamp=False)
            
            # File size preview
            if FILE_METRICS_AVAILABLE and self.include_file_analysis.get() and large_files > 0:
                self.analysis_console.write_warning(f"  ⚠️ {large_files} files exceed {self.custom_warning.get()} lines")
            
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
                
            # Also check capabilities including file size analysis
            capabilities = self.code_reviewer.get_analysis_capabilities()
            self.analysis_console.write_info("Analysis Capabilities:")
            
            if capabilities.get('ai_available'):
                self.analysis_console.write_success("  ✅ AI-powered analysis available")
                supported_scopes = capabilities.get('supported_scopes', [])
                self.analysis_console.write_info(f"  Supported scopes: {', '.join(supported_scopes)}")
                
                # NEW: File size analysis status (only if available)
                if FILE_METRICS_AVAILABLE and capabilities.get('file_size_analysis'):
                    current_preset = capabilities.get('current_preset', 'unknown')
                    self.analysis_console.write_success(f"  ✅ File size analysis enabled (preset: {current_preset})")
                elif FILE_METRICS_AVAILABLE:
                    self.analysis_console.write_warning("  ⚠️ File size analysis disabled")
                else:
                    self.analysis_console.write_info("  ℹ️ File size analysis not available (missing file_metrics_analyzer)")
            else:
                self.analysis_console.write_warning("  ⚠️ AI analysis limited - check API key configuration")
                
        except Exception as e:
            self.analysis_console.write_error(f"Error checking configuration: {str(e)}")

    def run_quick_size_check(self):
        """NEW: Run quick file size check without full AI analysis"""
        if not FILE_METRICS_AVAILABLE:
            self.analysis_console.write_error("❌ File size analysis not available. Missing file_metrics_analyzer module.")
            return
        
        scope = self.analysis_scope.get()
        
        if scope == "project" and self.selected_project_directory:
            self._run_quick_project_size_check()
        elif scope in ["single", "module"] and self.selected_analysis_files:
            self._run_quick_files_size_check()
        else:
            self.analysis_console.write_error("❌ No files or project selected for size check.")

    def _run_quick_project_size_check(self):
        """Run quick size check for entire project"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get():
            self.analysis_console.write_warning("File size analysis is disabled. Enable it in settings to use this feature.")
            return
        
        self.analysis_console.write_info("🔍 Running quick file size check for project...")
        
        try:
            # Update settings and run analysis
            self._update_code_reviewer_settings()
            
            from file_metrics_analyzer import FileMetricsAnalyzer
            if hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                analyzer = self.code_reviewer.multi_file_analyzer.file_analyzer
            else:
                # Fallback: create analyzer directly
                from file_metrics_analyzer import FileSizeThresholds
                thresholds = FileSizeThresholds(preset=self.file_size_preset.get())
                analyzer = FileMetricsAnalyzer(thresholds)
            
            metrics = analyzer.analyze_project(self.selected_project_directory)
            
            # Display results
            from file_metrics_analyzer import format_file_size_summary
            summary = format_file_size_summary(metrics)
            
            self.analysis_console.write_success("📊 Quick File Size Check Complete!")
            for line in summary.split('\n'):
                if line.strip():
                    if '🚨' in line or 'DANGEROUS' in line:
                        self.analysis_console.write_error(line, include_timestamp=False)
                    elif '🔥' in line or 'CRITICAL' in line:
                        self.analysis_console.write_warning(line, include_timestamp=False)
                    elif '⚠️' in line or 'WARNING' in line:
                        self.analysis_console.write_warning(line, include_timestamp=False)
                    elif '✅' in line or '📈' in line or '💡' in line:
                        self.analysis_console.write_success(line, include_timestamp=False)
                    else:
                        self.analysis_console.write_info(line, include_timestamp=False)
            
        except Exception as e:
            self.analysis_console.write_error(f"❌ Quick size check failed: {str(e)}")

    def _run_quick_files_size_check(self):
        """Run quick size check for selected files"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get():
            self.analysis_console.write_warning("File size analysis is disabled. Enable it in settings to use this feature.")
            return
        
        self.analysis_console.write_info(f"🔍 Running quick file size check for {len(self.selected_analysis_files)} files...")
        
        try:
            # Update settings and run analysis
            self._update_code_reviewer_settings()
            
            from file_metrics_analyzer import FileMetricsAnalyzer
            if hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                analyzer = self.code_reviewer.multi_file_analyzer.file_analyzer
            else:
                # Fallback: create analyzer directly
                from file_metrics_analyzer import FileSizeThresholds
                thresholds = FileSizeThresholds(preset=self.file_size_preset.get())
                analyzer = FileMetricsAnalyzer(thresholds)
            
            metrics = analyzer.analyze_files(self.selected_analysis_files)
            
            # Display results
            from file_metrics_analyzer import format_file_size_summary
            summary = format_file_size_summary(metrics)
            
            self.analysis_console.write_success("📊 Quick File Size Check Complete!")
            for line in summary.split('\n'):
                if line.strip():
                    if '🚨' in line or 'DANGEROUS' in line:
                        self.analysis_console.write_error(line, include_timestamp=False)
                    elif '🔥' in line or 'CRITICAL' in line:
                        self.analysis_console.write_warning(line, include_timestamp=False)
                    elif '⚠️' in line or 'WARNING' in line:
                        self.analysis_console.write_warning(line, include_timestamp=False)
                    elif '✅' in line or '📈' in line or '💡' in line:
                        self.analysis_console.write_success(line, include_timestamp=False)
                    else:
                        self.analysis_console.write_info(line, include_timestamp=False)
            
        except Exception as e:
            self.analysis_console.write_error(f"❌ Quick size check failed: {str(e)}")

    def run_analysis(self):
        """Run analysis based on selected scope with file size integration"""
        scope = self.analysis_scope.get()
        
        # Update file size settings before analysis
        if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
            self._update_code_reviewer_settings()
        
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
        """Run file-based analysis (single or module) with file size integration"""
        scope = self.analysis_scope.get()
        scope_enum = AnalysisScope.SINGLE if scope == "single" else AnalysisScope.MODULE
        
        file_analysis_status = ""
        if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
            file_analysis_status = "with file size analysis"
        else:
            file_analysis_status = "without file size analysis"
            
        self.analysis_console.write_info(f"🔍 Starting {scope} analysis {file_analysis_status}...")
        self.analysis_console.write_info(f"Analyzing {len(self.selected_analysis_files)} files...")
        
        # Update button state
        self.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            # Configure code reviewer for this analysis
            if FILE_METRICS_AVAILABLE and hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                self.code_reviewer.multi_file_analyzer.include_file_analysis = self.include_file_analysis.get()
            
            success, report_path, message = self.code_reviewer.analyze_files(
                self.selected_analysis_files, 
                scope_enum
            )
            
            if success:
                self.last_report_path = report_path
                self.open_report_button.config(state="normal")
                self.analysis_console.write_success(f"✅ {message}")
                self.analysis_console.write_success(f"📄 Report saved to: {report_path}")
                
                if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
                    self.analysis_console.write_info("📏 File size analysis included in report")
                
                self.analysis_console.write_info("Click 'Open Last Report' to view the detailed analysis.")
            else:
                self.analysis_console.write_error(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            self.analysis_console.write_error(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable button
            self.analyze_button.config(state="normal", text="🔍 Analyze Code")

    def _run_project_analysis(self):
        """Run project-level analysis with comprehensive file size metrics"""
        file_analysis_status = ""
        if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
            file_analysis_status = "with comprehensive file size metrics"
        else:
            file_analysis_status = "without file size analysis"
            
        self.analysis_console.write_info(f"🔍 Starting project analysis {file_analysis_status}...")
        self.analysis_console.write_info(f"Analyzing project: {self.selected_project_directory}")
        
        # Update button state
        self.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            # Configure code reviewer for this analysis
            if FILE_METRICS_AVAILABLE and hasattr(self.code_reviewer, 'multi_file_analyzer') and self.code_reviewer.multi_file_analyzer:
                self.code_reviewer.multi_file_analyzer.include_file_analysis = self.include_file_analysis.get()
            
            success, report_path, message = self.code_reviewer.analyze_project(
                self.selected_project_directory
            )
            
            if success:
                self.last_report_path = report_path
                self.open_report_button.config(state="normal")
                self.analysis_console.write_success(f"✅ {message}")
                self.analysis_console.write_success(f"📄 Report saved to: {report_path}")
                
                if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
                    self.analysis_console.write_info("📏 Comprehensive file size analysis included in report")
                
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
            report_name = os.path.basename(self.last_report_path)
            self.analysis_console.write_success(f"📄 Opened report: {report_name}")
            
            # Show file size highlights if included
            if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
                self.analysis_console.write_info("💡 Look for the 'File Size Analysis' section in the report for detailed metrics")
        else:
            self.analysis_console.write_error("❌ Failed to open report.")

    def _check_capabilities(self):
        """Check and display initial capabilities including file size analysis"""
        try:
            capabilities = self.code_reviewer.get_analysis_capabilities()
            
            if capabilities.get('ai_available'):
                self.analysis_info_label.config(text="✅ AI analysis ready", foreground="green")
            else:
                self.analysis_info_label.config(text="⚠️ Limited analysis (check API key)", foreground="orange")
            
            # Initialize file size settings based on capabilities
            if FILE_METRICS_AVAILABLE and capabilities.get('file_size_analysis'):
                current_preset = capabilities.get('current_preset', 'standard')
                self.file_size_preset.set(current_preset)
                self._on_preset_changed()
            elif not FILE_METRICS_AVAILABLE:
                # Update info label to show file size analysis status
                current_text = self.analysis_info_label.cget("text")
                self.analysis_info_label.config(text=f"{current_text} (file size analysis: not available)")
                
        except Exception as e:
            self.analysis_info_label.config(text="❌ Configuration error", foreground="red")

    def get_analysis_info(self):
        """Get information about the current analysis state including file size settings"""
        scope = self.analysis_scope.get()
        
        base_info = {
            'analysis_scope': scope,
            'has_report': self.last_report_path is not None and os.path.exists(self.last_report_path),
            'report_path': self.last_report_path,
            'file_size_analysis_available': FILE_METRICS_AVAILABLE,
            'file_size_analysis_enabled': FILE_METRICS_AVAILABLE and self.include_file_analysis.get(),
            'file_size_preset': self.file_size_preset.get() if FILE_METRICS_AVAILABLE else 'N/A'
        }
        
        if scope == "project":
            base_info.update({
                'selected_project': self.selected_project_directory,
                'has_selection': self.selected_project_directory is not None
            })
        else:
            base_info.update({
                'selected_files': len(self.selected_analysis_files),
                'file_list': [os.path.basename(f) for f in self.selected_analysis_files],
                'has_selection': len(self.selected_analysis_files) > 0
            })
        
        # Add file size threshold info
        if FILE_METRICS_AVAILABLE and self.include_file_analysis.get():
            base_info.update({
                'optimal_threshold': self.custom_optimal.get(),
                'warning_threshold': self.custom_warning.get(),
                'critical_threshold': self.custom_critical.get()
            })
        
        return base_info
