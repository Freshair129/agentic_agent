import sys
import yaml
from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

# Add root to path for tools
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from capabilities.tools.logger import safe_print
from operation_system.identity_manager import IdentityManager

# Import Logic Module
from .Module.psych_engine.matrix_psych_module import MatrixPsychModule

class EVAMatrixSystem:
    """
    System: EVA Matrix System
    Role: Authority for Psychological State (9D Matrix)
    Responsibility: Owns state, manages persistence, and subscribes to Bus. Delegates logic to MatrixPsychModule.
    """
    def __init__(self, base_path: Path = None, msp=None, bus=None):
        self.base_path = base_path or Path(".")
        self.msp = msp
        self.bus = bus
        
        # 1. Load Configuration
        self.config_path = self.base_path / "eva_matrix/configs/EVA_Matrix_configs.yaml"
        self.config = self._load_config()
        
        # 2. Setup Files
        persistence_subpath = self.config.get("runtime_hook", {}).get("persistence_file", "consciousness/state_memory/eva_matrix_state.json")
        self.state_file = self.base_path / Path(persistence_subpath)
        
        # 3. Owned State
        self.axes_9d = {
            "stress": 0.5, "warmth": 0.5, "drive": 0.5, "clarity": 0.5, "joy": 0.5,
            "stability": 0.5, "orientation": 0.5,
            "primary": "Neutral", "secondary": "Neutral"
        }
        self.momentum = {"intensity": 0.1}
        self.emotion_label = "Neutral"

        self._load_state()
        
        # 4. Initialize Logic Module
        self.psych_module = MatrixPsychModule(self.config)
        
        # 5. Subscribe to physical stream
        if self.bus:
            self.bus.subscribe(IdentityManager.BUS_PHYSICAL, self._on_physical_signal)
            
        safe_print(f"[EVA Matrix System] Initialized (5+2+2 Model)")

    def _load_config(self) -> Dict[str, Any]:
        """Loads YAML configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def _on_physical_signal(self, payload: Dict[str, Any]):
        """Handler for 'bus:physical' signals (from PhysioController)."""
        neural_signals = payload.get("receptor_signals", {})
        if neural_signals:
            self.process_signals(signals=neural_signals)
    
    def process_signals(self, signals: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Process neural signals via Psych Module and update System state.
        """
        # 1. Pull from MSP if signals not provided
        if signals is None and self.msp:
            signals = self.msp.get_active_state("neural_signals") or {}

        # 2. Delegate Calculation to Module
        result = self.psych_module.process_signals(self.axes_9d, self.momentum, signals or {})

        # 3. Update internal state (System Authority)
        self.axes_9d = result.get("axes_9d", {})
        self.emotion_label = result.get("emotion_label", "Neutral")
        self.momentum = result.get("momentum", {})

        # 4. Push to MSP
        if self.msp:
            self.msp.set_active_state("matrix_state", {
                "axes_9d": self.axes_9d,
                "emotion_label": self.emotion_label,
                "momentum": self.momentum,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self.msp.set_active_state("reflex_directives", result.get("reflex_directives", {}))

        # 5. Publish to Bus
        if self.bus:
            self.bus.publish(IdentityManager.BUS_PSYCHOLOGICAL, {
                "matrix_state": {
                    "axes_9d": self.axes_9d,
                    "emotion_label": self.emotion_label,
                    "momentum": self.momentum
                },
                "reflex_directives": result.get("reflex_directives", {}),
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        self._save_state()
        return result

    def _save_state(self):
        """Saves current state to persistence file."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "axes_9d": self.axes_9d,
                "momentum": self.momentum,
                "emotion_label": self.emotion_label,
                "last_update": datetime.now(timezone.utc).isoformat()
            }
            self.state_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            safe_print(f"[EVA Matrix System] Error saving state: {e}")

    def _load_state(self):
        """Loads state from persistence file."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self.axes_9d = data.get("axes_9d", self.axes_9d)
                self.momentum = data.get("momentum", self.momentum)
                self.emotion_label = data.get("emotion_label", self.emotion_label)
            except Exception as e:
                safe_print(f"[EVA Matrix System] Error loading state: {e}")

