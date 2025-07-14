# ui/app_frame.py
"""
AppFrame - Main application orchestrator for Wolfkit
Refactored from 1306-line monolithic class to clean orchestrator
Phase 3 of the refactoring strategy
"""
from ttkbootstrap import Frame, Notebook, Style
from ttkbootstrap.constants import *

# Import the individual tab implementations
from ui.main_workflow_tab import MainWorkflowTab
from ui.code_review_tab import CodeReviewTab
from ui.document_merge_tab import DocumentMergeTab
from ui.documentation_tab import DocumentationTab


class AppFrame(Frame):
    """Main application frame that orchestrates all tabs and handles global app state"""
    
    def __init__(self, parent, padding=10):
        """
        Initialize the main application frame
        
        Args:
            parent: Parent window
            padding: Padding around the main frame
        """
        super().__init__(parent, padding=padding)
        
        # Global app state
        self.parent = parent
        self.tabs = {}
        
        # Configure custom tab styling
        self._configure_tab_styling()
        
        # Create and setup the main interface
        self._create_notebook()
        self._create_tabs()
        
        # Setup inter-tab communication
        self._setup_tab_communication()
    
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
    
    def _create_notebook(self):
        """Create the main notebook widget for tabs"""
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=YES)
    
    def _create_tabs(self):
        """Create and add all application tabs"""
        # Main Workflow Tab
        self.tabs['main'] = MainWorkflowTab(self.notebook)
        self.notebook.add(self.tabs['main'], text="Main Workflow")
        
        # Code Review Tab
        self.tabs['review'] = CodeReviewTab(self.notebook)
        self.notebook.add(self.tabs['review'], text="Code Review")
        
        # Document Merge Tab
        self.tabs['merge'] = DocumentMergeTab(self.notebook)
        self.notebook.add(self.tabs['merge'], text="Document Merge")
        
        # Documentation Tab
        self.tabs['docs'] = DocumentationTab(self.notebook)
        self.notebook.add(self.tabs['docs'], text="Documentation")
    
    def _setup_tab_communication(self):
        """Setup communication channels between tabs if needed"""
        # For now, tabs are independent, but this method provides a place
        # to add inter-tab communication in the future if needed
        pass
    
    # Public API for accessing tab information and state
    
    def get_main_workflow_info(self):
        """Get information about the main workflow tab state"""
        if 'main' in self.tabs:
            return self.tabs['main'].get_batch_info()
        return None
    
    def get_code_review_info(self):
        """Get information about the code review tab state"""
        if 'review' in self.tabs:
            return self.tabs['review'].get_analysis_info()
        return None
    
    def get_document_merge_info(self):
        """Get information about the document merge tab state"""
        if 'merge' in self.tabs:
            return self.tabs['merge'].get_merge_info()
        return None
    
    def switch_to_tab(self, tab_name):
        """
        Programmatically switch to a specific tab
        
        Args:
            tab_name: Name of the tab ('main', 'review', 'merge', 'docs')
        """
        if tab_name in self.tabs:
            tab_index = list(self.tabs.keys()).index(tab_name)
            self.notebook.select(tab_index)
    
    def get_current_tab(self):
        """Get the currently selected tab name"""
        current_index = self.notebook.index(self.notebook.select())
        tab_names = list(self.tabs.keys())
        if 0 <= current_index < len(tab_names):
            return tab_names[current_index]
        return None
    
    def get_app_state(self):
        """Get comprehensive application state information"""
        return {
            'current_tab': self.get_current_tab(),
            'main_workflow': self.get_main_workflow_info(),
            'code_review': self.get_code_review_info(),
            'document_merge': self.get_document_merge_info(),
            'total_tabs': len(self.tabs)
        }
    
    def refresh_tab(self, tab_name):
        """
        Refresh a specific tab (useful for future extensions)
        
        Args:
            tab_name: Name of the tab to refresh
        """
        if tab_name in self.tabs and hasattr(self.tabs[tab_name], 'refresh'):
            self.tabs[tab_name].refresh()
    
    def are_all_tabs_initialized(self):
        """Check if all tabs have been fully initialized"""
        return all(tab.is_initialized() for tab in self.tabs.values())