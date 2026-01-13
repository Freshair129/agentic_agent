
"""
SLM Bridge (Cognitive Gateway)
Uses Qwen3 (0.6b) for fast, local intent extraction and tagging.
"""

import requests
import json
import re
from typing import Dict, List, Any

class SLMBridge:
    def __init__(self, model_name: str = "llama3.2:1b"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        print(f"[SLMBridge] [BRAIN] Initialized with model: {self.model_name}")

    def rerank(self, query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cognitive Reranking using SLM as a Cross-Encoder.
        Evaluates the relevance of retrieved memories against the user query.
        """
        if not candidates:
            return []

        # Prepare context for the SLM
        memory_list = ""
        for i, cand in enumerate(candidates):
            content = cand.get('content', cand.get('text', 'No content'))
            memory_list += f"[{i}] {content[:200]}\n"

        prompt = (
            f"Query: \"{query}\"\n\n"
            "Analyze these memory candidates. Which ones are TRULY relevant to the query's intent?\n"
            "Discard 'dumb' or irrelevant matches. Output only a JSON list of indices in order of relevance.\n"
            f"Candidates:\n{memory_list}\n"
            "Format: {\"relevant_indices\": [1, 0, ...]}"
        )

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.0},
                    "format": "json"
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = json.loads(response.json().get("response", "{}"))
            indices = data.get("relevant_indices", [])

            # Rebuild candidate list based on SLM's decision
            reranked = []
            for idx in indices:
                if 0 <= idx < len(candidates):
                    reranked.append(candidates[idx])
            
            # Add remaining candidates at a lower weight if desired, 
            # or just return the SLM-approved ones. 
            # For now, let's just return what the SLM says is relevant.
            return reranked

        except Exception as e:
            print(f"[SLMBridge] [RERANK_FAILED] Error: {e}")
            return candidates # Fallback to original order if rerank fails

    def extract_intent(self, text: str) -> Dict[str, Any]:
        """
        Analyze text to extract intent, tags, and initial gut-instinct stimulus vector.
        """
        prompt = (
            f"Analyze this Thai text: \"{text}\"\n"
            "Identify:\n"
            "1. Intent (Short summary)\n"
            "2. Salience Anchor (The exact short phrase that triggered the emotion)\n"
            "3. Emotional Signal (The initial gut feeling: jealousy, sarcasm, insecurity, possessiveness, or affection)\n"
            "4. Gut Vector (4 numbers between 0.0 and 1.0 indicating your instinct):\n"
            "   - Valence (Positive/Negative)\n"
            "   - Arousal (Energy/Calm)\n"
            "   - Stress (Threat level)\n"
            "   - Warmth (Connection/Social safety)\n\n"
            "Output JSON only: {\"intent\": \"...\", \"salience_anchor\": \"...\", \"emotional_signal\": \"...\", \"gut_vector\": {\"valence\": 0.5, \"arousal\": 0.5, \"stress\": 0.1, \"warmth\": 0.5}}"
        )

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1, 
                        "num_predict": 256
                    },
                    "format": "json"
                },
                timeout=30.0
            )
            response.raise_for_status()
            result_json = response.json()
            
            # Parse content
            content = result_json.get("response", "")
            data = json.loads(content)
            
            return {
                "intent": data.get("intent", "unknown"),
                "salience_anchor": data.get("salience_anchor", "None"),
                "emotional_signal": data.get("emotional_signal", "neutral"),
                "gut_vector": data.get("gut_vector", {"valence": 0.5, "arousal": 0.5, "stress": 0.1, "warmth": 0.5})
            }
            
        except json.JSONDecodeError:
            print(f"[SLMBridge] [FAILED] JSON Parse Error. Raw: {content}")
            return {"intent": "error", "tags": [], "sentiment": "neutral"}
        except Exception as e:
            print(f"[SLMBridge] [WARNING] Error: {e}")
            return {"intent": "unknown", "tags": [], "sentiment": "neutral"}

# Singleton Instance
slm = SLMBridge()
