# ui/code_review_tab.py
"""
CodeReviewTab - AI-powered code analysis functionality
Extracted from app_frame.py as part of Phase 2 refactoring
"""
import os
from ttkbootstrap import Frame, Label, Button
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab
from code_reviewer import analyze_files, check_reviewer_config


class CodeReviewTab(BaseTab):
    """Code review tab for AI-powered code analysis"""
    
    def __init__(self, parent, **kwargs):
        """Initialize CodeReviewTab"""
        self.selected_analysis_files = []
        self.last_report_path = None
        super().__init__(parent, **kwargs)
    
    def setup_tab(self):
        """Setup the code review tab UI"""
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
            text="Analyze code files for common issues before staging", 
            font=("TkDefaultFont", 9)
        )
        review_subtitle.pack(anchor="w")

        # File selection section
        file_section = Frame(self)
        file_section.pack(fill=X, pady=(0, 10))

        # File selection buttons
        file_buttons_frame = Frame(file_section)
        file_buttons_frame.pack(fill=X, pady=(0, 5))

        self.select_analysis_files_btn = Button(
            file_buttons_frame, 
            text="Select Files to Analyze", 
            command=self.select_analysis_files
        )
        self.select_analysis_files_btn.pack(side=LEFT, padx=(0, 10))

        self.check_config_btn = Button(
            file_buttons_frame, 
            text="Check Configuration", 
            bootstyle="info-outline", 
            command=self.check_analysis_config
        )
        self.check_config_btn.pack(side=LEFT, padx=(0, 10))

        self.clear_selection_btn = Button(
            file_buttons_frame, 
            text="Clear Selection", 
            bootstyle="secondary-outline", 
            command=self.clear_file_selection
        )
        self.clear_selection_btn.pack(side=LEFT)

        # File selection status
        self.analysis_files_label = Label(
            file_section, 
            text="No files selected for analysis", 
            anchor="w"
        )
        self.analysis_files_label.pack(fill=X)

        # Analysis controls
        analysis_controls_frame = Frame(self)
        analysis_controls_frame.pack(fill=X, pady=(0, 10))

        self.analyze_button = Button(
            analysis_controls_frame, 
            text="🔍 Analyze Files", 
            bootstyle="primary", 
            command=self.analyze_selected_files
        )
        self.analyze_button.pack(side=LEFT, padx=(0, 10))

        self.open_report_button = Button(
            analysis_controls_frame, 
            text="📄 Open Last Report", 
            bootstyle="success-outline", 
            command=self.open_last_report
        )
        self.open_report_button.pack(side=LEFT, padx=(0, 10))
        self.open_report_button.config(state="disabled")

        # Analysis output console
        self.analysis_console = self.create_console_section("Analysis Output:", height=20)
        self.analysis_console.pack(fill=BOTH, expand=YES, pady=(10, 0))

    def select_analysis_files(self):
        """Select files for AI analysis"""
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
            file_names = [os.path.basename(f) for f in file_paths]
            
            if len(file_names) <= 3:
                files_text = ", ".join(file_names)
            else:
                files_text = f"{', '.join(file_names[:3])} and {len(file_names) - 3} more"
            
            self.analysis_files_label.config(text=f"Selected: {files_text}")
            self.analysis_console.write_info(f"Selected {len(file_paths)} files for analysis:")
            for file_path in file_paths:
                self.analysis_console.write_info(f"  • {os.path.basename(file_path)}", include_timestamp=False)
        else:
            self.analysis_console.write_warning("No files selected for analysis.")

    def check_analysis_config(self):
        """Check if code analysis is properly configured"""
        try:
            success, message = check_reviewer_config()
            self.analysis_console.write_info("Configuration Check:")
            
            if success:
                self.analysis_console.write_success(message)
                self.analysis_console.write_success("✅ Ready to analyze code!")
            else:
                self.analysis_console.write_error(message)
                self.analysis_console.write_error("❌ Configuration issues found. Please check your .env file.")
        except Exception as e:
            self.analysis_console.write_error(f"Error checking configuration: {str(e)}")

    def analyze_selected_files(self):
        """Run AI analysis on selected files"""
        if not self.selected_analysis_files:
            self.analysis_console.write_error("❌ No files selected for analysis. Please select files first.")
            return

        self.analysis_console.write_info("🔍 Starting AI analysis...")
        self.analysis_console.write_info(f"Analyzing {len(self.selected_analysis_files)} files...")

        # Disable the analyze button during processing
        self.analyze_button.config(state="disabled", text="Analyzing...")

        try:
            success, report_path, message = analyze_files(self.selected_analysis_files)
            
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
            # Re-enable the analyze button
            self.analyze_button.config(state="normal", text="🔍 Analyze Files")

    def open_last_report(self):
        """Open the last generated analysis report"""
        if not self.last_report_path or not os.path.exists(self.last_report_path):
            self.analysis_console.write_error("❌ No report available to open.")
            return

        if self.open_file(self.last_report_path):
            self.analysis_console.write_success(f"📄 Opened report: {os.path.basename(self.last_report_path)}")
        else:
            self.analysis_console.write_error("❌ Failed to open report.")

    def clear_file_selection(self):
        """Clear the selected files for analysis"""
        self.selected_analysis_files = []
        self.analysis_files_label.config(text="No files selected for analysis")
        self.analysis_console.write_info("File selection cleared.")

    def get_analysis_info(self):
        """Get information about the current analysis state"""
        return {
            'selected_files': len(self.selected_analysis_files),
            'has_report': self.last_report_path is not None and os.path.exists(self.last_report_path),
            'report_path': self.last_report_path
        }