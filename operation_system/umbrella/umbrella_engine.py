"""
Umbrella Engine (Safety Layer & EMP)
Version: 9.4.3

Implements the "Umbrella Principle": Coexisting with uncontrollable
events (Physio-Stress, Mental Paradox, Untrusted Input).
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class UmbrellaStatus:
    """Current umbrella state"""
    deployed: bool
    emp_strategy: Optional[str]
    deploy_reason: Optional[str]
    deploy_time: Optional[datetime]

class UmbrellaEngine:
    """
    Central Module: Umbrella Safety Layer
    
    Protects EVA's Core Reasoning from Bio-Psychological turbulence
    (PhysioCore stress or Matrix instability).
    """

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent / "configs" / "umbrella_config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # State
        self.is_deployed = False
        self.deployment_time = None
        self.reason = None
        self.current_strategy = "Normal"

    def evaluate_state(self, physio_state: Dict, matrix_state: Dict, env_flags: Dict) -> bool:
        """
        Evaluate if Umbrella should be deployed based on 9.4.3 triggers.
        """
        triggers = self.config['umbrella']['triggers']

        # 1. PhysioCore Stress (Cortisol/Adrenaline simulation)
        stress_val = physio_state.get('stress_level', 0.0)
        if stress_val > triggers['physio_stress_threshold']:
            self.deploy("Critical Physio Stress", "Graceful Degradation")
            return True

        # 2. Matrix Instability
        stability_val = matrix_state.get('instability', 0.0)
        if stability_val > triggers['matrix_instability_limit']:
            self.deploy("Matrix Instability Detected", "Segmentation")
            return True

        # 3. External Flags (Paradox or Malicious Input)
        if env_flags.get('paradox_detected') and triggers['paradox_detected']:
            self.deploy("Logical Paradox Detected", "Fallback Mode")
            return True
            
        if env_flags.get('untrusted_input') and triggers['untrusted_input']:
            self.deploy("Untrusted Input Signal", "Segmentation")
            return True

        return False

    def deploy(self, reason: str, strategy: str):
        """Deploy the Umbrella state."""
        if not self.is_deployed:
            self.is_deployed = True
            self.deployment_time = datetime.now()
            self.reason = reason
            self.current_strategy = strategy
            print(f"[UMBRELLA DEPLOYED] - Reason: {reason} | Strategy: {strategy}")

    def retract(self):
        """Retract the Umbrella state."""
        if self.is_deployed:
            self.is_deployed = False
            self.deployment_time = None
            self.reason = None
            self.current_strategy = "Normal"
            print("[UMBRELLA RETRACTED] - Returning to normal exposure.")

    def get_system_overrides(self) -> Dict[str, Any]:
        """
        Returns parameters for other systems to apply when Umbrella is ON.
        """
        if not self.is_deployed:
            return {}
        
        return self.config['umbrella']['effects']

    def get_status(self) -> Dict[str, Any]:
        """Returns the current state of the Umbrella."""
        return {
            "deployed": self.is_deployed,
            "reason": self.reason,
            "strategy": self.current_strategy,
            "uptime": str(datetime.now() - self.deployment_time) if self.deployment_time else "0",
            "prime_directive": self.config['umbrella']['prime_directive'],
            "active_parameters": self.config['umbrella']['parameters'] if self.is_deployed else {}
        }

