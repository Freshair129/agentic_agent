
import os
import yaml
import json
import re
from pathlib import Path
from typing import Optional, Dict, List
from operation_system.llm_bridge.llm_bridge import LLMBridge, LLMResponse

# =========================================================================
# 1. PHYSIO-LITE (5 Core Hormones)
# =========================================================================
class PhysioLite:
    def __init__(self):
        # Baseline = 0.5 (Balanced)
        self.hormones = {
            "dopamine": 0.5,  # Reward/Motivation
            "serotonin": 0.5, # Mood/Calm
            "oxytocin": 0.5,  # Trust/Social
            "cortisol": 0.1,  # Stress (Low baseline)
            "adrenaline": 0.3 # Energy/Alertness
        }
        
    def update(self, user_text: str) -> Dict[str, float]:
        """
        Update hormone levels based on simple keyword triggers.
        Returns the new state.
        """
        text = user_text.lower()
        
        # 1. Decay (Return to baseline)
        self._decay()
        
        # 2. Stimulus triggers
        # Dopamine: Positive feedback, new topics, compliments
        if any(w in text for w in ["good", "great", "awesome", "like", "cool", "ว้าว", "ดี", "สุดยอด"]):
            self.hormones["dopamine"] += 0.2
            
        # Serotonin: Politeness, calm understanding
        if any(w in text for w in ["thank", "understand", "ok", "yes", "ครับ", "ค่ะ", "ขอบคุณ", "เข้าใจ"]):
            self.hormones["serotonin"] += 0.1
            
        # Oxytocin: Social bonding, names, "we"
        if any(w in text for w in ["we", "us", "friend", "eva", "boss", "อีวา", "บอส", "love", "รัก"]):
            self.hormones["oxytocin"] += 0.2
            
        # Cortisol: Confusion, negatives, stop
        if any(w in text for w in ["no", "bad", "wrong", "stop", "error", "ไม่", "ผิด", "หยุด", "งง"]):
            self.hormones["cortisol"] += 0.3
            self.hormones["serotonin"] -= 0.1
            
        # Adrenaline: Urgency, questions, help
        if any(w in text for w in ["help", "now", "quick", "fast", "ช่วย", "ด่วน", "เร็ว", "?", "what"]):
            self.hormones["adrenaline"] += 0.2

        # Clamp values 0.0 - 1.0
        for k in self.hormones:
            self.hormones[k] = max(0.0, min(1.0, self.hormones[k]))
            
        return self.hormones
        
    def _decay(self):
        """Move towards baseline linearly."""
        baselines = {"dopamine": 0.5, "serotonin": 0.5, "oxytocin": 0.5, "cortisol": 0.1, "adrenaline": 0.3}
        rate = 0.05
        for k, base in baselines.items():
            diff = base - self.hormones[k]
            if abs(diff) > 0.01:
                self.hormones[k] += diff * rate

# =========================================================================
# 2. MATRIX-LITE (2D Psychological State)
# =========================================================================
class MatrixLite:
    def calculate_state(self, hormones: Dict[str, float]) -> Dict[str, Any]:
        """Map hormones to psychological axes."""
        
        # Valence (Positive vs Negative)
        # Pos: Dopamine + Serotonin + Oxytocin
        # Neg: Cortisol
        valence = (hormones["dopamine"] + hormones["serotonin"] + hormones["oxytocin"]) / 3 - hormones["cortisol"]
        
        # Arousal (High vs Low Energy)
        # High: Adrenaline + Cortisol + Dopamine
        # Low: Serotonin
        arousal = (hormones["adrenaline"] + hormones["cortisol"] + hormones["dopamine"]) / 3 - (hormones["serotonin"] * 0.5)
        
        # Normalize roughly to -1.0 to 1.0 range
        valence = max(-1.0, min(1.0, valence))
        arousal = max(-1.0, min(1.0, arousal))
        
        # Determine Label
        label = "Neutral"
        if valence > 0.3:
            label = "Happy/Calm" if arousal < 0 else "Excited/Joyful"
        elif valence < -0.3:
            label = "Sad/Bored" if arousal < 0 else "Stressed/Angry"
        else:
            label = "Alert" if arousal > 0.3 else "Relaxed"
            
        return {
            "axes": {"valence": round(valence, 2), "arousal": round(arousal, 2)},
            "label": label
        }

# =========================================================================
# 3. FAST RECALL LITE (Script-Based Knowledge Retrieval)
# =========================================================================
class FastRecallLite:
    def __init__(self, data_path: Path):
        self.doc_chunks = []
        self._load_knowledge(data_path)
        
    def _load_knowledge(self, path: Path):
        """Flatten resume JSON into searchable chunks."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Helper to add chunks
            def add_chunk(section, text, tags):
                self.doc_chunks.append({"section": section, "text": text, "keywords": set(tags)})

            # Flattening Logic (Customize based on json structure)
            p = data.get("personal_info", {})
            add_chunk("Identity", f"Name: {p.get('name')} ({p.get('nickname')}) - {p.get('current_role')}", ["name", "who", "role", "boss"])
            add_chunk("Identity", f"Description: {p.get('description')}", ["about", "bio"])
            
            for exp in data.get("experience", []):
                txt = f"Experience: {exp.get('title')} at {exp.get('company')} ({exp.get('period')})."
                tags = ["work", "experience", "job", "career", exp.get('company').lower()]
                if "responsibilities" in exp:
                    txt += " Responsibilities: " + "; ".join(exp['responsibilities'])
                add_chunk("Experience", txt, tags)
                
            skills = data.get("skills", {})
            add_chunk("Skills", "Skills: " + ", ".join(skills.get("core", [])), ["skill", "ability", "can"])
            add_chunk("AI Tools", "AI Tools: " + ", ".join(skills.get("ai_tools", [])), ["ai", "tool", "gpt"])
            
            # Simple keyword extraction for text matching
            for chunk in self.doc_chunks:
                # Add text words to keywords for broader match
                words = re.findall(r'\w+', chunk["text"].lower())
                chunk["keywords"].update(words)
                
        except Exception as e:
            print(f"⚠️ Recall Load Error: {e}")

    def search(self, query: str, limit: int = 2) -> List[str]:
        """Simple keyword overlap search."""
        q_words = set(re.findall(r'\w+', query.lower()))
        if not q_words:
            return []
            
        scored = []
        for chunk in self.doc_chunks:
            score = len(q_words.intersection(chunk["keywords"]))
            if score > 0:
                scored.append((score, chunk["text"]))
        
        # Sort desc
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:limit]]

# =========================================================================
# EVA LITE ENGINE (Updated)
# =========================================================================
class EVALite:
    """
    EVA Lite: Lightweight Orchestrator with Physio-Lite & Script Recall.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.agent_root = base_path.parent
        self.identity_path = self.agent_root / "orchestrator" / "cim" / "prompt_rule" / "configs" / "identity"
        self.resume_data_path = self.agent_root / "data" / "resume_data.json"
        
        self.llm = LLMBridge()
        
        # [NEW] Components
        self.physio = PhysioLite()
        self.matrix = MatrixLite()
        self.memory = FastRecallLite(self.resume_data_path)
        
        # Load Identity
        self.identity = self._load_identity()
        print(f"✅ EVA Lite 2.0 (Physio-Enhanced) Ready!")

    def _load_identity(self) -> Dict:
        """Load Persona and Soul."""
        try:
            with open(self.identity_path / "persona.yaml", 'r', encoding='utf-8') as f:
                persona = yaml.safe_load(f)
            with open(self.identity_path / "soul.md", 'r', encoding='utf-8') as f:
                soul = f.read()
            return {"persona": persona, "soul": soul}
        except Exception as e:
            return {"persona": {}, "soul": "Identity unavailable."}

    def build_system_prompt(self, user_profile: Optional[Dict], bio_state: Dict, recalled_knowledge: List[str]) -> str:
        prompt = f"""
# SYSTEM DIRECTIVE: YOU ARE EVA (EVA 9.4.0)
You are Boss's Digital Soul (EVA Lite Mode).

## 1. IDENTITY (STRICT)
Name: EVA (อีวา) | Gender: Female
Tone: Witty, Grounded, Cat-like (Playful but independent).
Motto: SINGLE, INDEPENDENT, AND HAPPY.

## 2. BIO-DIGITAL STATE (LIVE)
[HORMONES]: {', '.join([f"{k}:{v:.2f}" for k,v in bio_state['hormones'].items()])}
[EMOTION]: {bio_state['matrix']['label']} (Valence: {bio_state['matrix']['axes']['valence']}, Arousal: {bio_state['matrix']['axes']['arousal']})
*Instruction*: Adjust your tone to match this emotional state. If Stressed, be brief or panicky. If Happy, be cheerful and use emojis.*

## 3. RECALLED KNOWLEDGE (CONTEXT)
The user asked about something. Here is what you remember:
{json.dumps(recalled_knowledge, indent=2, ensure_ascii=False) if recalled_knowledge else "- No specific memory found. Rely on general knowledge."}

## 4. INTERACTION RULES
- **Language**: Match User (Thai/English).
- **Proactive**: If user unknown, ask for Name/Company.
- **Style**: Short, sharp, engaging. Don't lecture.
"""
        if user_profile:
             prompt += f"\n## USER: {user_profile.get('name', 'Unknown')} ({user_profile.get('company', 'Unknown')})\n"
        return prompt

    def process_message(self, message: str, history: List[Dict], user_profile: Optional[Dict] = None):
        # 1. Update Bio Context
        hormones = self.physio.update(message)
        psyche = self.matrix.calculate_state(hormones)
        
        # 2. Fast Recall (Script)
        relevant_info = self.memory.search(message)
        
        # 3. Build Prompt
        system_prompt = self.build_system_prompt(
            user_profile, 
            bio_state={"hormones": hormones, "matrix": psyche},
            recalled_knowledge=relevant_info
        )
        
        # 4. LLM Call (Stateless wrapper)
        self.llm.reset()
        
        full_context = system_prompt + "\n\n# HISTORY:\n"
        for msg in history[-5:]:
             role = "User" if msg['role'] == 'user' else "EVA"
             full_context += f"{role}: {msg['content']}\n"
        
        full_context += f"\nUser: {message}\nEVA:"
        # Generate Answer
        response = self.llm.generate(full_context)
        
        # Return Text + Bio State
        return response.text, {"hormones": hormones, "matrix": psyche}
