import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import datetime

class JournalNode:
    """
    Node responsible for physical I/O operations of episodic memory.
    Supports split storage (Full, User, LLM) and append-only logging.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.root_path = Path(".").resolve()
        
        # Resolve Node Parameters from Config
        node_cfg = config.get("module_definitions", {}).get("episodic_memory_module", {}).get("nodes", {}).get("journal_node", {})
        params = node_cfg.get("parameters", {})
        
        # Paths are relative to agent root
        self.episodes_path = self.root_path / params.get("episodes_root", "consciousness/episodic_memory/episodes")
        self.user_path     = self.root_path / params.get("user_root", "consciousness/episodic_memory/episodes_user")
        self.ai_path       = self.root_path / params.get("ai_root", "consciousness/episodic_memory/episodes_ai")
        self.log_filename  = params.get("log_file", "episodic_log.jsonl")
        
        # Storage structure for log resolution
        storage_cfg = config.get("storage_structure", {}).get("episodic", {})
        self.base_path = self.root_path / storage_cfg.get("path", "consciousness/episodic_memory")
        
        # Ensure directories exist
        self.episodes_path.mkdir(parents=True, exist_ok=True)
        self.user_path.mkdir(parents=True, exist_ok=True)
        self.ai_path.mkdir(parents=True, exist_ok=True)

    def write_split_episodes(self, episode_id: str, full_ep: Dict[str, Any], user_ep: Dict[str, Any], llm_ep: Dict[str, Any]) -> Dict[str, str]:
        """
        Writes the three-way split of an episode.
        """
        results = {}
        
        # 1. Full Episode
        full_file = self.episodes_path / f"{episode_id}.json"
        self._write_json(full_file, full_ep)
        results["full"] = str(full_file)
        
        # 2. User Episode
        user_file = self.user_path / f"{episode_id}_user.json"
        self._write_json(user_file, user_ep)
        results["user"] = str(user_file)
        
        # 3. LLM Episode
        llm_file = self.ai_path / f"{episode_id}_llm.json"
        self._write_json(llm_file, llm_ep)
        results["llm"] = str(llm_file)
        
        return results

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=self.config.get("global", {}).get("json_indent", 4), ensure_ascii=False)

    def append_to_log(self, episode_summary: Dict[str, Any]) -> None:
        """
        Appends a summary line to episodic log.
        """
        log_path = self.base_path / self.log_filename
        
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(episode_summary, ensure_ascii=False) + "\n")

    def read_log(self) -> List[Dict[str, Any]]:
        """
        Reads the episodic log and returns a list of summaries.
        """
        log_path = self.base_path / self.log_filename
        if not log_path.exists():
            return []
        
        summaries = []
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        summaries.append(json.loads(line))
                    except (json.JSONDecodeError, Exception):
                        continue
        return summaries

    def read_full_episode(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """
        Reads a full episode by ID.
        """
        path = self.episodes_path / f"{episode_id}.json"
        if not path.exists():
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return None

    def update_episode(self, episode_id: str, updated_data: Dict[str, Any]) -> bool:
        """
        Updates an existing episode (GSD: Belief Revision Support).
        """
        path = self.episodes_path / f"{episode_id}.json"
        if not path.exists():
            return False
        
        try:
            self._write_json(path, updated_data)
            return True
        except Exception:
            return False
