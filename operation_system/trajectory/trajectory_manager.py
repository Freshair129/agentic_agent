"""
TrajectoryManager System (v9.4.0)
Captures execution traces for debugging and analysis.

Logs:
- LLM calls (prompts, responses, tool decisions)
- Tool executions (args, results, errors)
- Decision points (context, choice, reasoning)
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from threading import Lock

class TrajectoryManager:
    """
    System: TrajectoryManager
    Role: Execution Trace Logger
    
    Captures the agent's decision-making process including:
    - LLM reasoning steps
    - Tool calls and outputs
    - System errors
    - Decision points
    """
    
    def __init__(self, config_path: Optional[str] = None):
        # Load config
        if config_path is None:
            config_path = Path(__file__).parent.parent / "configs" / "trajectory_config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # State
        self.enabled = self.config['logging']['enabled']
        self.current_session_id = None
        self.current_turn_index = 0
        self.trajectory_buffer: List[Dict] = []
        self._lock = Lock()
        
        # Ensure directory exists
        self.output_dir = Path(self.config['output']['directory'])
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def current_turn(self) -> Dict[str, Any]:
        """Return the current turn's trajectory data."""
        return {
            "session_id": self.current_session_id,
            "turn_index": self.current_turn_index,
            "steps": self.trajectory_buffer
        }
    
    def start_turn(self, session_id: str, turn_index: int):
        """Initialize a new turn for trajectory logging."""
        with self._lock:
            # Flush previous turn if exists
            if self.trajectory_buffer:
                self.flush_trajectory()
            
            self.current_session_id = session_id
            self.current_turn_index = turn_index
            self.trajectory_buffer = []
    
    def log_llm_call(self, prompt: str, response: str, tool_calls: Optional[List[Dict]] = None, 
                     metadata: Optional[Dict] = None):
        """Log an LLM inference call."""
        if not self.enabled or not self.config['logging']['capture']['llm_calls']:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "llm_call",
            "data": {
                "prompt_length": len(prompt),
                "response_length": len(response),
                "tool_calls": tool_calls or [],
                "metadata": metadata or {}
            }
        }
        
        # Store full text if verbosity is full
        if self.config['logging']['verbosity'] == 'full':
            entry["data"]["prompt"] = prompt
            entry["data"]["response"] = response
        
        with self._lock:
            self.trajectory_buffer.append(entry)
    
    def log_tool_execution(self, tool_name: str, args: Dict, result: Any = None, 
                          error: Optional[str] = None, duration_ms: Optional[float] = None):
        """Log a tool execution."""
        if not self.enabled or not self.config['logging']['capture']['tool_calls']:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "tool_call",
            "data": {
                "tool_name": tool_name,
                "args": args,
                "success": error is None,
                "error": error,
                "duration_ms": duration_ms
            }
        }
        
        # Include result if verbosity allows
        if self.config['logging']['verbosity'] in ['standard', 'full']:
            entry["data"]["result"] = str(result)[:500] if result else None
        
        with self._lock:
            self.trajectory_buffer.append(entry)
    
    def log_error(self, error_type: str, message: str, context: Optional[Dict] = None):
        """Log a system error."""
        if not self.enabled or not self.config['logging']['capture']['errors']:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "data": {
                "error_type": error_type,
                "message": message,
                "context": context or {}
            }
        }
        
        with self._lock:
            self.trajectory_buffer.append(entry)
    
    def log_decision(self, decision_point: str, choice: str, reasoning: str, 
                    alternatives: Optional[List[str]] = None):
        """Log a decision point."""
        if not self.enabled or not self.config['logging']['capture']['decisions']:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "decision",
            "data": {
                "decision_point": decision_point,
                "choice": choice,
                "reasoning": reasoning,
                "alternatives": alternatives or []
            }
        }
        
        with self._lock:
            self.trajectory_buffer.append(entry)
    
    def flush_trajectory(self):
        """Write buffered trajectory to file."""
        if not self.trajectory_buffer or not self.current_session_id:
            return
        
        # Generate filename
        filename_pattern = self.config['output']['filename_pattern']
        filename = filename_pattern.format(
            session_id=self.current_session_id,
            turn_index=self.current_turn_index
        )
        
        filepath = self.output_dir / filename
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in self.trajectory_buffer:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"[TrajectoryManager] Saved trajectory: {filepath}")
        
        # Clear buffer
        with self._lock:
            self.trajectory_buffer = []
    
    def get_recent_trajectories(self, limit: int = 10) -> List[Path]:
        """Get paths to recent trajectory files."""
        files = sorted(self.output_dir.glob("TRAJ_*.jsonl"), 
                      key=lambda p: p.stat().st_mtime, 
                      reverse=True)
        return files[:limit]
