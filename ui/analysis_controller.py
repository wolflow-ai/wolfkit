# ui/analysis_controller.py
"""
Analysis Controller Module for Code Review Tab
Handles file/project selection, analysis execution, and business logic coordination
"""
import os
from typing import List, Optional, Dict, Any, Tuple
from code_reviewer import CodeReviewer, AnalysisScope, check_reviewer_config


class AnalysisController:
    """
    Manages analysis execution and business logic for code review
    """
    
    def __init__(self, parent_tab):
        """
        Initialize analysis controller
        
        Args:
            parent_tab: The parent CodeReviewTab instance
        """
        self.parent_tab = parent_tab
        
        # Selection state
        self.selected_analysis_files: List[str] = []
        self.selected_project_directory: Optional[str] = None
        self.last_report_path: Optional[str] = None
        
        # Code reviewer instance
        self.code_reviewer = CodeReviewer()
    
    def select_analysis_files(self) -> bool:
        """
        Handle file selection for analysis
        
        Returns:
            True if files were selected, False otherwise
        """
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
        
        file_paths = self.parent_tab.select_files(
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
            
            scope = self.parent_tab.analysis_scope.get()
            if scope == "module":
                self.parent_tab.selection_label.config(text=f"Module analysis: {files_text}")
            else:
                self.parent_tab.selection_label.config(text=f"Selected: {files_text}")
            
            console = self.parent_tab.analysis_console
            console.write_info(f"Selected {len(file_paths)} files for {scope} analysis:")
            for file_path in file_paths:
                console.write_info(f"  • {os.path.basename(file_path)}", include_timestamp=False)
            
            # Show file size preview if enabled and available
            if hasattr(self.parent_tab, 'file_size_settings') and len(file_paths) <= 10:
                self.parent_tab.file_size_settings.show_file_size_preview(file_paths)
            
            return True
        else:
            self.parent_tab.analysis_console.write_warning("No files selected for analysis.")
            return False

    def select_project_directory(self) -> bool:
        """
        Handle project directory selection
        
        Returns:
            True if directory was selected, False otherwise
        """
        directory = self.parent_tab.select_directory(title="Select Project Directory for Analysis")
        
        if directory:
            self.selected_project_directory = directory
            self.selected_analysis_files = []
            
            dir_name = os.path.basename(directory)
            self.parent_tab.selection_label.config(text=f"Project analysis: {dir_name} ({directory})")
            
            console = self.parent_tab.analysis_console
            console.write_info(f"Selected project directory: {directory}")
            
            # Quick directory analysis
            self._analyze_project_structure(directory)
            return True
        else:
            self.parent_tab.analysis_console.write_warning("No project directory selected.")
            return False

    def _analyze_project_structure(self, directory: str):
        """Perform quick analysis of project structure with file size preview"""
        console = self.parent_tab.analysis_console
        
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
                    if (hasattr(self.parent_tab, 'file_size_settings') and 
                        self.parent_tab.file_size_settings.include_file_analysis.get()):
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                line_count = len([line for line in f if line.strip()])
                            if line_count > self.parent_tab.file_size_settings.custom_warning.get():
                                large_files += 1
                        except:
                            pass  # Skip files we can't read
            
            # Report structure
            console.write_info(f"Project structure analysis:")
            console.write_info(f"  Total files: {total_files}", include_timestamp=False)
            
            # Show top file types
            sorted_types = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:5]:  # Top 5 file types
                ext_display = ext if ext else "(no extension)"
                console.write_info(f"  {ext_display}: {count} files", include_timestamp=False)
            
            # File size preview
            if (hasattr(self.parent_tab, 'file_size_settings') and 
                self.parent_tab.file_size_settings.include_file_analysis.get() and large_files > 0):
                console.write_warning(f"  ⚠️ {large_files} files exceed {self.parent_tab.file_size_settings.custom_warning.get()} lines")
            
            # Estimate analysis time
            estimated_time = min(max(total_files // 50, 10), 180)  # 10 seconds to 3 minutes
            console.write_info(f"  Estimated analysis time: ~{estimated_time} seconds")
            
        except Exception as e:
            console.write_error(f"Could not analyze project structure: {str(e)}")

    def clear_selection(self):
        """Clear file/project selection"""
        self.selected_analysis_files = []
        self.selected_project_directory = None
        self.parent_tab.selection_label.config(text="No files or project selected")
        self.parent_tab.analysis_console.write_info("Selection cleared.")

    def check_analysis_config(self):
        """Check if code analysis is properly configured"""
        console = self.parent_tab.analysis_console
        
        try:
            success, message = check_reviewer_config()
            console.write_info("Configuration Check:")
            
            if success:
                console.write_success(message)
            else:
                console.write_error(message)
                
            # Also check capabilities including file size analysis
            capabilities = self.code_reviewer.get_analysis_capabilities()
            console.write_info("Analysis Capabilities:")
            
            if capabilities.get('ai_available'):
                console.write_success("  ✅ AI-powered analysis available")
                supported_scopes = capabilities.get('supported_scopes', [])
                console.write_info(f"  Supported scopes: {', '.join(supported_scopes)}")
                
                # File size analysis status
                if hasattr(self.parent_tab, 'file_size_settings'):
                    settings_info = self.parent_tab.file_size_settings.get_settings_info()
                    if settings_info['file_size_analysis_available'] and settings_info['file_size_analysis_enabled']:
                        current_preset = settings_info['file_size_preset']
                        console.write_success(f"  ✅ File size analysis enabled (preset: {current_preset})")
                    elif settings_info['file_size_analysis_available']:
                        console.write_warning("  ⚠️ File size analysis disabled")
                    else:
                        console.write_info("  ℹ️ File size analysis not available (missing file_metrics_analyzer)")
            else:
                console.write_warning("  ⚠️ AI analysis limited - check API key configuration")
                
        except Exception as e:
            console.write_error(f"Error checking configuration: {str(e)}")

    def run_analysis(self):
        """Run analysis based on selected scope with file size integration"""
        scope = self.parent_tab.analysis_scope.get()
        
        # Update file size settings before analysis
        if hasattr(self.parent_tab, 'file_size_settings'):
            self.parent_tab.file_size_settings._update_code_reviewer_settings()
        
        if scope == "project":
            if not self.selected_project_directory:
                self.parent_tab.analysis_console.write_error("❌ No project directory selected. Please select a project directory first.")
                return
            self._run_project_analysis()
        else:
            if not self.selected_analysis_files:
                self.parent_tab.analysis_console.write_error("❌ No files selected for analysis. Please select files first.")
                return
            self._run_file_analysis()

    def _run_file_analysis(self):
        """Run file-based analysis (single or module) with file size integration"""
        scope = self.parent_tab.analysis_scope.get()
        scope_enum = AnalysisScope.SINGLE if scope == "single" else AnalysisScope.MODULE
        
        file_analysis_status = ""
        if (hasattr(self.parent_tab, 'file_size_settings') and 
            self.parent_tab.file_size_settings.include_file_analysis.get()):
            file_analysis_status = "with file size analysis"
        else:
            file_analysis_status = "without file size analysis"
            
        console = self.parent_tab.analysis_console
        console.write_info(f"🔍 Starting {scope} analysis {file_analysis_status}...")
        console.write_info(f"Analyzing {len(self.selected_analysis_files)} files...")
        
        # Update button state
        self.parent_tab.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            # Configure code reviewer for this analysis
            if (hasattr(self.code_reviewer, 'multi_file_analyzer') and 
                self.code_reviewer.multi_file_analyzer and
                hasattr(self.parent_tab, 'file_size_settings')):
                self.code_reviewer.multi_file_analyzer.include_file_analysis = (
                    self.parent_tab.file_size_settings.include_file_analysis.get()
                )
            
            success, report_path, message = self.code_reviewer.analyze_files(
                self.selected_analysis_files, 
                scope_enum
            )
            
            if success:
                self.last_report_path = report_path
                self.parent_tab.open_report_button.config(state="normal")
                console.write_success(f"✅ {message}")
                console.write_success(f"📄 Report saved to: {report_path}")
                
                if (hasattr(self.parent_tab, 'file_size_settings') and 
                    self.parent_tab.file_size_settings.include_file_analysis.get()):
                    console.write_info("📏 File size analysis included in report")
                
                console.write_info("Click 'Open Last Report' to view the detailed analysis.")
            else:
                console.write_error(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            console.write_error(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable button
            self.parent_tab.analyze_button.config(state="normal", text="🔍 Analyze Code")

    def _run_project_analysis(self):
        """Run project-level analysis with comprehensive file size metrics"""
        file_analysis_status = ""
        if (hasattr(self.parent_tab, 'file_size_settings') and 
            self.parent_tab.file_size_settings.include_file_analysis.get()):
            file_analysis_status = "with comprehensive file size metrics"
        else:
            file_analysis_status = "without file size analysis"
            
        console = self.parent_tab.analysis_console
        console.write_info(f"🔍 Starting project analysis {file_analysis_status}...")
        console.write_info(f"Analyzing project: {self.selected_project_directory}")
        
        # Update button state
        self.parent_tab.analyze_button.config(state="disabled", text="Analyzing...")
        
        try:
            # Configure code reviewer for this analysis
            if (hasattr(self.code_reviewer, 'multi_file_analyzer') and 
                self.code_reviewer.multi_file_analyzer and
                hasattr(self.parent_tab, 'file_size_settings')):
                self.code_reviewer.multi_file_analyzer.include_file_analysis = (
                    self.parent_tab.file_size_settings.include_file_analysis.get()
                )
            
            success, report_path, message = self.code_reviewer.analyze_project(
                self.selected_project_directory
            )
            
            if success:
                self.last_report_path = report_path
                self.parent_tab.open_report_button.config(state="normal")
                console.write_success(f"✅ {message}")
                console.write_success(f"📄 Report saved to: {report_path}")
                
                if (hasattr(self.parent_tab, 'file_size_settings') and 
                    self.parent_tab.file_size_settings.include_file_analysis.get()):
                    console.write_info("📏 Comprehensive file size analysis included in report")
                
                console.write_info("Click 'Open Last Report' to view the detailed analysis.")
            else:
                console.write_error(f"❌ Analysis failed: {message}")
                
        except Exception as e:
            console.write_error(f"❌ Unexpected error during analysis: {str(e)}")
        
        finally:
            # Re-enable button
            self.parent_tab.analyze_button.config(state="normal", text="🔍 Analyze Code")

    def open_last_report(self) -> bool:
        """
        Open the last generated analysis report
        
        Returns:
            True if report was opened successfully, False otherwise
        """
        if not self.last_report_path or not os.path.exists(self.last_report_path):
            self.parent_tab.analysis_console.write_error("❌ No report available to open.")
            return False

        if self.parent_tab.open_file(self.last_report_path):
            report_name = os.path.basename(self.last_report_path)
            console = self.parent_tab.analysis_console
            console.write_success(f"📄 Opened report: {report_name}")
            
            # Show file size highlights if included
            if (hasattr(self.parent_tab, 'file_size_settings') and 
                self.parent_tab.file_size_settings.include_file_analysis.get()):
                console.write_info("💡 Look for the 'File Size Analysis' section in the report for detailed metrics")
            return True
        else:
            self.parent_tab.analysis_console.write_error("❌ Failed to open report.")
            return False

    def check_capabilities(self) -> Dict[str, Any]:
        """Check and return analysis capabilities including file size analysis"""
        try:
            capabilities = self.code_reviewer.get_analysis_capabilities()
            
            # Add file size analysis capabilities
            if hasattr(self.parent_tab, 'file_size_settings'):
                settings_info = self.parent_tab.file_size_settings.get_settings_info()
                capabilities.update(settings_info)
            else:
                capabilities.update({
                    'file_size_analysis_available': False,
                    'file_size_analysis_enabled': False,
                    'file_size_preset': 'N/A'
                })
            
            return capabilities
                
        except Exception as e:
            return {
                'ai_available': False,
                'error': str(e),
                'file_size_analysis_available': False,
                'file_size_analysis_enabled': False
            }

    def update_analysis_info_display(self):
        """Update the analysis info label based on current capabilities"""
        try:
            capabilities = self.check_capabilities()
            
            if capabilities.get('ai_available'):
                self.parent_tab.analysis_info_label.config(text="✅ AI analysis ready", foreground="green")
            else:
                self.parent_tab.analysis_info_label.config(text="⚠️ Limited analysis (check API key)", foreground="orange")
            
            # Initialize file size settings based on capabilities
            if (hasattr(self.parent_tab, 'file_size_settings') and 
                capabilities.get('file_size_analysis_available')):
                current_preset = capabilities.get('current_preset', 'standard')
                self.parent_tab.file_size_settings.file_size_preset.set(current_preset)
                self.parent_tab.file_size_settings._on_preset_changed()
            elif not capabilities.get('file_size_analysis_available'):
                # Update info label to show file size analysis status
                current_text = self.parent_tab.analysis_info_label.cget("text")
                self.parent_tab.analysis_info_label.config(text=f"{current_text} (file size analysis: not available)")
                
        except Exception as e:
            self.parent_tab.analysis_info_label.config(text="❌ Configuration error", foreground="red")

    def get_analysis_info(self) -> Dict[str, Any]:
        """Get information about the current analysis state including file size settings"""
        scope = self.parent_tab.analysis_scope.get()
        
        base_info = {
            'analysis_scope': scope,
            'has_report': self.last_report_path is not None and os.path.exists(self.last_report_path),
            'report_path': self.last_report_path,
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
        
        # Add file size settings info
        if hasattr(self.parent_tab, 'file_size_settings'):
            settings_info = self.parent_tab.file_size_settings.get_settings_info()
            base_info.update(settings_info)
        
        return base_info

    def has_selection(self) -> bool:
        """Check if any files or project are selected"""
        return bool(self.selected_analysis_files or self.selected_project_directory)

    def get_selected_items_count(self) -> int:
        """Get count of selected items (files or 1 for project)"""
        if self.selected_project_directory:
            return 1
        return len(self.selected_analysis_files)

    def get_selection_summary(self) -> str:
        """Get a summary of current selection"""
        if self.selected_project_directory:
            dir_name = os.path.basename(self.selected_project_directory)
            return f"Project: {dir_name}"
        elif self.selected_analysis_files:
            if len(self.selected_analysis_files) == 1:
                return f"File: {os.path.basename(self.selected_analysis_files[0])}"
            else:
                return f"{len(self.selected_analysis_files)} files selected"
        else:
            return "No selection" 