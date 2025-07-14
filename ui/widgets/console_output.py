# ui/widgets/console_output.py
"""
ConsoleOutput Widget - Reusable console output component
Phase 4 Optimized: Type hints, threading safety, interface consistency
"""
import tkinter as tk
from typing import Optional, Literal, Union
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar
from ttkbootstrap.constants import *
from datetime import datetime
import threading


# Type alias for message levels
MessageLevel = Literal["info", "success", "warning", "error"]


class ConsoleOutput(Frame):
    """
    Reusable console output widget with scrolling and clear functionality
    
    Thread-safe console widget for displaying timestamped messages with different
    severity levels. Supports color-coded output and automatic scrolling.
    
    Attributes:
        title (str): Console title displayed in header
        height (int): Height in lines for the text widget
    """
    
    def __init__(
        self, 
        parent, 
        title: str = "Console Output:", 
        height: int = 20, 
        **kwargs
    ) -> None:
        """
        Initialize ConsoleOutput widget
        
        Args:
            parent: Parent widget (tkinter/ttkbootstrap widget)
            title: Title label text for the console header
            height: Height in lines for the text widget
            **kwargs: Additional keyword arguments passed to Frame constructor
        """
        super().__init__(parent, **kwargs)
        
        self.title: str = title
        self.height: int = height
        self._lock: threading.Lock = threading.Lock()  # Thread-safe operations
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
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
        
        # Determine best monospace font available
        font_family = self._get_monospace_font()
        
        self.console_text = Text(
            console_frame, 
            wrap="word", 
            height=self.height,
            state="disabled",
            font=(font_family, 9)
        )
        self.console_text.pack(side=LEFT, fill=BOTH, expand=YES)
        
        self.scrollbar = Scrollbar(console_frame, command=self.console_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text.config(yscrollcommand=self.scrollbar.set)
        
        # Configure text tags for different message types
        self._configure_text_tags()
    
    def _get_monospace_font(self) -> str:
        """
        Get the best available monospace font for the console
        
        Returns:
            Font family name string
        """
        available_fonts = tk.font.families()
        preferred_fonts = ["Consolas", "Monaco", "Menlo", "DejaVu Sans Mono", "TkFixedFont"]
        
        for font in preferred_fonts:
            if font in available_fonts:
                return font
        return "TkFixedFont"  # Fallback
    
    def _configure_text_tags(self) -> None:
        """Configure text tags for different message types"""
        self.console_text.tag_configure("info", foreground="blue")
        self.console_text.tag_configure("success", foreground="green")
        self.console_text.tag_configure("warning", foreground="orange")
        self.console_text.tag_configure("error", foreground="red")
        self.console_text.tag_configure("timestamp", foreground="gray", font=("TkFixedFont", 8))
    
    def write(
        self, 
        text: str, 
        level: MessageLevel = "info", 
        include_timestamp: bool = True
    ) -> None:
        """
        Write text to the console with specified formatting
        
        Args:
            text: Text content to write to console
            level: Message severity level for color coding
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
    
    def write_info(self, text: str, include_timestamp: bool = True) -> None:
        """
        Write info message to console
        
        Args:
            text: Info message text
            include_timestamp: Whether to include timestamp prefix
        """
        self.write(text, "info", include_timestamp)
    
    def write_success(self, text: str, include_timestamp: bool = True) -> None:
        """
        Write success message to console
        
        Args:
            text: Success message text
            include_timestamp: Whether to include timestamp prefix
        """
        self.write(text, "success", include_timestamp)
    
    def write_warning(self, text: str, include_timestamp: bool = True) -> None:
        """
        Write warning message to console
        
        Args:
            text: Warning message text
            include_timestamp: Whether to include timestamp prefix
        """
        self.write(text, "warning", include_timestamp)
    
    def write_error(self, text: str, include_timestamp: bool = True) -> None:
        """
        Write error message to console
        
        Args:
            text: Error message text
            include_timestamp: Whether to include timestamp prefix
        """
        self.write(text, "error", include_timestamp)
    
    def clear(self) -> None:
        """Clear all console content"""
        with self._lock:
            self.console_text.config(state="normal")
            self.console_text.delete("1.0", "end")
            self.console_text.config(state="disabled")
    
    def get_content(self) -> str:
        """
        Get all console content as string
        
        Returns:
            Complete console content without formatting
        """
        return self.console_text.get("1.0", "end-1c")
    
    def set_title(self, title: str) -> None:
        """
        Update the console title
        
        Args:
            title: New title text for console header
        """
        self.title = title
        self.title_label.config(text=title)
    
    def append_to_title(self, suffix: str) -> None:
        """
        Append text to the current title
        
        Args:
            suffix: Text to append to current title
        """
        new_title = f"{self.title} {suffix}"
        self.set_title(new_title)
    
    def get_title(self) -> str:
        """
        Get the current console title
        
        Returns:
            Current title string
        """
        return self.title
    
    def get_line_count(self) -> int:
        """
        Get the number of lines currently in the console
        
        Returns:
            Number of lines in console content
        """
        content = self.get_content()
        return len(content.split('\n')) if content else 0
    
    def set_height(self, height: int) -> None:
        """
        Update the console height
        
        Args:
            height: New height in lines
        """
        self.height = height
        self.console_text.config(height=height)
    
    def is_empty(self) -> bool:
        """
        Check if console is empty
        
        Returns:
            True if console has no content, False otherwise
        """
        return len(self.get_content().strip()) == 0