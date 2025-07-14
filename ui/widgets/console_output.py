# ui/widgets/console_output.py
"""
ConsoleOutput Widget - Reusable console output component
Extracted from app_frame.py as part of Phase 1 refactoring
"""
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar
from ttkbootstrap.constants import *
from datetime import datetime
import threading


class ConsoleOutput(Frame):
    """Reusable console output widget with scrolling and clear functionality"""
    
    def __init__(self, parent, title="Console Output:", height=20, **kwargs):
        """
        Initialize ConsoleOutput widget
        
        Args:
            parent: Parent widget
            title: Title label text for the console
            height: Height in lines for the text widget
            **kwargs: Additional keyword arguments for Frame
        """
        super().__init__(parent, **kwargs)
        
        self.title = title
        self.height = height
        self._lock = threading.Lock()  # For thread-safe operations
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the console UI elements"""
        # Header with title and clear button
        header_frame = Frame(self)
        header_frame.pack(fill=X, pady=(0, 5))
        
        self.title_label = Label(header_frame, text=self.title, anchor="w")
        self.title_label.pack(side=LEFT)
        
        self.clear_button = Button(
            header_frame, 
            text="Clear", 
            bootstyle="secondary-outline",
            command=self.clear
        )
        self.clear_button.pack(side=RIGHT)
        
        # Main console area with scrollbar
        console_frame = Frame(self)
        console_frame.pack(fill=BOTH, expand=YES)
        
        self.console_text = Text(
            console_frame, 
            wrap="word", 
            height=self.height,
            state="disabled",
            font=("Consolas", 9) if tk.font.families().__contains__("Consolas") else ("TkFixedFont", 9)
        )
        self.console_text.pack(side=LEFT, fill=BOTH, expand=YES)
        
        self.scrollbar = Scrollbar(console_frame, command=self.console_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text.config(yscrollcommand=self.scrollbar.set)
        
        # Configure text tags for different message types
        self.console_text.tag_configure("info", foreground="blue")
        self.console_text.tag_configure("success", foreground="green")
        self.console_text.tag_configure("warning", foreground="orange")
        self.console_text.tag_configure("error", foreground="red")
        self.console_text.tag_configure("timestamp", foreground="gray", font=("TkFixedFont", 8))
    
    def write(self, text, level="info", include_timestamp=True):
        """
        Write text to the console
        
        Args:
            text: Text to write
            level: Message level ('info', 'success', 'warning', 'error')
            include_timestamp: Whether to include timestamp prefix
        """
        with self._lock:
            self.console_text.config(state="normal")
            
            if include_timestamp:
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.console_text.insert("end", f"[{timestamp}] ", "timestamp")
            
            self.console_text.insert("end", text + "\n", level)
            self.console_text.see("end")
            self.console_text.config(state="disabled")
    
    def write_info(self, text, include_timestamp=True):
        """Write info message to console"""
        self.write(text, "info", include_timestamp)
    
    def write_success(self, text, include_timestamp=True):
        """Write success message to console"""
        self.write(text, "success", include_timestamp)
    
    def write_warning(self, text, include_timestamp=True):
        """Write warning message to console"""
        self.write(text, "warning", include_timestamp)
    
    def write_error(self, text, include_timestamp=True):
        """Write error message to console"""
        self.write(text, "error", include_timestamp)
    
    def clear(self):
        """Clear all console content"""
        with self._lock:
            self.console_text.config(state="normal")
            self.console_text.delete("1.0", "end")
            self.console_text.config(state="disabled")
    
    def get_content(self):
        """Get all console content as string"""
        return self.console_text.get("1.0", "end-1c")
    
    def set_title(self, title):
        """Update the console title"""
        self.title = title
        self.title_label.config(text=title)
    
    def append_to_title(self, suffix):
        """Append text to the current title"""
        new_title = f"{self.title} {suffix}"
        self.set_title(new_title)