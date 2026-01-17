
"""
ChromaDB Bridge for EVA 9.1.0
Provides local vector storage using ChromaDB and Sentence-Transformers (Offline & Multilingual).
"""

import chromadb
import uuid
import os
from typing import List, Dict, Any, Optional

class ChromaVectorBridge:
    def __init__(self, persistence_path: str = "eva/memory/vector_store", collection_name: str = "eva_memories"):
        """
        Initialize ChromaDB Client and Sentence Transformer Model.
        """
        # 1. Initialize Vector DB
        self.base_path = os.path.abspath(persistence_path)
        print(f"[ChromaBridge] Connecting to Local Vector DB at: {self.base_path}")
        
        try:
            self.client = chromadb.PersistentClient(path=self.base_path)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"[ChromaBridge] Connected DB. Count: {self.collection.count()}")
        except Exception as e:
            print(f"[ChromaBridge] DB Connection Failed: {e}")
            raise e

        # 2. Initialize Model (Lazy load)
        print("[ChromaBridge] Loading Embedding Model: intfloat/multilingual-e5-base ...")
        try:
            from sentence_transformers import SentenceTransformer
            # Use 'intfloat/multilingual-e5-base' for best Thai support
            self.model = SentenceTransformer('intfloat/multilingual-e5-base')
            print("[ChromaBridge] [SUCCESS] Embedding Model Loaded.")
        except ImportError:
            print("[ChromaBridge] [FAILED] 'sentence-transformers' not installed. Please run: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            print(f"[ChromaBridge] [FAILED] Failed to load model: {e}")
            self.model = None

    def _get_embedding(self, text: str, is_query: bool = False) -> List[float]:
        """
        Generate embedding vector using local model.
        Prefixes are handled here for e5 models.
        """
        if not self.model:
            return []
            
        try:
            # e5 models need prefix
            prefix = "query: " if is_query else "passage: "
            input_text = prefix + text
            
            # Generate
            vector = self.model.encode(input_text, normalize_embeddings=True)
            return vector.tolist()
            
        except Exception as e:
            print(f"[ChromaBridge] Embedding Error: {e}")
            return []

    def add_memory(self, text: str, metadata: Dict[str, Any], memory_id: Optional[str] = None):
        """
        Embed and save a memory snippet.
        """
        if not text: return
            
        vector = self._get_embedding(text, is_query=False)
        if not vector:
            return

        mid = memory_id or str(uuid.uuid4())
        
        # Normalize metadata (Chroma doesn't support lists)
        clean_metadata = {}
        for k, v in metadata.items():
            if isinstance(v, (list, tuple)):
                clean_metadata[k] = ", ".join(map(str, v))
            else:
                clean_metadata[k] = v

        try:
            self.collection.add(
                documents=[text],
                embeddings=[vector],
                metadatas=[clean_metadata],
                ids=[mid]
            )
        except Exception as e:
            print(f"[ChromaBridge] Save Error: {e}")

    def query_memory(self, query_text: str, n_results: int = 5, where: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Semantic search for memories.
        """
        vector = self._get_embedding(query_text, is_query=True)
        if not vector: return []

        try:
            results = self.collection.query(
                query_embeddings=[vector],
                n_results=n_results,
                where=where
            )
            
            # Format results
            formatted = []
            if results["ids"]:
                for i in range(len(results["ids"][0])):
                    item = {
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if results["distances"] else 0.0
                    }
                    formatted.append(item)
            
            return formatted
            
        except Exception as e:
            print(f"[ChromaBridge] Query Error: {e}")
            return []

    def count(self):
        return self.collection.count()
