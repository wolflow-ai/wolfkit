# ui/widgets/cluster_card.py
"""
ClusterCard Widget - Custom widget for displaying document clusters with merge options
Phase 4 Optimized: Type hints, interface consistency, callback improvements
"""
import tkinter as tk
from typing import Callable, Optional, Any, Protocol, Union
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar, LabelFrame
from ttkbootstrap.constants import *
from pathlib import Path


class DocumentCluster(Protocol):
    """
    Protocol defining the expected interface for document cluster objects
    
    This allows type checking without importing the actual DocumentCluster class,
    preventing circular imports while maintaining type safety.
    """
    cluster_id: int
    similarity_score: float
    documents: list[str]
    suggested_merge_name: str
    merge_preview: Optional[str]


# Type alias for cluster actions
ClusterAction = Union["merge", "preview", "skip"]

# Type alias for callback function
ClusterCallback = Callable[[DocumentCluster, ClusterAction, Optional[str]], None]


class ClusterCard(LabelFrame):
    """
    Custom widget to display a document cluster with merge options
    
    Provides an interactive card interface for viewing cluster details,
    editing merge names, and triggering cluster actions. Supports collapsible
    sections for documents and preview content.
    
    Attributes:
        cluster: Document cluster data object
        on_merge_callback: Callback function for handling cluster actions
        expanded: Whether the document list is currently expanded
    """
    
    def __init__(
        self, 
        parent, 
        cluster: DocumentCluster, 
        on_merge_callback: ClusterCallback, 
        **kwargs
    ) -> None:
        """
        Initialize ClusterCard widget
        
        Args:
            parent: Parent widget (tkinter/ttkbootstrap widget)
            cluster: DocumentCluster object containing cluster data
            on_merge_callback: Callback function for merge actions
                              Signature: (cluster, action, custom_name) -> None
            **kwargs: Additional keyword arguments for LabelFrame
        """
        super().__init__(parent, text=f"Cluster {cluster.cluster_id + 1}", **kwargs)
        
        self.cluster: DocumentCluster = cluster
        self.on_merge_callback: ClusterCallback = on_merge_callback
        self.expanded: bool = False
        
        # Initialize UI components (set in _create_widgets)
        self.similarity_label: Optional[Label] = None
        self.name_var: Optional[tk.StringVar] = None
        self.name_entry: Optional[tk.Entry] = None
        self.documents_frame: Optional[Frame] = None
        self.expand_button: Optional[Button] = None
        self.hidden_docs_frame: Optional[Frame] = None
        self.preview_button: Optional[Button] = None
        self.preview_text_frame: Optional[Frame] = None
        self.preview_text: Optional[Text] = None
        self.merge_button: Optional[Button] = None
        self.preview_only_button: Optional[Button] = None
        self.skip_button: Optional[Button] = None
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create the cluster card UI elements"""
        # Header with similarity score and document count
        header_frame = Frame(self)
        header_frame.pack(fill=X, padx=5, pady=5)
        
        similarity_text = self._format_similarity_text()
        self.similarity_label = Label(
            header_frame, 
            text=similarity_text, 
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.similarity_label.pack(side=LEFT)
        
        # Suggested merge name section
        self._create_merge_name_section()
        
        # Document list section (collapsible)
        self._create_documents_section()
        
        # Preview section (collapsible)
        self._create_preview_section()
        
        # Action buttons
        self._create_action_buttons()
    
    def _format_similarity_text(self) -> str:
        """
        Format the similarity and document count text
        
        Returns:
            Formatted text string for similarity display
        """
        return f"{self.cluster.similarity_score:.1%} similar • {len(self.cluster.documents)} documents"
    
    def _create_merge_name_section(self) -> None:
        """Create the merge name input section"""
        name_frame = Frame(self)
        name_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        Label(name_frame, text="Suggested name:", font=("TkDefaultFont", 8)).pack(side=LEFT)
        self.name_var = tk.StringVar(value=self.cluster.suggested_merge_name)
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, width=30)
        self.name_entry.pack(side=LEFT, padx=(5, 0))
    
    def _create_documents_section(self) -> None:
        """Create the collapsible documents list section"""
        self.documents_frame = Frame(self)
        self.documents_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        # Show first 3 documents, with option to expand
        docs_to_show = self.cluster.documents[:3]
        remaining_count = len(self.cluster.documents) - 3
        
        # Display initial documents
        for doc in docs_to_show:
            doc_label = Label(
                self.documents_frame, 
                text=f"• {Path(doc).name}", 
                font=("TkDefaultFont", 8),
                anchor="w"
            )
            doc_label.pack(fill=X)
        
        # Expand button for additional documents
        if remaining_count > 0:
            self.expand_button = Button(
                self.documents_frame,
                text=f"+ {remaining_count} more documents",
                bootstyle="link",
                command=self._toggle_documents
            )
            self.expand_button.pack(anchor="w")
            
            # Hidden documents container (shown when expanded)
            self.hidden_docs_frame = Frame(self.documents_frame)
            for doc in self.cluster.documents[3:]:
                doc_label = Label(
                    self.hidden_docs_frame,
                    text=f"• {Path(doc).name}",
                    font=("TkDefaultFont", 8),
                    anchor="w"
                )
                doc_label.pack(fill=X)
    
    def _create_preview_section(self) -> None:
        """Create the collapsible preview section"""
        preview_frame = Frame(self)
        preview_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        self.preview_button = Button(
            preview_frame,
            text="▼ Show Preview",
            bootstyle="link",
            command=self._toggle_preview
        )
        self.preview_button.pack(anchor="w")
        
        # Preview text area (initially hidden)
        self.preview_text_frame = Frame(preview_frame)
        self.preview_text = Text(
            self.preview_text_frame,
            height=4,
            wrap="word",
            font=("TkDefaultFont", 8),
            state="disabled"
        )
        
        preview_scroll = Scrollbar(self.preview_text_frame, command=self.preview_text.yview)
        self.preview_text.config(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side=LEFT, fill=BOTH, expand=YES)
        preview_scroll.pack(side=RIGHT, fill=Y)
        
        # Load preview content
        self._load_preview()
    
    def _create_action_buttons(self) -> None:
        """Create the action buttons section"""
        button_frame = Frame(self)
        button_frame.pack(fill=X, padx=5, pady=5)
        
        self.merge_button = Button(
            button_frame,
            text="🔄 Merge This Cluster",
            bootstyle="primary",
            command=self._on_merge_clicked
        )
        self.merge_button.pack(side=LEFT, padx=(0, 5))
        
        self.preview_only_button = Button(
            button_frame,
            text="👁 Preview Only",
            bootstyle="info-outline",
            command=self._on_preview_clicked
        )
        self.preview_only_button.pack(side=LEFT, padx=(0, 5))
        
        self.skip_button = Button(
            button_frame,
            text="❌ Skip",
            bootstyle="secondary-outline",
            command=self._on_skip_clicked
        )
        self.skip_button.pack(side=LEFT)
    
    def _toggle_documents(self) -> None:
        """Toggle showing all documents in the cluster"""
        if not self.expanded and self.hidden_docs_frame and self.expand_button:
            self.hidden_docs_frame.pack(fill=X, after=self.expand_button)
            self.expand_button.config(text="▲ Show fewer documents")
            self.expanded = True
        elif self.expanded and self.hidden_docs_frame and self.expand_button:
            self.hidden_docs_frame.pack_forget()
            remaining_count = len(self.cluster.documents) - 3
            self.expand_button.config(text=f"+ {remaining_count} more documents")
            self.expanded = False
    
    def _toggle_preview(self) -> None:
        """Toggle showing the merge preview"""
        if (self.preview_text_frame and self.preview_button and 
            self.preview_text_frame.winfo_viewable()):
            self.preview_text_frame.pack_forget()
            self.preview_button.config(text="▼ Show Preview")
        elif self.preview_text_frame and self.preview_button:
            self.preview_text_frame.pack(fill=BOTH, expand=YES, after=self.preview_button)
            self.preview_button.config(text="▲ Hide Preview")
    
    def _load_preview(self) -> None:
        """Load the merge preview into the text widget"""
        if not self.preview_text:
            return
            
        preview_content = self._get_preview_content()
        
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", preview_content)
        self.preview_text.config(state="disabled")
    
    def _get_preview_content(self) -> str:
        """
        Get the preview content with appropriate truncation
        
        Returns:
            Preview content string, potentially truncated for display
        """
        if self.cluster.merge_preview:
            # Show a truncated version for the card
            preview_content = self.cluster.merge_preview[:1000]
            if len(self.cluster.merge_preview) > 1000:
                preview_content += "\n\n[... Content truncated. Full preview available after merge ...]"
            return preview_content
        else:
            return "Preview will be generated during merge..."
    
    def _on_merge_clicked(self) -> None:
        """Handle merge button click"""
        custom_name = self.name_var.get() if self.name_var else None
        self.on_merge_callback(self.cluster, "merge", custom_name)
    
    def _on_preview_clicked(self) -> None:
        """Handle preview only button click"""
        self.on_merge_callback(self.cluster, "preview", None)
    
    def _on_skip_clicked(self) -> None:
        """Handle skip button click"""
        self.on_merge_callback(self.cluster, "skip", None)
    
    def get_custom_name(self) -> str:
        """
        Get the current custom merge name from the input field
        
        Returns:
            Custom merge name entered by user
        """
        return self.name_var.get() if self.name_var else ""
    
    def set_custom_name(self, name: str) -> None:
        """
        Set the custom merge name in the input field
        
        Args:
            name: New merge name to set
        """
        if self.name_var:
            self.name_var.set(name)
    
    def update_cluster_data(self, cluster: DocumentCluster) -> None:
        """
        Update the cluster data and refresh the display
        
        Args:
            cluster: New cluster data to display
        """
        self.cluster = cluster
        
        # Update similarity label
        if self.similarity_label:
            similarity_text = self._format_similarity_text()
            self.similarity_label.config(text=similarity_text)
        
        # Update title
        self.config(text=f"Cluster {cluster.cluster_id + 1}")
        
        # Update suggested name
        if self.name_var:
            self.name_var.set(cluster.suggested_merge_name)
        
        # Reload preview
        self._load_preview()
    
    def set_button_state(self, state: str) -> None:
        """
        Set the state of all action buttons
        
        Args:
            state: Button state ("normal", "disabled")
        """
        buttons = [self.merge_button, self.preview_only_button, self.skip_button]
        for button in buttons:
            if button:
                button.config(state=state)