# User Grounding & Conflict Detection - Example Usage

## Example 1: Allergy Conflict

### Initial State (User Block)

```json
{
  "user_id": "U_001",
  "user_block": {
    "grounding_facts": [
      {
        "fact_id": "UF_001",
        "category": "allergy",
        "statement": "แพ้อาหารทะเล",
        "confidence": 0.95,
        "evidence_episodes": ["EVA_EP025"],
        "last_verified": "2026-01-10",
        "contradictions": []
      }
    ]
  }
}
```

### Session Discovery

```python
# User says: "อยากกินกุ้งเผาอยุธยา"
buffer = SemanticMemoryBuffer("U_001", "SES_001")
buffer.add_discovery(
    statement="อยากกินกุ้ง",
    category="allergy",
    confidence=0.8,
    turn_id="TURN_001",
    evidence_text="อยากกินกุ้งเผาอยุธยา"
)
```

### Conflict Detection

```python
detector = ConflictDetector()
result = detector.detect_contradiction(
    user_block=user_profile["user_block"],
    semantic_buffer=buffer.to_dict()
)

# Result:
# {
#   "has_conflict": True,
#   "severity": 0.95,
#   "conflicts": [{
#     "discovery": {"statement": "อยากกินกุ้ง"},
#     "grounding_fact": {"statement": "แพ้อาหารทะเล"},
#     "severity": 0.95
#   }]
# }
```

### Natural Question Generation

```python
conflict = result["conflicts"][0]
question = detector.generate_natural_question(conflict)

# Output: "หืม คุณเคยบอกว่า\"แพ้อาหารทะเล\" ไม่ใช่หรอครับ?"
```

### Hypothesis Generation

```python
hypotheses = detector.generate_hypothesis(conflict)

# Output:
# [
#   {"type": "variable_refinement", "confidence": 0.7,
#    "description": "กุ้งแม่น้ำ ≠ กุ้งทะเล"},
#   {"type": "temporal_change", "confidence": 0.5,
#    "description": "แพ้ตอนเด็ก → โตแล้วไม่แพ้"},
#   ...
# ]
```

### Resolution (After User Confirms)

```python
# User: "กุ้งแม่น้ำกินได้ แพ้แค่ฟอร์มาลินจากอาหารทะเล"

# Update grounding fact
user_profile["user_block"]["grounding_facts"][0] = {
    "fact_id": "UF_001",
    "category": "allergy",
    "statement": "แพ้ฟอร์มาลินในอาหารทะเล (ไม่ใช่โปรตีนกุ้ง)",
    "confidence": 0.98,
    "evidence_episodes": ["EVA_EP025", "EVA_EP052"],
    "last_verified": "2026-01-12",
    "contradictions": [{
        "episode_id": "EVA_EP052",
        "conflicting_statement": "อยากกินกุ้ง",
        "resolution": "Refined: กุ้งแม่น้ำ OK, ฟอร์มาลินในทะเล NG",
        "timestamp": "2026-01-12T20:25:00"
    }]
}

# Mark as verified
buffer.mark_as_verified("อยากกินกุ้ง")
```

---

## Example 2: Integration with MSP

```python
class MSP:
    def __init__(self):
        self.user_registry = UserRegistryManager()
        self.conflict_detector = ConflictDetector()
        self.semantic_buffers = {}  # {user_id: SemanticMemoryBuffer}
    
    def get_or_create_buffer(self, user_id, session_id):
        key = f"{user_id}_{session_id}"
        if key not in self.semantic_buffers:
            self.semantic_buffers[key] = SemanticMemoryBuffer(user_id, session_id)
        return self.semantic_buffers[key]
    
    def check_for_conflicts(self, user_id, session_id):
        """Called in Orchestrator's The Gap"""
        user_profile = self.load_user_profile(user_id)
        buffer = self.get_or_create_buffer(user_id, session_id)
        
        result = self.conflict_detector.detect_contradiction(
            user_block=user_profile.get("user_block", {}),
            semantic_buffer=buffer.to_dict()
        )
        
        return result
```

---

## File Structure

```
eva/
├── memory_n_soul_passport/
│   ├── user_registry_manager.py          ✅ Created
│   ├── semantic_memory_buffer.py         ✅ Created
│   └── schema/
│       ├── User_Profile_Schema.json      ✅ Extended
│       └── Episodic_Memory_Schema_v2.json ✅ Extended
└── expansion/
    └── user_grounding/
        └── conflict_detector.py          ✅ Created
```
