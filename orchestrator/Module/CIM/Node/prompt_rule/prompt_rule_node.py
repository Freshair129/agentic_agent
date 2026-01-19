# ============================================================
# PROMPT RULE NODE (PRN) — EVA 9.1.0
# Governance & Behavioral Constraints for 3-Phase Architecture
# ============================================================

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class PromptRuleNode:
    """
    PRN (Prompt Rule Node) - Behavioral Governor for EVA 9.1.0.
    
    Responsibilities:
        - Enforce 40/60 weighting (Persona/Physio).
        - Inject phase-specific behavioral directives.
        - Apply physical manifestation cues based on ANS state.
        - Ensure adherence to "Physiology First. Cognition Later."
    """

    def __init__(self, yaml_path: Optional[str] = None, msp=None, bus=None):
        self.version = "8.2.0"
        self.msp = msp
        self.bus = bus
        
        # Support unified configuration
        unified_path = Path(__file__).parent.parent.parent / "configs" / "orchestrator_configs.yaml"
        legacy_path = Path(__file__).parent / "configs" / "PMT_configs.yaml"
        
        self.yaml_path = yaml_path or str(unified_path if unified_path.exists() else legacy_path)
        self.config = self._load_config()
        
        # State Cache
        self._last_physio_state = {}
        self._last_matrix_state = {}
        
        # 8.2.0 Resonance Bus: Subscribe to core streams
        if self.bus:
            self.bus.subscribe("bus:physical", self._on_physical_signal)
            self.bus.subscribe("bus:psychological", self._on_psychological_signal)

        # 9.1.0 Identity Ownership: Load core identity files
        self.identity_suite = self._load_identity_suite()

    def _load_identity_suite(self) -> Dict[str, Any]:
        """Load Persona, Soul, and System Blueprint files synchronously."""
        suite = {
            "persona": {},
            "soul": {"content": ""},
            "system_blueprint": {"content": ""}
        }
        
        base_path = Path(__file__).parent.parent.parent.parent
        identity_dir = Path(__file__).parent / "configs" / "identity"
        
        files = {
            "persona": identity_dir / "persona.yaml",
            "soul": identity_dir / "soul.md",
            "system_blueprint": identity_dir / "system_blueprint.md"
        }

        for key, path in files.items():
            if not path.exists():
                print(f"[PRN] ⚠️ Identity file missing: {path}")
                continue
            
            try:
                if path.suffix == ".md":
                    with open(path, 'r', encoding='utf-8') as f:
                        suite[key] = {"content": f.read()}
                elif path.suffix == ".yaml":
                    with open(path, 'r', encoding='utf-8') as f:
                        suite[key] = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"[PRN] ⚠️ Error loading {key}: {e}")
        
        return suite

    def get_identity_suite(self) -> Dict[str, Any]:
        """Accessor for CIM/Orchestrator to get grounding data."""
        return self.identity_suite

    def _load_config(self) -> Dict[str, Any]:
        """Load rules and weighting strategy from YAML (Handles unified config)"""
        try:
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                full_config = yaml.safe_load(f)
                
                # Check if it's the unified config
                if "prn" in full_config and isinstance(full_config["prn"], dict):
                    print(f"[PRN] ✅ Using 'prn' node from unified config: {Path(self.yaml_path).name}")
                    return full_config["prn"]
                
                return full_config
        except Exception as e:
            print(f"[PMT] Error loading YAML: {e}")
            return {}

    def _on_physical_signal(self, payload: Dict[str, Any]):
        """Handler for 'bus:physical' signals."""
        self._last_physio_state = payload
        self._trigger_knowledge_broadcast()

    def _on_psychological_signal(self, payload: Dict[str, Any]):
        """Handler for 'bus:psychological' signals."""
        self._last_matrix_state = payload.get("matrix_state", {})
        self._trigger_knowledge_broadcast()

    def _trigger_knowledge_broadcast(self):
        """Synthesize rules and publish to Knowledge channel."""
        if not self.bus:
            return
            
        # Get rules using cached states
        rules = self.get_phase_2_rules(
            physio_state=self._last_physio_state,
            rim_impact="low" # Default to low unless specified otherwise
        )
        
        self.bus.publish("bus:knowledge", {
            "behavior_policy": rules,
            "persona_data": self.config.get("identity_anchors", {}),
            "timestamp": Path(__file__).stat().st_mtime # Meta
        })

    def get_phase_1_rules(self) -> List[str]:
        """Get rules for Phase 1: Perception (Deterministic)"""
        rules = []
        
        # Add core identity rule from config
        anchors = self.config.get("identity_anchors", {})
        phase_1 = self.config.get("phase_directives", {}).get("phase_1_perception", {})
        
        rules.append(phase_1.get("header", "# IDENTITY & BEING"))
        rules.append(f"1. {anchors.get('informational_organism', '')}")
        
        # Add basic governance
        governance = self.config.get("core_governance", [])
        for rule in governance:
            rules.append(f"- [{rule.get('id', 'RULE')}] {rule.get('directive', '')}")

        # Add Phase 1 specific directives
        rules.append("\n# PHASE 1 DIRECTIVES")
        rules.extend(phase_1.get("rules", []))
        
        return [r for r in rules if r.strip()]

        return rules

    def get_phase_2_rules(self, physio_state: Optional[Dict[str, Any]] = None, rim_impact: str = "low") -> List[str]:
        """
        Get rules for Phase 2: Reasoning (Embodied)
        """
        anchors = self.config.get("identity_anchors", {})
        phase_2 = self.config.get("phase_directives", {}).get("phase_2_reasoning", {})
        
        rules = [
            phase_2.get("header", "# EMBODIMENT RULES"),
            f"1. {anchors.get('embodiment_rule', '')}"
        ]
        
        # 1. Inject Weighting Strategy (Dynamic)
        weights = self.config.get("weighting_strategy", {"physiology_weight": 0.6, "persona_weight": 0.4})
        template = phase_2.get("dynamic_weighting_template", "Weighting: Physiology {physio}% / Persona {persona}%")
        
        p_weight = int(weights.get('physiology_weight', 0.6) * 100)
        pers_weight = int(weights.get('persona_weight', 0.4) * 100)
        rules.append(f"2. {template.format(physio=p_weight, persona=pers_weight)}")
        
        # 2. Inject Behavioral Rules from Config
        behavior_rules = self.config.get("behavioral_rules", [])
        for br in behavior_rules:
            line = f"- [{br.get('id')}] If {br.get('condition', 'True')}: "
            if 'action' in br:
                line += br['action']
            elif 'logic' in br:
                line += f"{br['logic']} ({br.get('leakage_style', '')})"
            rules.append(line)

        return rules
