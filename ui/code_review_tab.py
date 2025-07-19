# ui/code_review_tab.py (Refactored - Slimmed UI Orchestration)
"""
CodeReviewTab - UI orchestration for code review functionality
Coordinates between file size settings and analysis controller modules
"""
import os
import tkinter as tk
from typing import Dict, Any
from ttkbootstrap import Frame, Label, Button, Radiobutton, LabelFrame
from ttkbootstrap.constants import *

from ui.base_tab import BaseTab
from ui.file_size_settings import FileSizeSettings
from ui.analysis_controller import AnalysisController


class CodeReviewTab(BaseTab):
    """Code review tab with clean UI orchestration"""
    
    def __init__(self, parent, **kwargs):
        """Initialize CodeReviewTab with modular components"""
        # Analysis scope selection
        self.analysis_scope = tk.StringVar(value="single")
        
        # UI components (initialized in setup_tab)
        self.selection_label = None
        self.analyze_button = None
        self.open_report_button = None
        self.analysis_info_label = None
        self.analysis_console = None
        
        # Initialize modular components (will be set in setup_tab)
        self.file_size_settings = None
        self.analysis_controller = None
        
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the code review tab UI with modular components"""
        # Initialize controller first
        self.analysis_controller = AnalysisController(self)
        
        # Initialize file size settings with controller's code reviewer
        self.file_size_settings = FileSizeSettings(self, self.analysis_controller.code_reviewer)
        
        # Header section
        self._create_header_section()
        
        # Analysis scope selection
        self._create_analysis_scope_section()

        # File size analysis settings (only if available)
        self.file_size_settings.create_settings_section(self)

        # File/Project selection section
        self._create_selection_section()

        # Analysis controls
        self._create_analysis_controls_section()

        # Analysis output console
        self.analysis_console = self.create_console_section("Analysis Output:", height=20)
        self.analysis_console.pack(fill=BOTH, expand=YES, pady=(10, 0))

        # Initialize capability check
        self._check_initial_capabilities()

    def _create_header_section(self):
        """Create header section with title and description"""
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
            command=self.analysis_controller.select_analysis_files
        )
        self.select_files_btn.pack(side=LEFT, padx=(0, 10))

        self.select_project_btn = Button(
            selection_buttons_frame, 
            text="Select Project Directory", 
            command=self.analysis_controller.select_project_directory
        )
        self.select_project_btn.pack(side=LEFT, padx=(0, 10))

        clear_btn = Button(
            selection_buttons_frame, 
            text="Clear Selection", 
            bootstyle="secondary-outline", 
            command=self.analysis_controller.clear_selection
        )
        clear_btn.pack(side=LEFT, padx=(0, 10))

        check_config_btn = Button(
            selection_buttons_frame, 
            text="Check Configuration", 
            bootstyle="info-outline", 
            command=self.analysis_controller.check_analysis_config
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
            command=self.analysis_controller.run_analysis
        )
        self.analyze_button.pack(side=LEFT, padx=(0, 10))

        self.open_report_button = Button(
            controls_frame, 
            text="📄 Open Last Report", 
            bootstyle="success-outline", 
            command=self.analysis_controller.open_last_report
        )
        self.open_report_button.pack(side=LEFT, padx=(0, 10))
        self.open_report_button.config(state="disabled")

        # Add quick file size check button (only if available)
        self.file_size_settings.add_quick_size_check_button(controls_frame)

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
            self.selection_label.config(text="Select project directory for architectural analysis with file metrics")
        else:
            self.select_files_btn.config(state="normal")
            self.select_project_btn.config(state="disabled")
            if scope == "single":
                self.selection_label.config(text="Select files for individual analysis")
            else:  # module
                self.selection_label.config(text="Select files for module analysis with cross-file context and size metrics")
        
        # Update file size button state
        self.file_size_settings.update_button_state_for_scope(scope)

    def _check_initial_capabilities(self):
        """Check and display initial capabilities including file size analysis"""
        self.analysis_controller.update_analysis_info_display()

    # === Public API for Tab Integration ===

    def get_analysis_info(self) -> Dict[str, Any]:
        """Get information about the current analysis state (for app_frame integration)"""
        return self.analysis_controller.get_analysis_info()
    
    def refresh(self):
        """Refresh tab state (for future extensions)"""
        self.analysis_controller.update_analysis_info_display()
    
    def is_initialized(self) -> bool:
        """Check if tab is fully initialized"""
        return (
            super().is_initialized() and 
            self.analysis_controller is not None and 
            self.file_size_settings is not None
        )

    # === Convenience Properties for Module Integration ===
    
    @property
    def selected_analysis_files(self):
        """Access to selected files for module integration"""
        return self.analysis_controller.selected_analysis_files
    
    @property 
    def selected_project_directory(self):
        """Access to selected project for module integration"""
        return self.analysis_controller.selected_project_directory
    
    # === Direct delegation methods for backward compatibility ===
    
    def select_files(self, title="Select Files", filetypes=None, initial_dir=None):
        """Delegate to BaseTab file selection (used by analysis_controller)"""
        return super().select_files(title, filetypes, initial_dir)
    
    def select_directory(self, title="Select Directory", initial_dir=None):
        """Delegate to BaseTab directory selection (used by analysis_controller)"""
        return super().select_directory(title, initial_dir)
    
    def open_file(self, file_path):
        """Delegate to BaseTab file opening (used by analysis_controller)"""
        return super().open_file(file_path)