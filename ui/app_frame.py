# ui/app_frame.py
"""
AppFrame - Main application orchestrator for Wolfkit
Phase 4 Optimized: Type hints, interface consistency, documentation improvements
Refactored from 1306-line monolithic class to clean orchestrator
"""
from typing import Optional, Dict, Any, Union
from ttkbootstrap import Frame, Notebook, Style
from ttkbootstrap.constants import *

# Import the individual tab implementations
from ui.main_workflow_tab import MainWorkflowTab
from ui.code_review_tab import CodeReviewTab
from ui.document_merge_tab import DocumentMergeTab
from ui.documentation_tab import DocumentationTab


class AppFrame(Frame):
    """
    Main application frame that orchestrates all tabs and handles global app state
    
    Serves as the primary coordinator for the Wolfkit application, managing
    tab creation, styling, and inter-tab communication. Maintains separation
    of concerns by delegating specific functionality to individual tab classes.
    
    Attributes:
        parent: Parent window widget
        tabs (Dict[str, Frame]): Dictionary mapping tab names to tab instances
    """
    
    def __init__(self, parent, padding: int = 10) -> None:
        """
        Initialize the main application frame
        
        Args:
            parent: Parent window widget
            padding: Padding around the main frame in pixels
        """
        super().__init__(parent, padding=padding)
        
        # Global app state
        self.parent = parent
        self.tabs: Dict[str, Union[MainWorkflowTab, CodeReviewTab, DocumentMergeTab, DocumentationTab]] = {}
        
        # UI components (set during initialization)
        self.notebook: Optional[Notebook] = None
        
        # Configure custom tab styling
        self._configure_tab_styling()
        
        # Create and setup the main interface
        self._create_notebook()
        self._create_tabs()
        
        # Setup inter-tab communication
        self._setup_tab_communication()
    
    def _configure_tab_styling(self) -> None:
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
    
    def _create_notebook(self) -> None:
        """Create the main notebook widget for tabs"""
        self.notebook = Notebook(self)
        self.notebook.pack(fill=BOTH, expand=YES)
    
    def _create_tabs(self) -> None:
        """Create and add all application tabs"""
        if not self.notebook:
            raise RuntimeError("Notebook must be created before adding tabs")
        
        # Code Review Tab (AI-powered analysis - priority #1)
        self.tabs['review'] = CodeReviewTab(self.notebook)
        self.notebook.add(self.tabs['review'], text="Code Review")
        
        # Document Merge Tab (AI-powered clustering - priority #2)
        self.tabs['merge'] = DocumentMergeTab(self.notebook)
        self.notebook.add(self.tabs['merge'], text="Document Merge")
        
        # File Testing Tab (safe staging workflow - priority #3)
        self.tabs['main'] = MainWorkflowTab(self.notebook)
        self.notebook.add(self.tabs['main'], text="File Testing")
        
        # Documentation Tab
        self.tabs['docs'] = DocumentationTab(self.notebook)
        self.notebook.add(self.tabs['docs'], text="Documentation")
    
    def _setup_tab_communication(self) -> None:
        """
        Setup communication channels between tabs if needed
        
        Currently tabs are independent, but this method provides a place
        to add inter-tab communication in the future if needed.
        """
        # Future enhancement: Add event system for tab communication
        pass
    
    # Public API for accessing tab information and state
    
    def get_main_workflow_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the main workflow tab state
        
        Returns:
            Dictionary with batch information or None if tab not available
        """
        if 'main' in self.tabs and hasattr(self.tabs['main'], 'get_batch_info'):
            return self.tabs['main'].get_batch_info()
        return None
    
    def get_code_review_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the code review tab state
        
        Returns:
            Dictionary with analysis information or None if tab not available
        """
        if 'review' in self.tabs and hasattr(self.tabs['review'], 'get_analysis_info'):
            return self.tabs['review'].get_analysis_info()
        return None
    
    def get_document_merge_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the document merge tab state
        
        Returns:
            Dictionary with merge information or None if tab not available
        """
        if 'merge' in self.tabs and hasattr(self.tabs['merge'], 'get_merge_info'):
            return self.tabs['merge'].get_merge_info()
        return None
    
    def switch_to_tab(self, tab_name: str) -> bool:
        """
        Programmatically switch to a specific tab
        
        Args:
            tab_name: Name of the tab ('review', 'merge', 'main', 'docs')
            
        Returns:
            True if tab switch was successful, False otherwise
        """
        if tab_name in self.tabs and self.notebook:
            try:
                tab_index = list(self.tabs.keys()).index(tab_name)
                self.notebook.select(tab_index)
                return True
            except (ValueError, tk.TclError):
                return False
        return False
    
    def get_current_tab(self) -> Optional[str]:
        """
        Get the currently selected tab name
        
        Returns:
            Name of current tab or None if unable to determine
        """
        if not self.notebook:
            return None
            
        try:
            current_index = self.notebook.index(self.notebook.select())
            tab_names = list(self.tabs.keys())
            if 0 <= current_index < len(tab_names):
                return tab_names[current_index]
        except tk.TclError:
            pass
        return None
    
    def get_app_state(self) -> Dict[str, Any]:
        """
        Get comprehensive application state information
        
        Returns:
            Dictionary containing complete application state
        """
        return {
            'current_tab': self.get_current_tab(),
            'main_workflow': self.get_main_workflow_info(),
            'code_review': self.get_code_review_info(),
            'document_merge': self.get_document_merge_info(),
            'total_tabs': len(self.tabs),
            'available_tabs': list(self.tabs.keys())
        }
    
    def refresh_tab(self, tab_name: str) -> bool:
        """
        Refresh a specific tab (useful for future extensions)
        
        Args:
            tab_name: Name of the tab to refresh
            
        Returns:
            True if refresh was successful, False otherwise
        """
        if tab_name in self.tabs and hasattr(self.tabs[tab_name], 'refresh'):
            try:
                self.tabs[tab_name].refresh()
                return True
            except Exception:
                return False
        return False
    
    def are_all_tabs_initialized(self) -> bool:
        """
        Check if all tabs have been fully initialized
        
        Returns:
            True if all tabs are initialized, False otherwise
        """
        return all(
            hasattr(tab, 'is_initialized') and tab.is_initialized() 
            for tab in self.tabs.values()
        )
    
    def get_tab_instance(self, tab_name: str) -> Optional[Union[MainWorkflowTab, CodeReviewTab, DocumentMergeTab, DocumentationTab]]:
        """
        Get direct reference to a tab instance
        
        Args:
            tab_name: Name of the tab to retrieve
            
        Returns:
            Tab instance or None if not found
        """
        return self.tabs.get(tab_name)
    
    def get_tab_count(self) -> int:
        """
        Get the total number of tabs
        
        Returns:
            Number of tabs in the application
        """
        return len(self.tabs)
    
    def has_tab(self, tab_name: str) -> bool:
        """
        Check if a specific tab exists
        
        Args:
            tab_name: Name of the tab to check
            
        Returns:
            True if tab exists, False otherwise
        """
        return tab_name in self.tabs