"""
MRF Engine (Metacognitive Re-contextualization Framework)
Version: 9.4.3

Purpose:
Transform unsolvable problems by shifting context/meaning rather than
solving them directly. Implements the "Umbrella Principle" - coexist with
uncontrollable events rather than trying to eliminate them.

7-Layer Processing:
1. Literal    - Surface meaning
2. Emotional  - Hidden emotion
3. Symbolic   - Metaphorical transformation (uses APM)
4. Relational - Relationship analysis
5. Narrative  - Story arc positioning
6. Meta       - Self-awareness of interpretation
7. Transcendental - Wisdom extraction (Umbrella deployment)
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class MRFOutput:
    """Output structure for MRF processing"""
    interpretation_map: Dict[str, Any]  # 7-layer interpretation
    paradox_detected: bool
    layer_depth: int  # 1-7
    umbrella_deployed: bool
    symbolic_archetype: Optional[str] = None


class MRFEngine:
    """
    Central Module: Metacognitive Re-contextualization Framework
    
    Transforms problems by shifting meaning/context rather than
    solving directly. Uses 7-layer interpretation pipeline.
    """
    
    def __init__(self, config_path: Optional[str] = None, 
                 apm_engine: Optional[Any] = None,
                 umbrella_engine: Optional[Any] = None):
        # Load config
        if config_path is None:
            config_path = Path(__file__).parent / "configs" / "mrf_config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Dependencies
        self.apm = apm_engine
        self.umbrella = umbrella_engine
        
        # State
        self.current_layer = 0
        self.paradox_active = False
    
    def process(self, text: str, context: Optional[Dict] = None) -> MRFOutput:
        """
        Main MRF processing pipeline.
        
        Args:
            text: Input text to recontextualize
            context: Optional context (user profile, current state, etc.)
        
        Returns:
            MRFOutput with interpretation_map and metadata
        """
        interpretation = {}
        paradox_detected = False
        umbrella_deployed = False
        layer_reached = 0
        
        # Layer 1: Literal
        if self.config['layers']['literal']['enabled']:
            interpretation['literal'] = self._process_literal(text)
            layer_reached = 1
        
        # Layer 2: Emotional
        if self.config['layers']['emotional']['enabled']:
            interpretation['emotional'] = self._process_emotional(text, context)
            layer_reached = 2
        
        # Layer 3: Symbolic (APM)
        if self.config['layers']['symbolic']['enabled']:
            symbolic_result = self._process_symbolic(text, context)
            interpretation['symbolic'] = symbolic_result
            layer_reached = 3
        
        # Layer 4: Relational
        if self.config['layers']['relational']['enabled']:
            interpretation['relational'] = self._process_relational(text, context)
            layer_reached = 4
        
        # Layer 5: Narrative
        if self.config['layers']['narrative']['enabled']:
            interpretation['narrative'] = self._process_narrative(text, context)
            layer_reached = 5
        
        # Layer 6: Meta (Paradox Detection)
        if self.config['layers']['meta']['enabled']:
            meta_result = self._process_meta(text, interpretation)
            interpretation['meta'] = meta_result
            paradox_detected = meta_result.get('paradox_detected', False)
            layer_reached = 6
        
        # Layer 7: Transcendental (Umbrella)
        if self.config['layers']['transcendental']['enabled'] and paradox_detected:
            transcendental_result = self._process_transcendental(
                text, interpretation, paradox_detected
            )
            interpretation['transcendental'] = transcendental_result
            umbrella_deployed = transcendental_result.get('umbrella_deployed', False)
            layer_reached = 7
        
        return MRFOutput(
            interpretation_map=interpretation,
            paradox_detected=paradox_detected,
            layer_depth=layer_reached,
            umbrella_deployed=umbrella_deployed,
            symbolic_archetype=interpretation.get('symbolic', {}).get('archetype')
        )
    
    def _process_literal(self, text: str) -> Dict[str, Any]:
        """Layer 1: Extract literal meaning (who, what, where)"""
        # TODO: Implement literal parsing
        return {
            "surface_meaning": text,
            "entities": []
        }
    
    def _process_emotional(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Layer 2: Extract emotional undertone"""
        # TODO: Implement emotion detection
        return {
            "primary_emotion": "neutral",
            "intensity": 0.5
        }
    
    def _process_symbolic(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Layer 3: Transform to symbolic/archetypal representation (uses APM)"""
        if self.apm:
            apm_context = {"user_input": text}
            if context:
                apm_context.update(context)
            
            apm_result = self.apm.project_archetype(apm_context)
            return {
                "archetype": apm_result.get('active_lenses', [None])[0] if apm_result.get('active_lenses') else None,
                "symbolic_meaning": apm_result.get('archetype_projection', ""),
                "apm_used": True
            }
            
        return {
            "archetype": None,
            "symbolic_meaning": "",
            "apm_used": False
        }
    
    def _process_relational(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Layer 4: Analyze relationship dynamics"""
        # TODO: Implement relational analysis
        return {
            "relationship_type": "unknown",
            "power_dynamic": "balanced"
        }
    
    def _process_narrative(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Layer 5: Position in life story arc"""
        # TODO: Implement narrative positioning
        return {
            "story_position": "middle",
            "arc_type": "unknown"
        }
    
    def _process_meta(self, text: str, interpretation: Dict) -> Dict[str, Any]:
        """Layer 6: Meta-cognitive analysis (why interpret this way?)"""
        # TODO: Implement paradox detection
        paradox_score = 0.0
        
        return {
            "meta_awareness": "low",
            "paradox_detected": paradox_score > self.config['paradox_detection']['threshold'],
            "paradox_score": paradox_score
        }
    
    def _process_transcendental(self, text: str, interpretation: Dict, 
                                 paradox: bool) -> Dict[str, Any]:
        """Layer 7: Transcendence to wisdom (Umbrella deployment)"""
        umbrella_deployed = False
        
        if paradox and self.config['umbrella_trigger']['enabled']:
            if self.umbrella:
                # Deploy Umbrella via engine
                self.umbrella.deploy(
                    reason=f"MRF Paradox detected in layer 6: {interpretation.get('meta', {}).get('paradox_score', 0)}",
                    strategy="Graceful Degradation"
                )
                umbrella_deployed = True
            else:
                # Virtual deployment if engine not provided
                umbrella_deployed = True
        
        return {
            "umbrella_deployed": umbrella_deployed,
            "transcendental_insight": "Paradox accepted. Transitioning to meta-stability.",
            "wisdom_extracted": True if umbrella_deployed else False
        }

