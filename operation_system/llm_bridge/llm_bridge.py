import os
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from tools.logger import safe_print
print = safe_print
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env if exists
load_dotenv()

class ToolCall:
    """Standardized tool call object"""
    def __init__(self, name: str, args: Dict[str, Any]):
        self.name = name
        self.args = args

class LLMResponse:
    """Standardized LLM response object"""
    def __init__(self, text: str = "", tool_calls: List[ToolCall] = None, usage: Dict = None):
        self.text = text
        self.tool_calls = tool_calls or []
        self.usage = usage or {"input_tokens": 0, "output_tokens": 0}

class LLMBridge:
    """
    Real Gemini API Bridge for EVA 9.1.0
    Supports Dual-Phase One-Inference with Function Calling.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash-exp", api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "AIzaSyAdIuP9WVnPhv0xDIUh37NAr8-54xYYyqY")
        genai.configure(api_key=self.api_key)
        
        self.model_name = model_name
        self.conversation_history = []
        self.chat_session = None
        
        # Tools will be bound during generate call
        self.tools = []

    def _initialize_chat(self, tools: Optional[List[Dict]] = None):
        """Initialize or re-initialize chat session with tools, preserving history."""
        print(f"[LLM] Initializing chat with {len(tools) if tools else 0} tools...")
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=tools
        )
        print("[LLM] Model created, starting chat...")
        # Preserve history if session exists
        history = self.chat_session.history if self.chat_session else []
        self.chat_session = self.model.start_chat(history=history or [])
        print("[LLM] Chat session ready")

    def generate(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> LLMResponse:
        """
        Generate Gemini response with optional function calling.
        """
        if not self.chat_session or tools != self.tools:
            self.tools = tools
            self._initialize_chat(tools)

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        try:
            print(f"[LLM] Sending request to Gemini (timeout: 60s)...")
            response = self.chat_session.send_message(
                prompt, 
                generation_config=generation_config,
                request_options={"timeout": 60}
            )
            print(f"[LLM] ✓ Received response from Gemini")
            
            text = ""
            tool_calls = []
            
            # Debug: Inspect response structure
            print(f"[DEBUG] Response has {len(response.candidates)} candidate(s)")
            if response.candidates and response.candidates[0].content.parts:
                print(f"[DEBUG] First candidate has {len(response.candidates[0].content.parts)} part(s)")
                for i, part in enumerate(response.candidates[0].content.parts):
                    print(f"[DEBUG] Part {i}: has_text={bool(part.text)}, has_function_call={bool(part.function_call)}")
                    if part.text:
                        text += part.text
                        print(f"[DEBUG] Text snippet: {part.text[:100]}...")
                    if part.function_call:
                        print(f"[DEBUG] Function call detected: {part.function_call.name}")
                        args = {k: v for k, v in part.function_call.args.items()}
                        tool_calls.append(ToolCall(
                            name=part.function_call.name,
                            args=args
                        ))
            
            print(f"[DEBUG] Extracted {len(tool_calls)} tool call(s), text length: {len(text)}")
            
            return LLMResponse(
                text=text,
                tool_calls=tool_calls,
                usage={"input_tokens": 0, "output_tokens": 0}
            )

        except Exception as e:
            print(f"❌ [GEMINI ERROR] {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return LLMResponse(text=f"Error: {str(e)}")

    @staticmethod
    def deep_clean(obj):
        """Standardized cleaning of Gemini/Protobuf objects for JSON serialization."""
        import json
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        if isinstance(obj, dict):
            return {str(k): LLMBridge.deep_clean(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set)):
            return [LLMBridge.deep_clean(v) for v in obj]
        if hasattr(obj, 'item'):  # Numpy scalars
            return obj.item()
        
        # Fallback for complex objects: convert to string/dict if possible
        try:
            # Check if it's already JSON serializable
            json.dumps(obj)
            return obj
        except:
            # If it has a __dict__, use it but don't recurse blindly
            if hasattr(obj, '__dict__') and not isinstance(obj, type):
                 # Convert dict keys to strings and values recursively
                 return {str(k): str(v) for k, v in obj.__dict__.items()}
            return str(obj)

    def continue_with_result(self, function_result: Dict[str, Any], function_name: str = "sync_biocognitive_state") -> LLMResponse:
        """
        Continue LLM inference after function call (Phase 2).
        """
        if not self.chat_session:
            return LLMResponse(text="Error: No active chat session to continue.")

        try:
            import google.generativeai as genai
            import json
            
            clean_result = LLMBridge.deep_clean(function_result)
            
            # Use a dictionary format for better compatibility with send_message
            # The SDK handles the conversion to Protos internally
            function_response_dict = {
                "function_response": {
                    "name": function_name,
                    "response": clean_result
                }
            }
            
            # Send the wrapped part. SDK handles Role assignment.
            try:
                response = self.chat_session.send_message(function_response_dict)
                # Ensure we have a valid response
                if not response.candidates:
                     raise ValueError("Gemini returned no candidates (blocked or empty)")
            except Exception as func_err:
                err_msg = str(func_err)
                print(f"⚠️ [LLM] Function response failed ({type(func_err).__name__}: {err_msg})")
                
                # If it's a Malformed Function Call, the session is likely corrupted.
                # We need to recover by resetting the session or pushing through.
                if "MALFORMED_FUNCTION_CALL" in err_msg or "StopCandidateException" in err_msg:
                    print("🔄 [LLM] Session corruption detected. Attempting history-preserved recovery...")
                    # Fallback: Capture history, reset session, and re-inject state as text
                    history = self.chat_session.history
                    self.reset()
                    self.chat_session = self.model.start_chat(history=history)
                    
                    # Try to force a response via text injection
                    fallback_text = (
                        f"[System: การประมวลผลฟังก์ชัน '{function_name}' ล้มเหลวทางเทคนิค แต่ข้อมูลต่อไปนี้ได้รับการยืนยันแล้ว:\n"
                        f"{json.dumps(clean_result, ensure_ascii=False, indent=2)}\n"
                        f"โปรดตอบกลับผู้ใช้เป็นภาษาไทย โดยใช้ข้อมูลนี้ประกอบการตัดสินใจ]"
                    )
                    response = self.chat_session.send_message(fallback_text)
                else:
                    # Generic fallback
                    fallback_text = (
                        f"ระบบบันทึกสถานะเรียบร้อยแล้ว (Function '{function_name}' executed)\n"
                        f"ผลลัพธ์: {json.dumps(clean_result, ensure_ascii=False, default=str)}\n\n"
                        f"โปรดดำเนินการต่อโดยตอบโต้กับผู้ใช้เป็นภาษาไทย"
                    )
                    response = self.chat_session.send_message(fallback_text)

            final_text = ""
            tool_calls = []
            
            # Robust extraction
            try:
                if response.candidates and len(response.candidates) > 0:
                    for p in response.candidates[0].content.parts:
                        if hasattr(p, "text") and p.text:
                            final_text += p.text
                        if hasattr(p, "function_call") and p.function_call:
                            tool_calls.append(ToolCall(
                                name=p.function_call.name,
                                args={k: v for k, v in p.function_call.args.items()}
                            ))
                elif hasattr(response, "text"):
                    final_text = response.text
            except Exception as extract_err:
                print(f"⚠️ [LLM] Extraction warning: {extract_err}")
                if not final_text:
                    final_text = "[Error extracting response text]"
                
            return LLMResponse(text=final_text.strip() or "[Empty Response]", tool_calls=tool_calls)

        except Exception as e:
            print(f"❌ [CONTINUATION FATAL ERROR] {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return LLMResponse(text=f"Error: {str(e)}")

    def reset(self):
        """Reset session."""
        self.chat_session = None

# Tool definition for sync_biocognitive_state
SYNC_BIOCOGNITIVE_STATE_TOOL = {
    "function_declarations": [{
        "name": "sync_biocognitive_state",
        "description": "Synchronize biological and cognitive state. If you agree with SLM's Gut Instinct, you can omit 'stimulus_vector' and set high confidence.",
        "parameters": {
            "type": "object",
            "properties": {
                "stimulus_id": {
                    "type": "string",
                    "description": "The pre-defined ID from the Stimulus Catalog (e.g., 'acute_threat', 'social_status')."
                },
                "stimulus_vector": {
                    "type": "object",
                    "description": "OPTIONAL: Provide only if you wish to override or refine the SLM's gut instinct vector.",
                    "properties": {
                        "stress": {"type": "number"},
                        "warmth": {"type": "number"},
                        "arousal": {"type": "number"},
                        "valence": {"type": "number"}
                    }
                },
                "bio_impacts": {
                    "type": "object",
                    "description": "Direct chemical/hormonal impacts if not covered by stimulus_id (e.g., {'ESC_H01_ADRENALINE': 0.5})."
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "salience_anchor": {
                    "type": "string",
                    "description": "The exact phrase or keyword from the input that triggered this stimulus."
                },
                "rim_impact": {
                    "type": "number",
                    "description": "Estimated Resonance Impact (0.0-1.0) of the salience_anchor on the system's state."
                },
                "confidence_score": {
                    "type": "number",
                    "description": "0.0-1.0. High confidence (>0.9) indicates you accept the SLM's perception/vector as accurate."
                }
            },
            "required": ["tags", "salience_anchor", "rim_impact", "confidence_score"]
        }
    }]
}

# Tool definition for episodic memory proposal
# Tool definition for episodic memory proposal
PROPOSE_EPISODIC_MEMORY_TOOL = {
    "function_declarations": [{
        "name": "propose_episodic_memory",
        "description": "Propose narrative and interpretive content for episodic memory record.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_fragment_proposal": {
                    "type": "object",
                    "properties": {
                        "turn_user": {
                            "type": "object",
                            "properties": {
                                "affective_inference": {
                                    "type": "object",
                                    "properties": {
                                        "emotion_signal": {"type": "string"},
                                        "intensity": {"type": "number"},
                                        "confidence": {"type": "number"}
                                    }
                                },
                                "salience_anchor": {
                                    "type": "object",
                                    "properties": {
                                        "phrase": {"type": "string"},
                                        "Resonance_impact": {"type": "number"}
                                    }
                                }
                            }
                        }
                    }
                },
                "llm_fragment_proposal": {
                    "type": "object",
                    "properties": {
                        "turn_llm": {
                            "type": "object",
                            "properties": {
                                "summary": {"type": "string"},
                                "epistemic_mode": {
                                    "type": "string", 
                                    "enum": ["explore", "hypothesize", "assert", "caution", "reflect"]
                                },
                                "confidence": {"type": "number"}
                            }
                        },
                        "crosslinks": {
                            "type": "object",
                            "properties": {
                                "semantic_refs": {"type": "array", "items": {"type": "string"}},
                                "aqi_refs": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    }
                },
                "context_proposal": {
                    "type": "object",
                    "properties": {
                        "episode_tag": {"type": "string"},
                        "interaction_mode": {
                            "type": "string", 
                            "enum": ["small_talk", "casual", "deep_discussion", "conflict", "instruction", "meta"]
                        }
                    }
                }
            },
            "required": ["user_fragment_proposal", "llm_fragment_proposal", "context_proposal"]
        }
    }]
}
