"""
Conflict Detector
Detects contradictions between User Block (ground truth) and Semantic Memory Buffer (session discoveries)
"""

from typing import Dict, List, Optional
import difflib


class ConflictDetector:
    """
    Detects and analyzes conflicts between persistent user facts and session discoveries.
    Generates hypotheses and natural language questions for resolution.
    """
    
    def __init__(self, persona_style: str = "thai_casual"):
        """
        Initialize conflict detector
        
        Args:
            persona_style: Persona style for question generation
        """
        self.persona_style = persona_style
        self.conflict_threshold = 0.6  # Similarity below this = conflict
    
    def detect_contradiction(
        self,
        user_block: Dict,
        semantic_buffer: Dict
    ) -> Dict:
        """
        Detect contradictions between grounding facts and session discoveries
        
        Args:
            user_block: Persistent user facts (from User Profile)
            semantic_buffer: Session discoveries (from SemanticMemoryBuffer)
        
        Returns:
            {
                "has_conflict": bool,
                "conflicts": [...],
                "severity": float (0.0-1.0)
            }
        """
        grounding_facts = user_block.get("grounding_facts", [])
        discoveries = semantic_buffer.get("discoveries", [])
        
        conflicts = []
        
        for discovery in discoveries:
            if discovery["status"] != "unverified":
                continue  # Skip already processed
            
            for fact in grounding_facts:
                # Check same category
                if discovery["category"] != fact["category"]:
                    continue
                
                # Check for semantic conflict
                similarity = self._calculate_similarity(
                    discovery["statement"],
                    fact["statement"]
                )
                
                # If statements are similar but confidence differs significantly
                is_opposite = self._is_opposite_meaning(
                    discovery["statement"],
                    fact["statement"]
                )
                
                if is_opposite or (similarity > 0.3 and similarity < self.conflict_threshold):
                    conflict = {
                        "discovery": discovery,
                        "grounding_fact": fact,
                        "similarity": similarity,
                        "is_opposite": is_opposite,
                        "severity": self._calculate_severity(fact, discovery)
                    }
                    conflicts.append(conflict)
        
        # Calculate overall severity
        max_severity = max([c["severity"] for c in conflicts], default=0.0)
        
        return {
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts,
            "severity": max_severity,
            "conflict_count": len(conflicts)
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (0.0-1.0)"""
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _is_opposite_meaning(self, text1: str, text2: str) -> bool:
        """
        Detect opposite meanings (simple heuristic)
        
        Examples:
        - "แพ้อาหารทะเล" vs "กินอาหารทะเลได้"
        - "ไม่ชอบกาแฟ" vs "ชอบกาแฟ"
        """
        # Negation patterns
        negations_thai = ["ไม่", "ไม่ได้", "ไม่มี", "ไม่เคย"]
        negations_en = ["not", "don't", "doesn't", "can't", "won't"]
        
        has_neg_1 = any(neg in text1 for neg in negations_thai + negations_en)
        has_neg_2 = any(neg in text2 for neg in negations_thai + negations_en)
        
        # XOR: one has negation, other doesn't
        return has_neg_1 != has_neg_2
    
    def _calculate_severity(self, fact: Dict, discovery: Dict) -> float:
        """
        Calculate conflict severity (0.0-1.0)
        
        Factors:
        - Fact confidence (higher = more severe)
        - Category (health > preference > memory)
        - Evidence count
        """
        base_severity = fact.get("confidence", 0.5)
        
        # Category multiplier
        category_weights = {
            "health": 1.0,      # Highest priority (safety)
            "allergy": 1.0,     # Same as health
            "preference": 0.7,  # Medium
            "memory": 0.5,      # Lower
            "skill": 0.6,
            "belief": 0.4
        }
        
        category = fact.get("category", "unknown")
        weight = category_weights.get(category, 0.5)
        
        # Evidence strength
        evidence_count = len(fact.get("evidence_episodes", []))
        evidence_factor = min(1.0, evidence_count / 3.0)  # Cap at 3 episodes
        
        severity = base_severity * weight * (0.7 + 0.3 * evidence_factor)
        return min(1.0, severity)
    
    def calculate_confidence_penalty(self, severity: float) -> float:
        """
        Calculate confidence penalty for LLM
        
        Args:
            severity: Conflict severity (0.0-1.0)
        
        Returns:
            Penalty factor (0.0-0.5)
        """
        # Linear penalty: 0.1 to 0.5 based on severity
        return 0.1 + (severity * 0.4)
    
    def generate_natural_question(
        self,
        conflict: Dict,
        persona_style: str = None
    ) -> str:
        """
        Generate natural language clarification question
        
        Args:
            conflict: Conflict dict from detect_contradiction
            persona_style: Override default style
        
        Returns:
            Natural question string
        """
        style = persona_style or self.persona_style
        fact = conflict["grounding_fact"]
        discovery = conflict["discovery"]
        
        # Thai casual style (EVA's default)
        if style == "thai_casual":
            prefixes = [
                "หืม",
                "เดี๋ยวนะ",
                "ถ้าจำไม่ผิด",
                "ผมจำได้ว่า"
            ]
            
            # Build question
            import random
            prefix = random.choice(prefixes)
            
            question = (
                f"{prefix} คุณเคยบอกว่า\"{fact['statement']}\" "
                f"ไม่ใช่หรอครับ?"
            )
            
            return question
        
        # English formal
        elif style == "english_formal":
            return (
                f"I recall you mentioned that \"{fact['statement']}\". "
                f"Could you clarify this?"
            )
        
        # Default
        return f"Conflict detected: {fact['statement']} vs {discovery['statement']}"
    
    def generate_hypothesis(self, conflict: Dict) -> List[Dict]:
        """
        Generate hypotheses to explain the conflict
        
        Args:
            conflict: Conflict dict
        
        Returns:
            List of hypothesis dicts
        """
        fact = conflict["grounding_fact"]
        discovery = conflict["discovery"]
        
        hypotheses = []
        
        # Hypothesis 1: Variable refinement (most common)
        hypotheses.append({
            "type": "variable_refinement",
            "description": "ข้อมูลถูกต้องทั้งคู่ แต่มีตัวแปรที่ยังไม่ระบุ",
            "example": "แพ้อาหารทะเล → แพ้ฟอร์มาลิน (ไม่ใช่โปรตีนกุ้ง)",
            "confidence": 0.7
        })
        
        # Hypothesis 2: Temporal change
        hypotheses.append({
            "type": "temporal_change",
            "description": "ความจริงเปลี่ยนไปตามเวลา",
            "example": "แพ้ตอนเด็ก → โตแล้วไม่แพ้",
            "confidence": 0.5
        })
        
        # Hypothesis 3: Misunderstanding
        hypotheses.append({
            "type": "misunderstanding",
            "description": "เข้าใจผิดในครั้งแรก",
            "example": "บอกผิด หรือ EVA จำผิด",
            "confidence": 0.3
        })
        
        return hypotheses
