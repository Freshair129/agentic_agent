import json
import hashlib
import os
from pathlib import Path
from typing import Dict, Optional, List, Any
import yaml

class EngramEngine:
    """
    Engram System (Conditional Memory Layer)
    
    Implements O(1) Scalable Lookup for frequent interaction patterns,
    bypassing heavy Vector/SLM inference.
    """

    def __init__(self, config_path: str = None):
        if not config_path:
            config_path = str(Path(__file__).parent / "configs" / "engram_config.yaml")

        self.config = self._load_config(config_path)
        self.enabled = self.config.get("engram_system", {}).get("enabled", True)
        
        self.params = self.config.get("engram_system", {}).get("parameters", {})
        self.ngram_size = self.params.get("ngram_size", 4)
        self.min_conf = self.params.get("min_confidence", 0.95)

        # Storage setup
        storage_cfg = self.config.get("engram_system", {}).get("storage", {})
        self.store_path = Path(__file__).parent / storage_cfg.get("path", "data/engram_store.json")
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.memory_table = self._load_memory()

    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ [Engram] Config load failed: {e}")
            return {}

    def _load_memory(self) -> Dict:
        if not self.store_path.exists():
            return {}
        try:
            with open(self.store_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_memory(self):
        try:
            with open(self.store_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory_table, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ [Engram] Save failed: {e}")

    def _hash_text(self, text: str) -> str:
        """Create a deterministic hash from normalized text."""
        normalized = text.strip().lower() # Simple normalization
        return hashlib.sha256(normalized.encode()).hexdigest()

    def lookup(self, text: str) -> Optional[Dict]:
        """
        O(1) Lookup for exact pattern matches.
        Returns the cached memory object if found.
        """
        if not self.enabled:
            return None

        # 1. Exact Match Check
        key_hash = self._hash_text(text)
        if key_hash in self.memory_table:
            return self.memory_table[key_hash]

        # 2. (Future) N-gram Check could go here
        return None

    def memorize(self, text: str, context_data: Dict, confidence: float) -> bool:
        """
        Conditionally memorize valid interactions.
        Only stores if confidence > threshold.
        """
        if not self.enabled or confidence < self.min_conf:
            return False

        key_hash = self._hash_text(text)
        
        # Don't overwrite unless significantly better (logic can be expanded)
        if key_hash in self.memory_table:
            return False 

        entry = {
            "text": text,
            "context_data": context_data, # Should include intent, emotional_signal, etc.
            "confidence": confidence,
            "hits": 0
        }
        
        self.memory_table[key_hash] = entry
        self._save_memory()
        return True
