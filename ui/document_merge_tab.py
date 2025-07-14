# ui/document_merge_tab.py
"""
DocumentMergeTab - Document clustering and merging functionality
Phase 4 Optimized: Local imports, type hints, interface consistency
"""
import os
import tkinter as tk
from typing import List, Tuple, Optional, Any, Dict, Union
from ttkbootstrap import Frame, Label, Button, Spinbox
from ttkbootstrap.constants import *
from ui.base_tab import BaseTab
from ui.widgets import ClusterCard


class DocumentMergeTab(BaseTab):
    """
    Document merge tab for clustering and merging related documents
    
    Provides interface for selecting document folders, configuring clustering
    parameters, analyzing documents with AI, and managing merge operations
    through interactive cluster cards.
    
    Attributes:
        selected_document_folder (Optional[str]): Path to selected document folder
        num_clusters (tk.IntVar): Number of clusters to create
        current_clusters (List[Any]): Current document clusters from analysis
    """
    
    def __init__(self, parent, **kwargs) -> None:
        """Initialize DocumentMergeTab"""
        self.selected_document_folder: Optional[str] = None
        self.num_clusters: tk.IntVar = tk.IntVar(value=3)
        self.current_clusters: List[Any] = []
        
        # UI component references (set in setup_tab)
        self.document_folder_label: Optional[Label] = None
        self.cluster_spinbox: Optional[Spinbox] = None
        self.analyze_documents_button: Optional[Button] = None
        self.progress_tracker: Optional[Any] = None
        self.clusters_canvas: Optional[tk.Canvas] = None
        self.clusters_scrollbar: Optional[tk.Scrollbar] = None
        self.clusters_scrollable_frame: Optional[Frame] = None
        self.no_clusters_label: Optional[Label] = None
        
        super().__init__(parent, **kwargs)
    
    def setup_tab(self) -> None:
        """Setup the document merge tab UI"""
        # Header section
        self._create_header_section()
        
        # Folder selection section
        self._create_folder_selection_section()
        
        # Clustering settings
        self._create_clustering_settings_section()
        
        # Progress tracker
        self.progress_tracker = self.create_progress_section()
        self.progress_tracker.pack(fill=X, pady=(0, 10))
        
        # Cluster results area (scrollable)
        self._create_results_section()
    
    def _create_header_section(self) -> None:
        """Create the header section with title and description"""
        merge_header_frame = Frame(self)
        merge_header_frame.pack(fill=X, pady=(0, 10))

        merge_title = Label(
            merge_header_frame, 
            text="📄 Document Clustering & Merge", 
            font=("TkDefaultFont", 12, "bold")
        )
        merge_title.pack(anchor="w")

        merge_subtitle = Label(
            merge_header_frame, 
            text="Semantically cluster and merge related documents using AI", 
            font=("TkDefaultFont", 9)
        )
        merge_subtitle.pack(anchor="w")

        # Supported formats info
        formats_text = self._get_supported_formats_text()
        formats_label = Label(
            merge_header_frame, 
            text=formats_text, 
            font=("TkDefaultFont", 8), 
            foreground="gray"
        )
        formats_label.pack(anchor="w")
    
    def _get_supported_formats_text(self) -> str:
        """
        Get supported document formats text with local import
        
        Returns:
            Formatted string of supported file types
        """
        try:
            # Local import to avoid circular dependencies
            from document_merger import get_supported_document_types
            formats = get_supported_document_types()
            return f"Supported: {', '.join(formats)}"
        except ImportError:
            return "Supported: PDF, Word, Text, Markdown, Code files"
    
    def _create_folder_selection_section(self) -> None:
        """Create the folder selection section"""
        folder_section = Frame(self)
        folder_section.pack(fill=X, pady=(0, 10))

        folder_buttons_frame = Frame(folder_section)
        folder_buttons_frame.pack(fill=X, pady=(0, 5))

        select_folder_btn = Button(
            folder_buttons_frame, 
            text="Select Document Folder", 
            command=self.select_document_folder
        )
        select_folder_btn.pack(side=LEFT, padx=(0, 10))

        check_config_btn = Button(
            folder_buttons_frame, 
            text="Check Configuration", 
            bootstyle="info-outline", 
            command=self.check_merge_config
        )
        check_config_btn.pack(side=LEFT, padx=(0, 10))

        clear_folder_btn = Button(
            folder_buttons_frame, 
            text="Clear Folder", 
            bootstyle="secondary-outline", 
            command=self.clear_document_folder
        )
        clear_folder_btn.pack(side=LEFT)

        self.document_folder_label = Label(
            folder_section, 
            text="No document folder selected", 
            anchor="w"
        )
        self.document_folder_label.pack(fill=X)
    
    def _create_clustering_settings_section(self) -> None:
        """Create the clustering settings section"""
        settings_frame = Frame(self)
        settings_frame.pack(fill=X, pady=(0, 10))

        Label(settings_frame, text="Number of clusters:").pack(side=LEFT)
        
        self.cluster_spinbox = Spinbox(
            settings_frame, 
            from_=2, 
            to=20, 
            textvariable=self.num_clusters, 
            width=5
        )
        self.cluster_spinbox.pack(side=LEFT, padx=(5, 10))

        auto_clusters_btn = Button(
            settings_frame, 
            text="Auto", 
            bootstyle="secondary-outline", 
            command=self.auto_detect_clusters
        )
        auto_clusters_btn.pack(side=LEFT, padx=(0, 10))

        self.analyze_documents_button = Button(
            settings_frame, 
            text="🔍 Analyze Documents", 
            bootstyle="primary", 
            command=self.analyze_documents
        )
        self.analyze_documents_button.pack(side=LEFT, padx=(10, 0))
    
    def _create_results_section(self) -> None:
        """Create the scrollable cluster results section"""
        results_label = Label(self, text="Cluster Analysis Results:")
        results_label.pack(anchor="w", pady=(10, 5))

        # Create scrollable frame for cluster cards
        self.clusters_canvas = tk.Canvas(self, height=400)
        self.clusters_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.clusters_canvas.yview)
        self.clusters_scrollable_frame = Frame(self.clusters_canvas)

        self.clusters_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.clusters_canvas.configure(scrollregion=self.clusters_canvas.bbox("all"))
        )

        self.clusters_canvas.create_window((0, 0), window=self.clusters_scrollable_frame, anchor="nw")
        self.clusters_canvas.configure(yscrollcommand=self.clusters_scrollbar.set)

        self.clusters_canvas.pack(side="left", fill="both", expand=True)
        self.clusters_scrollbar.pack(side="right", fill="y")

        # Initially show placeholder
        self._show_placeholder()

    def select_document_folder(self) -> None:
        """Select folder containing documents to analyze"""
        folder_path = self.select_directory(title="Select Folder with Documents to Cluster")
        if folder_path:
            self.selected_document_folder = folder_path
            folder_name = os.path.basename(folder_path)
            if self.document_folder_label:
                self.document_folder_label.config(text=f"Selected: {folder_name} ({folder_path})")
            if self.progress_tracker:
                self.progress_tracker.update_message(f"Selected document folder: {folder_path}")
            # Clear any existing clusters
            self._clear_cluster_display()
        else:
            if self.progress_tracker:
                self.progress_tracker.update_message("No folder selected.")

    def check_merge_config(self) -> None:
        """Check if document merger is properly configured"""
        try:
            # Local import to avoid startup dependencies
            from document_merger import check_document_merger_config
            success, message = check_document_merger_config()
            if self.progress_tracker:
                self.progress_tracker.update_message(f"Configuration Check: {message}")
        except ImportError:
            if self.progress_tracker:
                self.progress_tracker.update_message("Configuration error: document_merger module not available")
        except Exception as e:
            if self.progress_tracker:
                self.progress_tracker.update_message(f"Configuration error: {str(e)}")

    def clear_document_folder(self) -> None:
        """Clear the selected document folder"""
        self.selected_document_folder = None
        if self.document_folder_label:
            self.document_folder_label.config(text="No document folder selected")
        if self.progress_tracker:
            self.progress_tracker.update_message("Document folder selection cleared.")
        self._clear_cluster_display()

    def auto_detect_clusters(self) -> None:
        """Automatically detect optimal number of clusters"""
        self.num_clusters.set(0)  # 0 means auto-detect
        if self.progress_tracker:
            self.progress_tracker.update_message("Set to auto-detect optimal number of clusters.")

    def analyze_documents(self) -> None:
        """Analyze and cluster documents in the selected folder"""
        if not self.selected_document_folder:
            if self.progress_tracker:
                self.progress_tracker.update_message("❌ No document folder selected. Please select a folder first.")
            return

        if self.progress_tracker:
            self.progress_tracker.start_progress("🔍 Starting document analysis and clustering...")

        # Disable button during processing
        if self.analyze_documents_button:
            self.analyze_documents_button.config(state="disabled", text="Analyzing...")

        # Use after to run analysis in background (pseudo-threading for demo)
        self.after(100, self._run_document_analysis)

    def _run_document_analysis(self) -> None:
        """Run the actual document analysis with local imports"""
        try:
            # Local import to avoid startup dependencies
            from document_merger import analyze_documents_in_folder
            
            num_clusters = self.num_clusters.get() if self.num_clusters.get() > 0 else None
            
            success, clusters, message = analyze_documents_in_folder(
                self.selected_document_folder, 
                num_clusters
            )
            
            if success:
                self.current_clusters = clusters
                self._display_clusters(clusters)
                if self.progress_tracker:
                    self.progress_tracker.stop_progress(f"✅ {message}")
            else:
                if self.progress_tracker:
                    self.progress_tracker.stop_progress(f"❌ Analysis failed: {message}")
                self._clear_cluster_display()
                
        except ImportError:
            if self.progress_tracker:
                self.progress_tracker.stop_progress("❌ Document merger module not available")
            self._clear_cluster_display()
        except Exception as e:
            if self.progress_tracker:
                self.progress_tracker.stop_progress(f"❌ Unexpected error during analysis: {str(e)}")
            self._clear_cluster_display()
        
        finally:
            # Re-enable the analyze button
            if self.analyze_documents_button:
                self.analyze_documents_button.config(state="normal", text="🔍 Analyze Documents")

    def _display_clusters(self, clusters: List[Any]) -> None:
        """
        Display clusters in the scrollable area using cluster cards
        
        Args:
            clusters: List of document cluster objects to display
        """
        # Clear existing display
        self._clear_cluster_display()
        
        if not clusters:
            self._show_no_results()
            return
        
        # Create cluster cards
        for i, cluster in enumerate(clusters):
            cluster_card = ClusterCard(
                self.clusters_scrollable_frame,
                cluster,
                self._handle_cluster_action,
                bootstyle="info",
                padding=10
            )
            cluster_card.pack(fill=X, padx=5, pady=5)
        
        # Update scroll region
        if self.clusters_scrollable_frame and self.clusters_canvas:
            self.clusters_scrollable_frame.update_idletasks()
            self.clusters_canvas.configure(scrollregion=self.clusters_canvas.bbox("all"))

    def _clear_cluster_display(self) -> None:
        """Clear all cluster cards from display"""
        if self.clusters_scrollable_frame:
            for widget in self.clusters_scrollable_frame.winfo_children():
                widget.destroy()
        self._show_placeholder()

    def _show_placeholder(self) -> None:
        """Show placeholder message when no clusters are displayed"""
        if self.clusters_scrollable_frame:
            self.no_clusters_label = Label(
                self.clusters_scrollable_frame, 
                text="No clusters to display. Select a folder and analyze documents to see results here.",
                font=("TkDefaultFont", 9),
                foreground="gray"
            )
            self.no_clusters_label.pack(pady=20)

    def _show_no_results(self) -> None:
        """Show no results message"""
        if self.clusters_scrollable_frame:
            no_results_label = Label(
                self.clusters_scrollable_frame,
                text="No clusters found. Try adjusting the number of clusters or check document similarity.",
                font=("TkDefaultFont", 9),
                foreground="gray"
            )
            no_results_label.pack(pady=20)

    def _handle_cluster_action(self, cluster: Any, action: str, custom_name: Optional[str]) -> None:
        """
        Handle actions from cluster cards
        
        Args:
            cluster: The cluster object from the action
            action: Action type ("merge", "preview", "skip")
            custom_name: Custom merge name if provided
        """
        if action == "merge":
            self._perform_cluster_merge(cluster, custom_name)
        elif action == "preview":
            self._show_cluster_preview(cluster)
        elif action == "skip":
            if self.progress_tracker:
                self.progress_tracker.update_message(f"Skipped Cluster {cluster.cluster_id + 1}")

    def _perform_cluster_merge(self, cluster: Any, custom_name: Optional[str]) -> None:
        """
        Actually perform the merge operation with local imports
        
        Args:
            cluster: Cluster object to merge
            custom_name: Custom filename for merged output
        """
        # Ask user where to save the merged file
        output_dir = self.select_directory(
            title="Select Output Directory for Merged File",
            initial_dir=self.selected_document_folder
        )
        
        if not output_dir:
            if self.progress_tracker:
                self.progress_tracker.update_message("Merge cancelled - no output directory selected.")
            return
        
        try:
            # Local import to avoid startup dependencies
            from document_merger import merge_document_cluster
            
            if self.progress_tracker:
                self.progress_tracker.start_progress(f"Merging Cluster {cluster.cluster_id + 1}...")
            
            success, output_path, message = merge_document_cluster(cluster, output_dir, custom_name)
            
            if success:
                if self.progress_tracker:
                    self.progress_tracker.stop_progress(f"✅ {message}")
                # Offer to open the merged file
                if self.ask_yes_no("Merge Complete", f"{message}\n\nWould you like to open the merged file?"):
                    self.open_file(output_path)
            else:
                if self.progress_tracker:
                    self.progress_tracker.stop_progress(f"❌ Merge failed: {message}")
                
        except ImportError:
            if self.progress_tracker:
                self.progress_tracker.stop_progress("❌ Document merger module not available")
        except Exception as e:
            if self.progress_tracker:
                self.progress_tracker.stop_progress(f"❌ Error during merge: {str(e)}")

    def _show_cluster_preview(self, cluster: Any) -> None:
        """
        Show a detailed preview of the cluster merge in a popup window
        
        Args:
            cluster: Cluster object to preview
        """
        preview_window = tk.Toplevel(self)
        preview_window.title(f"Cluster {cluster.cluster_id + 1} Preview")
        preview_window.geometry("800x600")
        
        # Create text widget with scroll
        text_frame = Frame(preview_window)
        text_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        from ttkbootstrap import Text, Scrollbar
        preview_text = Text(text_frame, wrap="word")
        preview_scroll = Scrollbar(text_frame, command=preview_text.yview)
        preview_text.config(yscrollcommand=preview_scroll.set)
        
        preview_text.pack(side=LEFT, fill=BOTH, expand=YES)
        preview_scroll.pack(side=RIGHT, fill=Y)
        
        # Load content
        if hasattr(cluster, 'merge_preview') and cluster.merge_preview:
            preview_text.insert("1.0", cluster.merge_preview)
        else:
            preview_text.insert("1.0", "Preview not available. Try generating the merge first.")
        
        preview_text.config(state="disabled")
        
        # Close button
        Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=5)

    def get_merge_info(self) -> Dict[str, Union[bool, str, int]]:
        """
        Get information about the current merge state
        
        Returns:
            Dictionary containing merge state information
        """
        return {
            'folder_selected': self.selected_document_folder is not None,
            'folder_path': self.selected_document_folder or "",
            'num_clusters_setting': self.num_clusters.get(),
            'clusters_found': len(self.current_clusters)
        }
    
    def get_selected_folder(self) -> Optional[str]:
        """
        Get the currently selected document folder
        
        Returns:
            Path to selected folder or None if no folder selected
        """
        return self.selected_document_folder
    
    def get_cluster_count(self) -> int:
        """
        Get the number of clusters found in last analysis
        
        Returns:
            Number of clusters from last analysis
        """
        return len(self.current_clusters)
    
    def reset_analysis(self) -> None:
        """Reset the analysis state and clear all clusters"""
        self.current_clusters = []
        self._clear_cluster_display()
        if self.progress_tracker:
            self.progress_tracker.reset()