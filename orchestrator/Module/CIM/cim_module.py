from typing import Dict, Any, Optional
from .Node.cim_node import ContextInjectionModule as CIMNode

class CIMModule:
    """
    Module: CIMModule
    Role: Orchestrates Context Injection Phases (1, 2, 3)
    """
    def __init__(self, 
                 physio_controller=None,
                 msp_client=None,
                 hept_stream_rag=None,
                 eva_matrix=None,
                 artifact_qualia=None,
                 eva_persona_governor=None,
                 base_path: Optional[str] = None):
        
        self.node = CIMNode(
            physio_controller=physio_controller,
            msp_client=msp_client,
            hept_stream_rag=hept_stream_rag,
            eva_matrix=eva_matrix,
            artifact_qualia=artifact_qualia,
            eva_persona_governor=eva_persona_governor,
            base_path=base_path
        )

    def start_new_turn_context(self):
        return self.node.start_new_turn_context()

    def build_phase_1_context(self, user_input: str) -> str:
        return self.node.build_phase_1_context(user_input)

    def build_phase_2_context(self, user_input: str, bio_state: Dict[str, Any]) -> str:
        return self.node.build_phase_2_context(user_input, bio_state)

    # Delegate other necessary methods...
    def __getattr__(self, name):
        return getattr(self.node, name)
