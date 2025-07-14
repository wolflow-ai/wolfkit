# ui/security_analysis_tab.py
"""
SecurityAnalysisTab - Comprehensive security analysis interface for Wolfkit
Integrates with existing BaseTab architecture and UI patterns
"""
import os
import threading
from typing import Optional, Dict, Any, List
from ttkbootstrap import Frame, Label, Button, Checkbutton, Combobox, LabelFrame
from ttkbootstrap.constants import *
import tkinter as tk

from ui.base_tab import BaseTab


class SecurityAnalysisTab(BaseTab):
    """Security analysis tab for comprehensive codebase security scanning"""
    
    def __init__(self, parent, **kwargs) -> None:
        """Initialize SecurityAnalysisTab"""
        # Analysis state
        self.selected_directory: Optional[str] = None
        self.current_report: Optional[Any] = None  # SecurityReport
        self.analysis_running: bool = False
        
        # Analysis options
        self.include_dependencies = tk.BooleanVar(value=True)
        self.include_config_files = tk.BooleanVar(value=True)
        self.quick_scan = tk.BooleanVar(value=False)
        self.severity_filter = tk.StringVar(value="MEDIUM")
        
        # UI components (initialized in setup_tab)
        self.directory_label: Optional[Label] = None
        self.analyze_button: Optional[Button] = None
        self.export_button: Optional[Button] = None
        self.open_report_button: Optional[Button] = None
        self.progress_tracker: Optional[Any] = None
        self.results_console: Optional[Any] = None
        self.risk_meter: Optional[Any] = None
        
        super().__init__(parent, **kwargs)
    
    def setup_tab(self) -> None:
        """Setup the security analysis tab UI"""
        # Header section
        self._create_header_section()
        
        # Directory selection section
        self._create_directory_selection_section()
        
        # Analysis options section
        self._create_analysis_options_section()
        
        # Progress and status section
        self.progress_tracker = self.create_progress_section()
        self.progress_tracker.pack(fill=X, pady=(0, 10))
        
        # Action buttons section
        self._create_action_buttons_section()
        
        # Results display section
        self._create_results_section()
    
    def _create_header_section(self) -> None:
        """Create the header section with title and description"""
        header_frame = Frame(self)
        header_frame.pack(fill=X, pady=(0, 10))

        title = Label(
            header_frame, 
            text="🛡️ Security Analysis", 
            font=("TkDefaultFont", 12, "bold")
        )
        title.pack(anchor="w")

        subtitle = Label(
            header_frame, 
            text="Comprehensive security vulnerability scanning with OWASP Top 10 analysis", 
            font=("TkDefaultFont", 9)
        )
        subtitle.pack(anchor="w")

        features_text = "Features: Framework detection, injection analysis, cryptographic review, access control audit"
        features_label = Label(
            header_frame, 
            text=features_text, 
            font=("TkDefaultFont", 8), 
            foreground="gray"
        )
        features_label.pack(anchor="w")
    
    def _create_directory_selection_section(self) -> None:
        """Create the directory selection section"""
        dir_frame = LabelFrame(self, text="🗂️ Codebase Selection")
        dir_frame.pack(fill=X, pady=(0, 10), padx=5)

        # Directory selection buttons
        dir_buttons_frame = Frame(dir_frame)
        dir_buttons_frame.pack(fill=X, pady=5, padx=5)

        select_dir_btn = Button(
            dir_buttons_frame, 
            text="Select Codebase Directory", 
            command=self.select_codebase_directory
        )
        select_dir_btn.pack(side=LEFT, padx=(0, 10))

        check_config_btn = Button(
            dir_buttons_frame, 
            text="Check Configuration", 
            bootstyle="info-outline", 
            command=self.check_security_config
        )
        check_config_btn.pack(side=LEFT, padx=(0, 10))

        clear_dir_btn = Button(
            dir_buttons_frame, 
            text="Clear Selection", 
            bootstyle="secondary-outline", 
            command=self.clear_directory_selection
        )
        clear_dir_btn.pack(side=LEFT)

        # Directory status label
        self.directory_label = Label(
            dir_frame, 
            text="No codebase directory selected", 
            anchor="w",
            padding=(5, 2)
        )
        self.directory_label.pack(fill=X, padx=5, pady=(0, 5))
    
    def _create_analysis_options_section(self) -> None:
        """Create the analysis options section"""
        options_frame = LabelFrame(self, text="⚙️ Analysis Options")
        options_frame.pack(fill=X, pady=(0, 10), padx=5)

        # First row of options
        options_row1 = Frame(options_frame)
        options_row1.pack(fill=X, pady=5, padx=5)

        Checkbutton(
            options_row1, 
            text="Include dependencies", 
            variable=self.include_dependencies
        ).pack(side=LEFT, padx=(0, 15))

        Checkbutton(
            options_row1, 
            text="Include config files", 
            variable=self.include_config_files
        ).pack(side=LEFT, padx=(0, 15))

        Checkbutton(
            options_row1, 
            text="Quick scan mode", 
            variable=self.quick_scan
        ).pack(side=LEFT)

        # Second row of options
        options_row2 = Frame(options_frame)
        options_row2.pack(fill=X, pady=(0, 5), padx=5)

        Label(options_row2, text="Minimum severity:").pack(side=LEFT, padx=(0, 5))
        
        severity_combo = Combobox(
            options_row2, 
            textvariable=self.severity_filter,
            values=["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
            state="readonly",
            width=10
        )
        severity_combo.pack(side=LEFT, padx=(0, 15))

        # Help text
        help_text = "Quick scan: Faster analysis with reduced pattern matching. Config files: .env, settings, etc."
        help_label = Label(
            options_frame,
            text=help_text,
            font=("TkDefaultFont", 8),
            foreground="gray",
            wraplength=600
        )
        help_label.pack(fill=X, padx=5, pady=(0, 5))
    
    def _create_action_buttons_section(self) -> None:
        """Create the action buttons section"""
        button_frame = Frame(self)
        button_frame.pack(fill=X, pady=(0, 10))

        self.analyze_button = Button(
            button_frame, 
            text="🔍 Run Security Analysis", 
            bootstyle="primary", 
            command=self.run_security_analysis
        )
        self.analyze_button.pack(side=LEFT, padx=(0, 10))

        self.export_button = Button(
            button_frame, 
            text="📄 Export Report", 
            bootstyle="success-outline", 
            command=self.export_security_report
        )
        self.export_button.pack(side=LEFT, padx=(0, 10))
        self.export_button.config(state="disabled")

        self.open_report_button = Button(
            button_frame, 
            text="📂 Open Report", 
            bootstyle="info-outline", 
            command=self.open_last_report
        )
        self.open_report_button.pack(side=LEFT)
        self.open_report_button.config(state="disabled")
    
    def _create_results_section(self) -> None:
        """Create the results display section"""
        results_frame = LabelFrame(self, text="📊 Analysis Results")
        results_frame.pack(fill=BOTH, expand=YES, pady=(0, 0), padx=5)

        # Risk meter placeholder (will be implemented as custom widget)
        risk_frame = Frame(results_frame)
        risk_frame.pack(fill=X, pady=5, padx=5)

        self.risk_meter = Label(
            risk_frame,
            text="Risk Level: Not analyzed",
            font=("TkDefaultFont", 10, "bold"),
            anchor="center",
            padding=10
        )
        self.risk_meter.pack(fill=X)

        # Results console
        self.results_console = self.create_console_section("Security Analysis Output:", height=18)
        self.results_console.pack(fill=BOTH, expand=YES, pady=(5, 5), padx=5)

        # Initial message
        self.results_console.write_info("Ready to analyze codebase security.")
        self.results_console.write_info("Select a codebase directory and configure options to begin.")
    
    def select_codebase_directory(self) -> None:
        """Handle codebase directory selection"""
        directory = self.select_directory(title="Select Codebase Directory for Security Analysis")
        if directory:
            self.selected_directory = directory
            dir_name = os.path.basename(directory)
            if self.directory_label:
                self.directory_label.config(text=f"Selected: {dir_name} ({directory})")
            
            self.results_console.write_info(f"Selected codebase: {directory}")
            
            # Quick directory analysis
            self._analyze_directory_structure(directory)
        else:
            self.results_console.write_warning("No directory selected.")
    
    def _analyze_directory_structure(self, directory: str) -> None:
        """Perform quick analysis of directory structure"""
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
            self.results_console.write_info(f"Directory structure analysis:")
            self.results_console.write_info(f"  Total files: {total_files}", include_timestamp=False)
            
            # Show top file types
            sorted_types = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:8]:  # Top 8 file types
                ext_display = ext if ext else "(no extension)"
                self.results_console.write_info(f"  {ext_display}: {count} files", include_timestamp=False)
            
            # Estimate analysis time
            estimated_time = min(max(total_files // 100, 5), 120)  # 5 seconds to 2 minutes
            self.results_console.write_info(f"  Estimated analysis time: ~{estimated_time} seconds")
            
        except Exception as e:
            self.results_console.write_error(f"Could not analyze directory structure: {str(e)}")
    
    def check_security_config(self) -> None:
        """Check if security analysis is properly configured"""
        try:
            # Local import to avoid startup dependencies
            from security_analyzer import check_security_analyzer_config
            
            success, message = check_security_analyzer_config()
            
            if success:
                self.results_console.write_success(message)
                self.results_console.write_success("✅ Ready to perform security analysis!")
            else:
                self.results_console.write_error(message)
                self.results_console.write_error("❌ Configuration issues found.")
                
        except ImportError:
            self.results_console.write_error("❌ Security analyzer module not available.")
        except Exception as e:
            self.results_console.write_error(f"Configuration check failed: {str(e)}")
    
    def clear_directory_selection(self) -> None:
        """Clear the selected directory"""
        self.selected_directory = None
        if self.directory_label:
            self.directory_label.config(text="No codebase directory selected")
        self.results_console.write_info("Directory selection cleared.")
    
    def run_security_analysis(self) -> None:
        """Run comprehensive security analysis"""
        if not self.selected_directory:
            self.show_error("Error", "Please select a codebase directory first.")
            return
        
        if self.analysis_running:
            self.show_warning("Analysis Running", "Security analysis is already in progress.")
            return
        
        # Start analysis in background thread
        self.analysis_running = True
        self._update_ui_for_analysis_start()
        
        # Run analysis in background
        threading.Thread(target=self._run_analysis_background, daemon=True).start()
    
    def _update_ui_for_analysis_start(self) -> None:
        """Update UI elements when analysis starts"""
        if self.analyze_button:
            self.analyze_button.config(state="disabled", text="🔍 Analyzing...")
        
        if self.export_button:
            self.export_button.config(state="disabled")
        
        if self.open_report_button:
            self.open_report_button.config(state="disabled")
        
        self.results_console.clear()
        self.results_console.write_info("🛡️ Starting comprehensive security analysis...")
        
        if self.progress_tracker:
            self.progress_tracker.start_progress("Initializing security analysis...")
    
    def _run_analysis_background(self) -> None:
        """Background thread for running security analysis"""
        try:
            # Local imports to avoid startup overhead
            from security_analyzer import CodebaseSecurityAnalyzer
            from security_reporter import SecurityReporter
            
            # Initialize analyzer
            self._update_progress("Initializing analyzer...")
            analyzer = CodebaseSecurityAnalyzer(self.selected_directory)
            
            # Configure analysis options
            if self.quick_scan.get():
                self._update_console("Quick scan mode enabled - reduced pattern matching")
            
            # Run analysis phases
            self._update_progress("Phase 1: Discovering architecture...")
            self._update_console("🔍 Discovering framework and database technologies...")
            
            # This would be the actual analysis call
            # For now, we'll simulate the process
            report = analyzer.analyze()
            
            self.current_report = report
            
            # Generate and display results
            self._update_progress("Generating analysis report...")
            self._display_analysis_results(report)
            
            # Complete
            self._update_progress_complete("✅ Security analysis complete!")
            self.after(0, self._update_ui_for_analysis_complete)
            
        except ImportError as e:
            self._update_console_error(f"❌ Security analyzer not available: {str(e)}")
            self.after(0, self._update_ui_for_analysis_error)
        except Exception as e:
            self._update_console_error(f"❌ Analysis failed: {str(e)}")
            self.after(0, self._update_ui_for_analysis_error)
    
    def _update_progress(self, message: str) -> None:
        """Thread-safe progress update"""
        if self.progress_tracker:
            self.after(0, lambda: self.progress_tracker.update_message(message))
    
    def _update_progress_complete(self, message: str) -> None:
        """Thread-safe progress completion"""
        if self.progress_tracker:
            self.after(0, lambda: self.progress_tracker.stop_progress(message))
    
    def _update_console(self, message: str) -> None:
        """Thread-safe console update"""
        self.after(0, lambda: self.results_console.write_info(message))
    
    def _update_console_error(self, message: str) -> None:
        """Thread-safe console error update"""
        self.after(0, lambda: self.results_console.write_error(message))
    
    def _display_analysis_results(self, report) -> None:
        """Display analysis results in the console"""
        self.after(0, lambda: self._display_results_ui(report))
    
    def _display_results_ui(self, report) -> None:
        """Update UI with analysis results (runs on main thread)"""
        # Update risk meter
        risk_level = self._get_risk_level(report.risk_score)
        risk_color = self._get_risk_color(risk_level)
        
        if self.risk_meter:
            self.risk_meter.config(
                text=f"Risk Level: {risk_level} ({report.risk_score}/100)",
                foreground=risk_color
            )
        
        # Display summary in console
        self.results_console.write_success(f"🛡️ Security Analysis Complete!")
        self.results_console.write_info(f"Framework detected: {report.framework_detected or 'Unknown'}")
        self.results_console.write_info(f"Database detected: {report.database_type or 'Unknown'}")
        self.results_console.write_info(f"Files scanned: {report.total_files_scanned}")
        
        # Summary stats
        stats = report.summary_stats
        self.results_console.write_info(f"Security findings summary:")
        if stats.get('CRITICAL', 0) > 0:
            self.results_console.write_error(f"  🔴 Critical: {stats['CRITICAL']}", include_timestamp=False)
        if stats.get('HIGH', 0) > 0:
            self.results_console.write_warning(f"  🟠 High: {stats['HIGH']}", include_timestamp=False)
        if stats.get('MEDIUM', 0) > 0:
            self.results_console.write_info(f"  🟡 Medium: {stats['MEDIUM']}", include_timestamp=False)
        if stats.get('LOW', 0) > 0:
            self.results_console.write_info(f"  🔵 Low: {stats['LOW']}", include_timestamp=False)
        
        total_findings = stats.get('total', 0)
        if total_findings == 0:
            self.results_console.write_success(f"✅ No security issues found!")
        else:
            self.results_console.write_info(f"Total findings: {total_findings}")
        
        self.results_console.write_info("Click 'Export Report' to generate detailed analysis document.")
    
    def _update_ui_for_analysis_complete(self) -> None:
        """Update UI when analysis completes successfully"""
        self.analysis_running = False
        
        if self.analyze_button:
            self.analyze_button.config(state="normal", text="🔍 Run Security Analysis")
        
        if self.export_button:
            self.export_button.config(state="normal")
        
        if self.open_report_button:
            self.open_report_button.config(state="normal")
    
    def _update_ui_for_analysis_error(self) -> None:
        """Update UI when analysis encounters an error"""
        self.analysis_running = False
        
        if self.analyze_button:
            self.analyze_button.config(state="normal", text="🔍 Run Security Analysis")
        
        if self.progress_tracker:
            self.progress_tracker.stop_progress("❌ Analysis failed")
    
    def export_security_report(self) -> None:
        """Export the security analysis report"""
        if not self.current_report:
            self.show_error("Error", "No analysis report available to export.")
            return
        
        try:
            # Local import to avoid startup overhead
            from security_reporter import SecurityReporter
            
            reporter = SecurityReporter(self.current_report)
            success, file_path, message = reporter.generate_full_report("markdown")
            
            if success:
                self.results_console.write_success(f"📄 {message}")
                self.results_console.write_info(f"Report saved to: {file_path}")
                
                # Offer to open the report
                if self.ask_yes_no("Report Exported", f"{message}\n\nWould you like to open the report?"):
                    self.open_file(file_path)
            else:
                self.results_console.write_error(f"❌ Export failed: {message}")
                
        except ImportError:
            self.show_error("Error", "Security reporter module not available.")
        except Exception as e:
            self.results_console.write_error(f"❌ Export error: {str(e)}")
    
    def open_last_report(self) -> None:
        """Open the most recent security report"""
        try:
            reports_dir = os.path.abspath("./reports")
            if not os.path.exists(reports_dir):
                self.show_error("Error", "No reports directory found.")
                return
            
            # Find most recent security report
            security_reports = [
                f for f in os.listdir(reports_dir) 
                if f.startswith("wolfkit_security_analysis_") and f.endswith(".md")
            ]
            
            if not security_reports:
                self.show_error("Error", "No security reports found.")
                return
            
            # Get most recent report
            latest_report = sorted(security_reports)[-1]
            report_path = os.path.join(reports_dir, latest_report)
            
            if self.open_file(report_path):
                self.results_console.write_success(f"📄 Opened report: {latest_report}")
            else:
                self.results_console.write_error("❌ Failed to open report.")
                
        except Exception as e:
            self.results_console.write_error(f"❌ Error opening report: {str(e)}")
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score >= 70:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level display"""
        colors = {
            "CRITICAL": "#e74c3c",  # Red
            "HIGH": "#f39c12",      # Orange
            "MEDIUM": "#f1c40f",    # Yellow
            "LOW": "#27ae60"        # Green
        }
        return colors.get(risk_level, "#2c3e50")  # Default dark blue
    
    def get_analysis_info(self) -> Dict[str, Any]:
        """Get information about the current analysis state"""
        return {
            'directory_selected': self.selected_directory is not None,
            'directory_path': self.selected_directory or "",
            'analysis_running': self.analysis_running,
            'has_report': self.current_report is not None,
            'quick_scan_enabled': self.quick_scan.get(),
            'severity_filter': self.severity_filter.get()
        }