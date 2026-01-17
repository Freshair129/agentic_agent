"""
Artifact Qualia System Engine (Independent Version: 2.4.3)
Phenomenological Experience Integrator with State Bus support.
"""

import sys
from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Add root to path for tools
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from capabilities.tools.logger import safe_print
from operation_system.identity_manager import IdentityManager

# Import Logic Module
from .Module.qualia_integrator.qualia_integrator_module import QualiaIntegratorModule, QualiaSnapshot

# =============================================================================
# Data Contracts
# =============================================================================

@dataclass
class RIMSemantic:
    impact_level: str              # low | medium | high
    impact_trend: str              # rising | stable | fading
    affected_domains: List[str]

# =============================================================================
# Artifact Qualia System
# =============================================================================

class ArtifactQualiaSystem:
    """
    System: Artifact Qualia System
    Role: Authority for Phenomenological Experience
    Responsibility: Owns state, manages persistence, and subscribes to Bus. Delegates logic to QualiaIntegratorModule.
    """

    def __init__(self, base_path: Path = None, msp=None, bus=None, config_path: str = None):
        self.base_path = base_path or Path(".")
        self.msp = msp
        self.bus = bus
        self.state_file = self.base_path / "system_state/artifact_qualia_state.json"
        
        # Load Configuration (SSOT)
        self.config = {}
        target_cfg = config_path or "artifact_qualia/configs/Artifact_Qualia_configs.yaml"
        full_cfg_path = self.base_path / target_cfg
        
        if full_cfg_path.exists():
            try:
                import yaml
                with open(full_cfg_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            except Exception as e:
                safe_print(f"[Artifact Qualia] ⚠️ Config load error: {e}")

        # Instance of Logic Module
        self.integrator = QualiaIntegratorModule(config=self.config)
        self.last_qualia: Optional[QualiaSnapshot] = None

        self._load_state()
        
        # 8.2.0 Resonance Bus: Subscribe to psychological stream
        if self.bus:
            self.bus.subscribe(IdentityManager.BUS_PSYCHOLOGICAL, self._on_psychological_signal)
            
        safe_print(f"[Artifact Qualia System] Initialized (Phenomenology Core - Config Driven)")

    def _on_psychological_signal(self, payload: Dict[str, Any]):
        """Handler for 'bus:psychological' signals (from EVA_Matrix)."""
        matrix_data = payload.get("matrix_state", {})
        if matrix_data:
            # Extract axes_9d for the core integrator
            axes = matrix_data.get("axes_9d", {})
            eva_state = {
                "baseline_arousal": axes.get("Alertness", 0.5),
                "emotional_tension": axes.get("Stress", 0.3),
                "coherence": axes.get("Groundedness", 0.6),
                "momentum": matrix_data.get("momentum", {}).get("total", 0.5),
                "calm_depth": axes.get("Openness", 0.4)
            }
            self.process_experience(eva_state=eva_state)

    def process_experience(
        self, 
        eva_state: Dict[str, float] = None, 
        rim_semantic: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Integrate psyche state via Module and Push to Bus.
        """
        # 1. PULL from State Bus if eva_state not provided
        if eva_state is None and self.msp:
            matrix_data = self.msp.get_active_state("matrix_state") or {}
            # Map axes_9d to expected flat dict
            axes = matrix_data.get("axes_9d", {})
            eva_state = {
                "baseline_arousal": axes.get("Alertness", 0.5),
                "emotional_tension": axes.get("Stress", 0.3),
                "coherence": axes.get("Groundedness", 0.6),
                "momentum": matrix_data.get("momentum", {}).get("total", 0.5),
                "calm_depth": axes.get("Openness", 0.4)
            }

        # 2. Default RIM Semantic if not provided
        if rim_semantic is None:
            rim_semantic = RIMSemantic(
                impact_level="low",
                impact_trend="stable",
                affected_domains=["ambient"]
            )
        else:
            rim_semantic = RIMSemantic(
                impact_level=rim_semantic.get("impact_level", "low"),
                impact_trend=rim_semantic.get("impact_trend", "stable"),
                affected_domains=rim_semantic.get("affected_domains", ["ambient"])
            )

        # 3. Process via Module
        self.last_qualia = self.integrator.integrate(eva_state, rim_semantic)

        # 4. PUSH to State Bus
        result_dict = {
            "intensity": float(self.last_qualia.intensity),
            "tone": str(self.last_qualia.tone),
            "coherence": float(self.last_qualia.coherence),
            "depth": float(self.last_qualia.depth),
            "texture": {k: float(v) for k, v in self.last_qualia.texture.items()},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if self.msp:
            self.msp.set_active_state("qualia_state", result_dict)

        # 8.2.0 Resonance Bus: Publish phenomenological state
        if self.bus:
            self.bus.publish(IdentityManager.BUS_PHENOMENOLOGICAL, {
                "qualia_snapshot": result_dict,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        self._save_state()
        return result_dict

    def get_full_state(self) -> Dict[str, Any]:
        """Return complete system state."""
        # Merge module state with system state
        state = self.integrator.get_internal_state()
        if self.last_qualia:
            state["last_snapshot"] = {
                "intensity": self.last_qualia.intensity,
                "tone": self.last_qualia.tone,
                "coherence": self.last_qualia.coherence,
                "depth": self.last_qualia.depth,
                "texture": self.last_qualia.texture
            }
        return state

    def _save_state(self):
        """Saves current state via System Authority."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            # Retrieve internal state from Module
            state_data = self.integrator.get_internal_state()
            state_data["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            safe_print(f"[Artifact Qualia System] Error saving state: {e}")

    def _load_state(self):
        """Load internal core state from persistence."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Inject state back into Module
                    self.integrator.set_state(
                        last_intensity=data.get("last_intensity", 0.3),
                        last_coherence=data.get("last_coherence", 0.6)
                    )
                    safe_print(f"[Artifact Qualia] Loaded state (Intensity: {data.get('last_intensity', 'N/A')})")
            except Exception as e:
                safe_print(f"[Artifact Qualia] Warning: Could not load state: {e}")


