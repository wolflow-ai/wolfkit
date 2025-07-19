# ui/file_size_settings.py
"""
File Size Settings Module for Code Review Tab
Handles file size analysis configuration, thresholds, and quick size checks
"""
import os
import tkinter as tk
from typing import Optional, Dict, Any, List
from ttkbootstrap import Frame, Label, Button, Checkbutton, Combobox, Spinbox, LabelFrame
from ttkbootstrap.constants import *

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


class FileSizeSettings:
    """
    Manages file size analysis settings and quick size check functionality
    """
    
    def __init__(self, parent_tab, code_reviewer):
        """
        Initialize file size settings
        
        Args:
            parent_tab: The parent CodeReviewTab instance
            code_reviewer: CodeReviewer instance for analysis
        """
        self.parent_tab = parent_tab
        self.code_reviewer = code_reviewer
        
        # File size analysis settings
        self.include_file_analysis = tk.BooleanVar(value=True)
        self.file_size_preset = tk.StringVar(value="standard")
        self.custom_optimal = tk.IntVar(value=400)
        self.custom_warning = tk.IntVar(value=800)
        self.custom_critical = tk.IntVar(value=1200)
        
        # UI components (initialized in create_settings_section)
        self.preset_combo: Optional[Combobox] = None
        self.custom_frame: Optional[Frame] = None
        self.optimal_spinbox: Optional[Spinbox] = None
        self.warning_spinbox: Optional[Spinbox] = None
        self.critical_spinbox: Optional[Spinbox] = None
        self.preset_description_label: Optional[Label] = None
        self.quick_size_check_button: Optional[Button] = None
    
    def create_settings_section(self, parent_frame: Frame) -> Optional[LabelFrame]:
        """
        Create file size analysis settings section
        
        Args:
            parent_frame: Parent frame to add settings to
            
        Returns:
            LabelFrame containing settings or None if not available
        """
        if not FILE_METRICS_AVAILABLE:
            return None
        
        size_frame = LabelFrame(parent_frame, text="📏 File Size Analysis Settings")
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
        
        # Use proper Combobox configuration
        self.preset_combo = Combobox(
            preset_frame,
            textvariable=self.file_size_preset,
            values=["strict", "standard", "relaxed", "legacy", "custom"],
            state="readonly",
            width=12
        )
        self.preset_combo.pack(side=LEFT, padx=(0, 15))
        
        # Bind to the proper event
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
        
        return size_frame
    
    def add_quick_size_check_button(self, parent_frame: Frame) -> Optional[Button]:
        """
        Add quick file size check button to controls frame
        
        Args:
            parent_frame: Parent frame for the button
            
        Returns:
            Button widget or None if not available
        """
        if not FILE_METRICS_AVAILABLE:
            return None
        
        self.quick_size_check_button = Button(
            parent_frame,
            text="📏 Quick Size Check",
            bootstyle="info-outline",
            command=self.run_quick_size_check
        )
        self.quick_size_check_button.pack(side=LEFT, padx=(0, 10))
        return self.quick_size_check_button
    
    def _on_file_analysis_toggled(self):
        """Handle file analysis enable/disable"""
        if not FILE_METRICS_AVAILABLE:
            return
            
        enabled = self.include_file_analysis.get()
        
        # Enable/disable file size controls
        state = "normal" if enabled else "disabled"
        if self.preset_combo:
            self.preset_combo.config(state="readonly" if enabled else "disabled")
        
        for widget in [self.optimal_spinbox, self.warning_spinbox, self.critical_spinbox]:
            if widget:
                widget.config(state=state)
        
        # Update quick size check button
        if self.quick_size_check_button and enabled:
            scope = self.parent_tab.analysis_scope.get()
            if scope != "single":
                self.quick_size_check_button.config(state="normal")
        elif self.quick_size_check_button:
            self.quick_size_check_button.config(state="disabled")
        
        # Update code reviewer settings
        self._update_code_reviewer_settings()

    def _on_preset_changed(self, event=None):
        """Handle file size preset change"""
        if not FILE_METRICS_AVAILABLE:
            return
            
        preset = self.file_size_preset.get()
        
        # Show/hide custom controls
        if preset == "custom" and self.custom_frame:
            self.custom_frame.pack(side=LEFT, padx=(10, 0))
        elif self.custom_frame:
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
        
        if self.preset_description_label:
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

    def show_file_size_preview(self, file_paths: List[str]):
        """Show quick file size preview for selected files"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get() or len(file_paths) > 10:
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
            
            console = self.parent_tab.analysis_console
            
            if metrics.problematic_files:
                console.write_warning(f"⚠️ {len(metrics.problematic_files)} files exceed size thresholds:")
                for file_metrics in metrics.problematic_files[:3]:  # Show top 3
                    severity_icon = "🚨" if file_metrics.size_category.value == "dangerous" else "⚠️"
                    console.write_warning(
                        f"  {severity_icon} {os.path.basename(file_metrics.file_path)}: {file_metrics.line_count} lines",
                        include_timestamp=False
                    )
            else:
                console.write_success("✅ All selected files are within size thresholds")
                
        except Exception as e:
            console = self.parent_tab.analysis_console
            console.write_error(f"Could not analyze file sizes: {str(e)}")

    def run_quick_size_check(self):
        """Run quick file size check without full AI analysis"""
        if not FILE_METRICS_AVAILABLE:
            console = self.parent_tab.analysis_console
            console.write_error("❌ File size analysis not available. Missing file_metrics_analyzer module.")
            return
        
        scope = self.parent_tab.analysis_scope.get()
        
        if scope == "project" and self.parent_tab.selected_project_directory:
            self._run_quick_project_size_check()
        elif scope in ["single", "module"] and self.parent_tab.selected_analysis_files:
            self._run_quick_files_size_check()
        else:
            console = self.parent_tab.analysis_console
            console.write_error("❌ No files or project selected for size check.")

    def _run_quick_project_size_check(self):
        """Run quick size check for entire project"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get():
            console = self.parent_tab.analysis_console
            console.write_warning("File size analysis is disabled. Enable it in settings to use this feature.")
            return
        
        console = self.parent_tab.analysis_console
        console.write_info("🔍 Running quick file size check for project...")
        
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
            
            metrics = analyzer.analyze_project(self.parent_tab.selected_project_directory)
            
            # Display results
            from file_metrics_analyzer import format_file_size_summary
            summary = format_file_size_summary(metrics)
            
            console.write_success("📊 Quick File Size Check Complete!")
            self._display_size_check_results(summary)
            
        except Exception as e:
            console.write_error(f"❌ Quick size check failed: {str(e)}")

    def _run_quick_files_size_check(self):
        """Run quick size check for selected files"""
        if not FILE_METRICS_AVAILABLE or not self.include_file_analysis.get():
            console = self.parent_tab.analysis_console
            console.write_warning("File size analysis is disabled. Enable it in settings to use this feature.")
            return
        
        console = self.parent_tab.analysis_console
        console.write_info(f"🔍 Running quick file size check for {len(self.parent_tab.selected_analysis_files)} files...")
        
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
            
            metrics = analyzer.analyze_files(self.parent_tab.selected_analysis_files)
            
            # Display results
            from file_metrics_analyzer import format_file_size_summary
            summary = format_file_size_summary(metrics)
            
            console.write_success("📊 Quick File Size Check Complete!")
            self._display_size_check_results(summary)
            
        except Exception as e:
            console.write_error(f"❌ Quick size check failed: {str(e)}")

    def _display_size_check_results(self, summary: str):
        """Display formatted size check results in console"""
        console = self.parent_tab.analysis_console
        
        for line in summary.split('\n'):
            if line.strip():
                if '🚨' in line or 'DANGEROUS' in line:
                    console.write_error(line, include_timestamp=False)
                elif '🔥' in line or 'CRITICAL' in line:
                    console.write_warning(line, include_timestamp=False)
                elif '⚠️' in line or 'WARNING' in line:
                    console.write_warning(line, include_timestamp=False)
                elif '✅' in line or '📈' in line or '💡' in line:
                    console.write_success(line, include_timestamp=False)
                else:
                    console.write_info(line, include_timestamp=False)

    def update_button_state_for_scope(self, scope: str):
        """Update quick size check button state based on analysis scope"""
        if not FILE_METRICS_AVAILABLE or not self.quick_size_check_button:
            return
        
        enabled = self.include_file_analysis.get()
        
        if enabled and scope != "single":
            self.quick_size_check_button.config(state="normal")
        else:
            self.quick_size_check_button.config(state="disabled")

    def get_settings_info(self) -> Dict[str, Any]:
        """Get current file size settings information"""
        return {
            'file_size_analysis_available': FILE_METRICS_AVAILABLE,
            'file_size_analysis_enabled': FILE_METRICS_AVAILABLE and self.include_file_analysis.get(),
            'file_size_preset': self.file_size_preset.get() if FILE_METRICS_AVAILABLE else 'N/A',
            'optimal_threshold': self.custom_optimal.get() if FILE_METRICS_AVAILABLE else 0,
            'warning_threshold': self.custom_warning.get() if FILE_METRICS_AVAILABLE else 0,
            'critical_threshold': self.custom_critical.get() if FILE_METRICS_AVAILABLE else 0
        }