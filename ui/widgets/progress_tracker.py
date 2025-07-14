# ui/widgets/progress_tracker.py
"""
ProgressTracker Widget - Reusable progress bar and status component
Extracted from app_frame.py as part of Phase 1 refactoring
"""
from ttkbootstrap import Frame, Label, Progressbar
from ttkbootstrap.constants import *


class ProgressTracker(Frame):
    """Reusable progress bar with status message management"""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize ProgressTracker widget
        
        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments for Frame
        """
        super().__init__(parent, **kwargs)
        
        self.is_active = False
        self.current_message = "Ready"
        
        self._create_widgets()
    
    def _create_widgets(self):
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
        
    def start_progress(self, message="Processing..."):
        """
        Start progress indication with a status message
        
        Args:
            message: Status message to display
        """
        self.current_message = message
        self.status_label.config(text=message)
        
        if not self.is_active:
            self.progress_bar.pack(fill=X, pady=(0, 5))
            self.progress_bar.start()
            self.is_active = True
    
    def stop_progress(self, final_message="Complete"):
        """
        Stop progress indication and update status
        
        Args:
            final_message: Final status message to display
        """
        if self.is_active:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.is_active = False
        
        self.current_message = final_message
        self.status_label.config(text=final_message)
    
    def update_message(self, message):
        """
        Update status message without affecting progress state
        
        Args:
            message: New status message
        """
        self.current_message = message
        self.status_label.config(text=message)
    
    def set_progress_style(self, bootstyle):
        """
        Change the progress bar style
        
        Args:
            bootstyle: New bootstrap style for progress bar
        """
        self.progress_bar.config(bootstyle=bootstyle)
    
    def is_running(self):
        """Check if progress is currently active"""
        return self.is_active
    
    def reset(self):
        """Reset to initial state"""
        self.stop_progress("Ready")


class StatusOnlyTracker(Frame):
    """Simplified version with just status messages (no progress bar)"""
    
    def __init__(self, parent, initial_message="Ready", **kwargs):
        """
        Initialize StatusOnlyTracker widget
        
        Args:
            parent: Parent widget
            initial_message: Initial status message
            **kwargs: Additional keyword arguments for Frame
        """
        super().__init__(parent, **kwargs)
        
        self.current_message = initial_message
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the status tracker UI elements"""
        self.status_label = Label(
            self, 
            text=self.current_message, 
            anchor="w"
        )
        self.status_label.pack(fill=X)
    
    def update(self, message):
        """
        Update the status message
        
        Args:
            message: New status message
        """
        self.current_message = message
        self.status_label.config(text=message)
    
    def clear(self):
        """Clear the status message"""
        self.update("")
    
    def reset(self, message="Ready"):
        """Reset to initial or specified message"""
        self.update(message)