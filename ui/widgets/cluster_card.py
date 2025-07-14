# ui/widgets/cluster_card.py
"""
ClusterCard Widget - Custom widget for displaying document clusters with merge options
Extracted from app_frame.py as part of Phase 1 refactoring
"""
import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Text, Scrollbar, LabelFrame
from ttkbootstrap.constants import *
from pathlib import Path


class ClusterCard(LabelFrame):
    """Custom widget to display a document cluster with merge options"""
    
    def __init__(self, parent, cluster, on_merge_callback, **kwargs):
        """
        Initialize ClusterCard widget
        
        Args:
            parent: Parent widget
            cluster: DocumentCluster object containing cluster data
            on_merge_callback: Callback function for merge actions
            **kwargs: Additional keyword arguments for LabelFrame
        """
        super().__init__(parent, text=f"Cluster {cluster.cluster_id + 1}", **kwargs)
        
        self.cluster = cluster
        self.on_merge_callback = on_merge_callback
        self.expanded = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the cluster card UI elements"""
        # Header with similarity score and document count
        header_frame = Frame(self)
        header_frame.pack(fill=X, padx=5, pady=5)
        
        similarity_text = f"{self.cluster.similarity_score:.1%} similar • {len(self.cluster.documents)} documents"
        self.similarity_label = Label(
            header_frame, 
            text=similarity_text, 
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        self.similarity_label.pack(side=LEFT)
        
        # Suggested merge name
        name_frame = Frame(self)
        name_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        Label(name_frame, text="Suggested name:", font=("TkDefaultFont", 8)).pack(side=LEFT)
        self.name_var = tk.StringVar(value=self.cluster.suggested_merge_name)
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, width=30)
        self.name_entry.pack(side=LEFT, padx=(5, 0))
        
        # Document list (collapsible)
        self.documents_frame = Frame(self)
        self.documents_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        # Show first 3 documents, with option to expand
        docs_to_show = self.cluster.documents[:3]
        remaining_count = len(self.cluster.documents) - 3
        
        for doc in docs_to_show:
            doc_label = Label(
                self.documents_frame, 
                text=f"• {Path(doc).name}", 
                font=("TkDefaultFont", 8),
                anchor="w"
            )
            doc_label.pack(fill=X)
        
        if remaining_count > 0:
            self.expand_button = Button(
                self.documents_frame,
                text=f"+ {remaining_count} more documents",
                bootstyle="link",
                command=self._toggle_documents
            )
            self.expand_button.pack(anchor="w")
            
            # Hidden documents (shown when expanded)
            self.hidden_docs_frame = Frame(self.documents_frame)
            for doc in self.cluster.documents[3:]:
                doc_label = Label(
                    self.hidden_docs_frame,
                    text=f"• {Path(doc).name}",
                    font=("TkDefaultFont", 8),
                    anchor="w"
                )
                doc_label.pack(fill=X)
        
        # Preview section (collapsible)
        preview_frame = Frame(self)
        preview_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        self.preview_button = Button(
            preview_frame,
            text="▼ Show Preview",
            bootstyle="link",
            command=self._toggle_preview
        )
        self.preview_button.pack(anchor="w")
        
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
        
        # Action buttons
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
    
    def _toggle_documents(self):
        """Toggle showing all documents in the cluster"""
        if not self.expanded:
            self.hidden_docs_frame.pack(fill=X, after=self.expand_button)
            self.expand_button.config(text="▲ Show fewer documents")
            self.expanded = True
        else:
            self.hidden_docs_frame.pack_forget()
            remaining_count = len(self.cluster.documents) - 3
            self.expand_button.config(text=f"+ {remaining_count} more documents")
            self.expanded = False
    
    def _toggle_preview(self):
        """Toggle showing the merge preview"""
        if self.preview_text_frame.winfo_viewable():
            self.preview_text_frame.pack_forget()
            self.preview_button.config(text="▼ Show Preview")
        else:
            self.preview_text_frame.pack(fill=BOTH, expand=YES, after=self.preview_button)
            self.preview_button.config(text="▲ Hide Preview")
    
    def _load_preview(self):
        """Load the merge preview into the text widget"""
        if self.cluster.merge_preview:
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", "end")
            
            # Show a truncated version for the card
            preview_content = self.cluster.merge_preview[:1000]
            if len(self.cluster.merge_preview) > 1000:
                preview_content += "\n\n[... Content truncated. Full preview available after merge ...]"
            
            self.preview_text.insert("1.0", preview_content)
            self.preview_text.config(state="disabled")
        else:
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", "Preview will be generated during merge...")
            self.preview_text.config(state="disabled")
    
    def _on_merge_clicked(self):
        """Handle merge button click"""
        custom_name = self.name_var.get()
        self.on_merge_callback(self.cluster, "merge", custom_name)
    
    def _on_preview_clicked(self):
        """Handle preview only button click"""
        self.on_merge_callback(self.cluster, "preview", None)
    
    def _on_skip_clicked(self):
        """Handle skip button click"""
        self.on_merge_callback(self.cluster, "skip", None)