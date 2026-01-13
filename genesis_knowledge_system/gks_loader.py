import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class GKSLoader:
    """
    Genesis Knowledge System (GKS) Loader
    Loads the 7 Master/Genesis JSON Blocks into runtime memory.
    """
    
    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Default to current directory if not provided
            self.base_path = Path(__file__).parent
            
        self.master_block = {}
        self.genesis_blocks = {}
        self.safety_block = {}
        self._is_loaded = False

    def load_all(self) -> bool:
        """Loads all GKS blocks from disk."""
        try:
            # 1. Master Block
            self.master_block = self._load_json("Master_Block.json")
            
            # 2. Genesis Blocks (The 5 Ws + How)
            self.genesis_blocks = {
                "algorithm": self._load_json("Algorithm_How_Genesis_Block.json"),
                "concept": self._load_json("Concept_Why_Genesis_Block.json"),
                "framework": self._load_json("Framework_Genesis_Block.json"),
                "parameter": self._load_json("Parameter_What_Genesis_Block.json"),
                "protocol": self._load_json("Protocol_Process_Genesis_Block.json"),
                "time": self._load_json("Time_When_Genesis_Block.json")
            }
            
            # 3. Safety Block
            self.safety_block = self._load_json("Safety_Block.json")
            
            self._is_loaded = True
            print(f"[GKS] [OK] Loaded Knowledge Blocks from {self.base_path}")
            return True
            
        except Exception as e:
            print(f"[GKS] [FAIL] Failed to load blocks: {e}")
            self._is_loaded = False
            return False

    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Helper to load a single JSON file."""
        file_path = self.base_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"GKS Block not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_master_block(self) -> Dict[str, Any]:
        return self.master_block

    def get_genesis_block(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific Genesis Block.
        Category: 'algorithm', 'concept', 'framework', 'parameter', 'protocol', 'time'
        """
        return self.genesis_blocks.get(category.lower())

    def get_safety_block(self) -> Dict[str, Any]:
        return self.safety_block

    def query_concept(self, query: str) -> str:
        """
        Basic semantic search stub (to be upgraded with Vector Search later).
        Currently searches keys/descriptions in Concept & Framework blocks.
        """
        # TODO: Implement deeper search
        return f"GKS Query '{query}' functionality pending expansion."
