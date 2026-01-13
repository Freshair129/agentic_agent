import json
from pathlib import Path
from typing import Dict, Any

class QualiaStorageNode:
    """
    Node responsible for persisting sensory metadata and feature vectors.
    Links sensory data to Episodic IDs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.root_path = Path(".").resolve()
        
        # Resolve Node Parameters
        node_cfg = config.get("module_definitions", {}).get("sensory_memory_module", {}).get("nodes", {}).get("qualia_storage_node", {})
        params = node_cfg.get("parameters", {})
        
        self.log_filename = params.get("log_file", "sensory_log.jsonl")
        
        storage_cfg = config.get("storage_structure", {}).get("sensory", {})
        self.base_path = self.root_path / storage_cfg.get("path", "consciousness/sensory_memory")
        
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write_sensory_record(self, sensory_data: Dict[str, Any]):
        """
        Appends sensory data to the sensory log.
        """
        log_path = self.base_path / self.log_filename
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(sensory_data, ensure_ascii=False) + "\n")
