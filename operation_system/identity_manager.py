"""
IdentityManager
Centralized Factory for all IDs (Episodes, Sessions, Cores, Spheres, Contexts)
"""

import os
from datetime import datetime
import time

class IdentityManager:
    # --- System & Bus Registry (V9.3.3 Resonance Edition) ---
    # These constants prevent magic string errors across the codebase.
    
    # Core System IDs
    SYSTEM_MSP = "MSP"
    SYSTEM_PHYSIO = "PhysioCore"
    SYSTEM_MATRIX = "EVA_Matrix"
    SYSTEM_QUALIA = "Artifact_Qualia"
    SYSTEM_RMS = "RMS"
    SYSTEM_CIM = "CIM"
    SYSTEM_PRN = "PRN"
    SYSTEM_RAG = "AgenticRAG"
    SYSTEM_ORCH = "Orchestrator"
    
    # Cognitive & Expansion Systems (V9.3.0G+)
    SYSTEM_GKS = "GKS"
    SYSTEM_NEXUS = "NexusMind"
    SYSTEM_APM = "APM"
    SYSTEM_MLL = "MLL"
    SYSTEM_TEMPORAL = "TemporalEngine"
    
    # Sub-Systems (Temporal)
    SUBSYSTEM_PULSE = "PULSE"
    SUBSYSTEM_NODE_SOT = "NodeSOT"

    # Resonance Bus Channels
    BUS_PHYSICAL = "bus:physical"
    BUS_PSYCHOLOGICAL = "bus:psychological"
    BUS_PHENOMENOLOGICAL = "bus:phenomenological"
    BUS_KNOWLEDGE = "bus:knowledge"
    BUS_COGNITIVE = "bus:cognitive"      # For GKS/NexusMind
    BUS_TEMPORAL = "bus:temporal"        # For Temporal Engine

    # Persona Registry
    PERSONA_MAP = {
        "EVA": "PE_01",
        "LYRA": "PE_02"
    }

    @staticmethod
    def get_persona_id(persona_code: str) -> str:
        return IdentityManager.PERSONA_MAP.get(persona_code, "PE_UNKNOWN")

    @staticmethod
    def generate_episode_id(persona_code: str, episode_num: int, pattern: str = "{PERSONA}_EP{number:02d}") -> str:
        """
        Format: {PERSONA}_EP{number} (e.g., EVA_EP01)
        Pattern driven by MSP_configs.yaml
        """
        try:
            return pattern.format(PERSONA=persona_code, number=episode_num)
        except Exception:
            # Fallback if pattern is invalid
            return f"{persona_code}_EP{episode_num:02d}"

    @staticmethod
    def generate_turn_id(session_id: str, turn_index: int) -> str:
        """
        Format: TURN_{session_id}_{turn_index:03d}
        Source of Truth for sequential interactions.
        """
        return f"TURN_{session_id}_{turn_index:03d}"

    @staticmethod
    def generate_session_id(dev_id: str, sphere: int, core: int, session: int) -> str:
        """Format: {dev_id}_SP{sphere+1}C{core+1}_SES{session}"""
        return f"{dev_id}_SP{sphere + 1}C{core + 1}_SES{session}"

    @staticmethod
    def generate_context_id(session_seq: int, episodic_id: str) -> str:
        """Format: ctx_{session_seq}_{episodic_id}.md"""
        return f"ctx_{session_seq}_{episodic_id}.md"

    @staticmethod
    def generate_core_id(dev_id: str, sphere: int, core: int) -> str:
        """Format: {dev_id}_SP{sphere}C{core} (Display as 1-indexed)"""
        return f"{dev_id}_SP{sphere + 1}C{core + 1}"

    @staticmethod
    def generate_session_memory_id(dev_id: str, sphere: int, core: int, session: int) -> str:
        """Format: {dev_id}_SP{sphere}C{core}_SES{session} (session is position in core)"""
        # Note: SP and C are usually displayed 1-indexed for humans
        return f"{dev_id}_SP{sphere + 1}C{core + 1}_SES{session}"

    @staticmethod
    def generate_sphere_id(dev_id: str, sphere: int) -> str:
        """Format: {dev_id}_SP{sphere} (Display as 1-indexed)"""
        return f"{dev_id}_SP{sphere + 1}"

    @staticmethod
    def generate_full_episodic_filename(session_id: str, episode_id: str) -> str:
        """
        Logic for the full episodic identifier/filename.
        Format: {session_id}_{episode_id}
        Example: THA-06_SP3C1_SES1_EVA_EP01
        """
        return f"{session_id}_{episode_id}"

