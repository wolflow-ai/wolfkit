# === document_merger.py ===
import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import docling
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentCluster:
    """Represents a cluster of related documents"""
    def __init__(self, cluster_id: int, documents: List[str], similarity_score: float):
        self.cluster_id = cluster_id
        self.documents = documents  # List of file paths
        self.similarity_score = similarity_score
        self.suggested_merge_name = self._generate_merge_name()
        self.merge_preview = None
        self.selected_documents = documents.copy()  # For custom selection
        
    def _generate_merge_name(self) -> str:
        """Generate a suggested name for the merged document"""
        # Extract common keywords from filenames
        basenames = [Path(doc).stem.lower() for doc in self.documents]
        common_words = set(basenames[0].split('_')) if basenames else set()
        
        for name in basenames[1:]:
            common_words &= set(name.split('_'))
        
        if common_words:
            # Remove common non-descriptive words that appear in many document types
            filtered_words = [w for w in common_words if w not in {
                'doc', 'document', 'file', 'pdf', 'docx', 'txt', 'md',
                'copy', 'final', 'draft', 'v1', 'v2', 'version', 'new', 'old',
                'temp', 'tmp', 'backup', 'bak', 'archive'
            }]
            if filtered_words:
                return f"merged_{'_'.join(sorted(filtered_words))}.md"
        
        # Extract potential topic words from filenames using common patterns
        topic_hints = []
        for doc in self.documents:
            name_lower = Path(doc).stem.lower()
            # Look for meaningful words that aren't common file descriptors
            words = name_lower.replace('-', '_').split('_')
            meaningful_words = [w for w in words if len(w) > 2 and w not in {
                'doc', 'document', 'file', 'pdf', 'docx', 'txt', 'md',
                'copy', 'final', 'draft', 'version', 'new', 'old', 'the', 'and', 'for'
            }]
            topic_hints.extend(meaningful_words)
        
        # Find most common meaningful word
        if topic_hints:
            from collections import Counter
            most_common = Counter(topic_hints).most_common(1)
            if most_common:
                return f"merged_{most_common[0][0]}_documents.md"
        
        # Final fallback
        return f"merged_cluster_{self.cluster_id}.md"
    
    def get_preview_text(self, max_length: int = 200) -> str:
        """Get a short preview of the merge content"""
        if not self.merge_preview:
            return "Preview not generated yet..."
        
        # Clean up markdown and get first meaningful text
        lines = self.merge_preview.split('\n')
        clean_text = ""
        
        for line in lines:
            # Skip markdown headers and empty lines
            if line.strip() and not line.startswith('#') and not line.startswith('**'):
                clean_text += line.strip() + " "
                if len(clean_text) > max_length:
                    break
        
        if len(clean_text) > max_length:
            return clean_text[:max_length] + "..."
        return clean_text or "Content preview available..."

class DocumentMerger:
    """Main class for document clustering and merging operations"""
    
    def __init__(self):
        self.client = None
        self.converter = DocumentConverter()
        self.documents_cache = {}  # Cache for processed documents
        self.current_clusters = []  # Store current analysis results
        
    def check_merger_config(self) -> Tuple[bool, str]:
        """Check if document merger is properly configured"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return False, "❌ No OpenAI API key found. Please add OPENAI_API_KEY to your .env file."
            
            self.client = OpenAI(api_key=api_key)
            
            # Test API connection with a simple embedding request
            test_response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input="test connection"
            )
            
            return True, "✅ Document merger ready! OpenAI API connected successfully."
            
        except Exception as e:
            return False, f"❌ Configuration error: {str(e)}"
    
    def scan_documents(self, folder_path: str) -> List[str]:
        """Scan folder for supported document types"""
        supported_extensions = {'.pdf', '.docx', '.doc', '.txt', '.md', '.py', '.js', '.html', '.css'}
        documents = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                # Skip common directories that don't contain documents
                dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.vscode', '.idea', 'venv', 'env'}]
                
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in supported_extensions:
                        documents.append(str(file_path))
            
            return sorted(documents)
            
        except Exception as e:
            print(f"Error scanning documents: {e}")
            return []
    
    def extract_document_content(self, file_path: str) -> Tuple[bool, str, str]:
        """Extract text content from various document types"""
        try:
            file_path = Path(file_path)
            
            # Check cache first
            file_hash = self._get_file_hash(file_path)
            if file_hash in self.documents_cache:
                return True, self.documents_cache[file_hash], "From cache"
            
            # Handle different file types
            if file_path.suffix.lower() in {'.txt', '.md', '.py', '.js', '.html', '.css'}:
                # Plain text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            elif file_path.suffix.lower() in {'.pdf', '.docx', '.doc'}:
                # Use Docling for complex documents
                result = self.converter.convert(str(file_path))
                content = result.document.export_to_markdown()
            
            else:
                return False, "", f"Unsupported file type: {file_path.suffix}"
            
            # Cache the result
            self.documents_cache[file_hash] = content
            
            return True, content, f"Extracted {len(content)} characters"
            
        except Exception as e:
            return False, "", f"Error extracting content: {str(e)}"
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file caching"""
        stat = file_path.stat()
        return hashlib.md5(f"{file_path}_{stat.st_mtime}_{stat.st_size}".encode()).hexdigest()
    
    def generate_embeddings(self, documents: List[str]) -> Tuple[bool, np.ndarray, List[str], str]:
        """Generate embeddings for document clustering"""
        try:
            if not self.client:
                return False, np.array([]), [], "OpenAI client not initialized"
            
            # Extract content from all documents
            contents = []
            valid_docs = []
            
            for doc_path in documents:
                success, content, _ = self.extract_document_content(doc_path)
                if success and content.strip():
                    # Truncate very long documents for embedding
                    truncated_content = content[:8000]  # ~8k chars for embedding
                    contents.append(truncated_content)
                    valid_docs.append(doc_path)
            
            if not contents:
                return False, np.array([]), [], "No valid document content found"
            
            # Generate embeddings in batches
            embeddings = []
            batch_size = 100  # OpenAI limit
            
            for i in range(0, len(contents), batch_size):
                batch = contents[i:i + batch_size]
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=batch
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            
            embeddings_array = np.array(embeddings)
            
            return True, embeddings_array, valid_docs, f"Generated embeddings for {len(valid_docs)} documents"
            
        except Exception as e:
            return False, np.array([]), [], f"Error generating embeddings: {str(e)}"
    
    def cluster_documents(self, documents: List[str], num_clusters: Optional[int] = None) -> Tuple[bool, List[DocumentCluster], str]:
        """Cluster documents based on semantic similarity"""
        try:
            if len(documents) < 2:
                return False, [], "Need at least 2 documents for clustering"
            
            # Generate embeddings
            success, embeddings, valid_docs, msg = self.generate_embeddings(documents)
            if not success:
                return False, [], msg
            
            # Determine optimal number of clusters
            if num_clusters is None:
                # Use elbow method or default to sqrt(n/2)
                num_clusters = max(2, min(len(valid_docs) // 3, int(np.sqrt(len(valid_docs) / 2))))
            
            # Ensure we don't have more clusters than documents
            num_clusters = min(num_clusters, len(valid_docs))
            
            # Perform clustering
            kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Calculate cluster similarities
            clusters = []
            for cluster_id in range(num_clusters):
                cluster_docs = [valid_docs[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
                
                if len(cluster_docs) > 1:  # Only include clusters with multiple documents
                    # Calculate average similarity within cluster
                    cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
                    cluster_embeddings = embeddings[cluster_indices]
                    
                    if len(cluster_embeddings) > 1:
                        similarity_matrix = cosine_similarity(cluster_embeddings)
                        avg_similarity = np.mean(similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)])
                    else:
                        avg_similarity = 1.0
                    
                    cluster = DocumentCluster(cluster_id, cluster_docs, avg_similarity)
                    clusters.append(cluster)
            
            # Store clusters for UI access
            self.current_clusters = clusters
            
            return True, clusters, f"Found {len(clusters)} clusters with {sum(len(c.documents) for c in clusters)} documents"
            
        except Exception as e:
            return False, [], f"Error during clustering: {str(e)}"
    
    def generate_merge_preview(self, cluster: DocumentCluster) -> Tuple[bool, str, str]:
        """Generate a preview of what the merged document would look like"""
        try:
            if not self.client:
                return False, "", "OpenAI client not initialized"
            
            # Use selected documents (allows for custom selection)
            documents_to_merge = cluster.selected_documents
            
            # Extract content from selected documents in cluster
            documents_content = []
            for doc_path in documents_to_merge:
                success, content, _ = self.extract_document_content(doc_path)
                if success:
                    doc_name = Path(doc_path).name
                    documents_content.append(f"=== {doc_name} ===\n{content}\n")
            
            if not documents_content:
                return False, "", "No content found in selected documents"
            
            # Create merge prompt
            combined_content = "\n".join(documents_content)
            
            prompt = f"""
You are a document merger. Please merge the following related documents into a single, coherent document.

Requirements:
1. Remove duplicate information
2. Organize content logically with clear headings
3. Preserve important details from all documents
4. Use Markdown formatting
5. Create a professional, well-structured document

Documents to merge:
{combined_content[:15000]}  # Limit content for API

Please provide the merged document:
"""
            
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.3
            )
            
            merged_content = response.choices[0].message.content
            cluster.merge_preview = merged_content
            
            return True, merged_content, f"Generated merge preview ({len(merged_content)} characters)"
            
        except Exception as e:
            return False, "", f"Error generating merge preview: {str(e)}"
    
    def perform_cluster_merge(self, cluster: DocumentCluster, output_path: str, custom_name: str = None) -> Tuple[bool, str, str]:
        """Actually perform the merge and save the result"""
        try:
            # Generate merge content if not already done
            if not cluster.merge_preview:
                success, _, msg = self.generate_merge_preview(cluster)
                if not success:
                    return False, "", f"Failed to generate merge content: {msg}"
            
            # Determine output filename
            if custom_name:
                filename = custom_name if custom_name.endswith('.md') else f"{custom_name}.md"
            else:
                filename = cluster.suggested_merge_name
            
            full_output_path = os.path.join(output_path, filename)
            
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Write merged content
            with open(full_output_path, 'w', encoding='utf-8') as f:
                f.write(cluster.merge_preview)
            
            return True, full_output_path, f"Successfully merged {len(cluster.selected_documents)} documents into {filename}"
            
        except Exception as e:
            return False, "", f"Error performing merge: {str(e)}"
    
    def save_merge_report(self, clusters: List[DocumentCluster], output_dir: str = "./reports") -> Tuple[bool, str, str]:
        """Save clustering and merge analysis report"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(output_dir, f"wolfkit_document_analysis_{timestamp}.md")
            
            report_content = f"""# Wolfkit Document Clustering Analysis
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Clusters Found:** {len(clusters)}
**Total Documents:** {sum(len(c.documents) for c in clusters)}

---

"""
            
            for i, cluster in enumerate(clusters, 1):
                report_content += f"""## Cluster {i} (Similarity: {cluster.similarity_score:.2%})

**Suggested Merge Name:** `{cluster.suggested_merge_name}`

**Documents in Cluster:**
"""
                for doc in cluster.documents:
                    report_content += f"- {Path(doc).name}\n"
                
                report_content += f"\n**Merge Preview:**\n```markdown\n{cluster.merge_preview[:500] if cluster.merge_preview else 'No preview generated'}...\n```\n\n---\n\n"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return True, report_path, f"Analysis report saved to {report_path}"
            
        except Exception as e:
            return False, "", f"Error saving report: {str(e)}"

# === Integration Functions for Controller ===

def check_document_merger_config() -> Tuple[bool, str]:
    """Check if document merger is properly configured"""
    merger = DocumentMerger()
    return merger.check_merger_config()

def analyze_documents_in_folder(folder_path: str, num_clusters: Optional[int] = None) -> Tuple[bool, List[DocumentCluster], str]:
    """Analyze and cluster documents in a folder, return clusters for UI"""
    try:
        merger = DocumentMerger()
        
        # Check configuration
        config_ok, config_msg = merger.check_merger_config()
        if not config_ok:
            return False, [], config_msg
        
        # Scan documents
        documents = merger.scan_documents(folder_path)
        if not documents:
            return False, [], f"No supported documents found in {folder_path}"
        
        # Cluster documents
        success, clusters, cluster_msg = merger.cluster_documents(documents, num_clusters)
        if not success:
            return False, [], cluster_msg
        
        # Generate merge previews for each cluster
        for cluster in clusters:
            merger.generate_merge_preview(cluster)
        
        return True, clusters, f"Document analysis complete: {len(clusters)} clusters found"
        
    except Exception as e:
        return False, [], f"Error analyzing documents: {str(e)}"

def merge_document_cluster(cluster: DocumentCluster, output_path: str, custom_name: str = None) -> Tuple[bool, str, str]:
    """Merge a specific cluster and save the result"""
    merger = DocumentMerger()
    return merger.perform_cluster_merge(cluster, output_path, custom_name)

def get_supported_document_types() -> List[str]:
    """Get list of supported document file extensions"""
    return ['.pdf', '.docx', '.doc', '.txt', '.md', '.py', '.js', '.html', '.css']