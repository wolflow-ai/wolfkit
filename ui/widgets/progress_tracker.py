# ui/widgets/progress_tracker.py
"""
ProgressTracker Widget - Reusable progress bar and status component
Phase 4 Optimized: Type hints, interface consistency, documentation improvements
"""
from typing import Optional, Union
from ttkbootstrap import Frame, Label, Progressbar
from ttkbootstrap.constants import *


class ProgressTracker(Frame):
    """
    Reusable progress bar with status message management
    
    Provides indeterminate progress indication with status messages.
    Thread-safe for UI updates from background operations.
    
    Attributes:
        is_active (bool): Whether progress is currently running
        current_message (str): Current status message being displayed
    """
    
    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize ProgressTracker widget
        
        Args:
            parent: Parent widget (tkinter/ttkbootstrap widget)
            **kwargs: Additional keyword arguments passed to Frame constructor
        """
        super().__init__(parent, **kwargs)
        
        self.is_active: bool = False
        self.current_message: str = "Ready"
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create the progress tracker UI elements"""
        # Status label
        self.status_label = Label(
            self, 
            text=self.current_message, 
            anchor="w"
        )
        self.status_label.pack(fill=X, pady=(0, 5))
        
        # Progress bar (initially hidden)
        self.progress_bar = Progressbar(
            self, 
            mode='indeterminate',
            bootstyle="info"
        )
        # Don't pack initially - will be shown when needed
        
    def start_progress(self, message: str = "Processing...") -> None:
        """
        Start progress indication with a status message
        
        Args:
            message: Status message to display during progress
        """
        self.current_message = message
        self.status_label.config(text=message)
        
        if not self.is_active:
            self.progress_bar.pack(fill=X, pady=(0, 5))
            self.progress_bar.start()
            self.is_active = True
    
    def stop_progress(self, final_message: str = "Complete") -> None:
        """
        Stop progress indication and update status
        
        Args:
            final_message: Final status message to display after completion
        """
        if self.is_active:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.is_active = False
        
        self.current_message = final_message
        self.status_label.config(text=final_message)
    
    def update_message(self, message: str) -> None:
        """
        Update status message without affecting progress state
        
        Args:
            message: New status message to display
        """
        self.current_message = message
        self.status_label.config(text=message)
    
    def set_progress_style(self, bootstyle: str) -> None:
        """
        Change the progress bar style
        
        Args:
            bootstyle: New bootstrap style for progress bar
                      (e.g., "info", "success", "warning", "danger")
        """
        self.progress_bar.config(bootstyle=bootstyle)
    
    def is_running(self) -> bool:
        """
        Check if progress is currently active
        
        Returns:
            True if progress is running, False otherwise
        """
        return self.is_active
    
    def reset(self) -> None:
        """Reset progress tracker to initial state"""
        self.stop_progress("Ready")
    
    def get_status(self) -> str:
        """
        Get the current status message
        
        Returns:
            Current status message string
        """
        return self.current_message


class StatusOnlyTracker(Frame):
    """
    Simplified version with just status messages (no progress bar)
    
    Lightweight alternative when progress indication isn't needed,
    just status message updates.
    
    Attributes:
        current_message (str): Current status message being displayed
    """
    
    def __init__(self, parent, initial_message: str = "Ready", **kwargs) -> None:
        """
        Initialize StatusOnlyTracker widget
        
        Args:
            parent: Parent widget (tkinter/ttkbootstrap widget)
            initial_message: Initial status message to display
            **kwargs: Additional keyword arguments passed to Frame constructor
        """
        super().__init__(parent, **kwargs)
        
        self.current_message: str = initial_message
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create the status tracker UI elements"""
        self.status_label = Label(
            self, 
            text=self.current_message, 
            anchor="w"
        )
        self.status_label.pack(fill=X)
    
    def update(self, message: str) -> None:
        """
        Update the status message
        
        Args:
            message: New status message to display
        """
        self.current_message = message
        self.status_label.config(text=message)
    
    def clear(self) -> None:
        """Clear the status message (set to empty string)"""
        self.update("")
    
    def reset(self, message: str = "Ready") -> None:
        """
        Reset to initial or specified message
        
        Args:
            message: Message to reset to (default: "Ready")
        """
        self.update(message)
    
    def get_status(self) -> str:
        """
        Get the current status message
        
        Returns:
            Current status message string
        """
        return self.current_message