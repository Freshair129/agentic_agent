import requests
import json
import re
from typing import List, Dict, Any, Optional

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

class OllamaBridge:
    """
    Interface for Ollama API providing local LLM and Embedding services.
    """
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.2:3b", context_window: int = 32768):
        self.host = host
        self.embed_model = "nomic-embed-text"
        self.gen_model = model
        self.context_window = context_window
        self.tools = []

    def generate(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system: Optional[str] = None
    ) -> LLMResponse:
        self.tools = tools or []
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.gen_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature, 
                "num_predict": max_tokens,
                "num_ctx": self.context_window
            }
        }
        # Temporarily disabled - testing if this blocks model output
        # if self.tools:
        #     payload["format"] = "json"
        if system: payload["system"] = system

        try:
            # safe_print(f"[OllamaBridge] Prompting for {len(self.tools)} tools...") 
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            text = response.json()["response"]
            print(f"[DEBUG RAW LLM OUTPUT]:\n{text}\n[END DEBUG]")
            
            # --- Tool Call Parsing (heuristic) ---
            tool_calls = []
            if self.tools:
                # 1. Try finding specific Tool JSON format
                # Look for { ... } block
                json_match = re.search(r'(\{.*\})', text, re.DOTALL)
                
                if json_match:
                    try:
                        data = json.loads(json_match.group(1))
                        
                        # Determine Tool Name (Simple assumption: single tool context)
                        # In CIM we usually provide one tool at a time (sync or propose)
                        target_tool_name = self.tools[0]["function"]["name"] if self.tools else "unknown"
                        
                        # Handling different LLM output styles:
                        # Type A: {"tool": "name", "args": {...}}
                        # Type B: {"function": {"name": "...", "arguments": ...}} (OpenAI)
                        # Type C: Just the arguments { "arg1": ... } (Qwen common)
                        
                        final_args = {}
                        final_name = target_tool_name
                        
                        if "function" in data and "name" in data["function"]:
                            final_name = data["function"]["name"]
                            args_raw = data["function"]["arguments"]
                            final_args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                        elif "tool" in data and "args" in data:
                            final_name = data["tool"]
                            final_args = data["args"]
                        else:
                            # Verify if keys match expected args, or just assume it's the args
                            final_args = data
                        
                        tool_calls.append(ToolCall(final_name, final_args))
                        # print(f"[OllamaBridge] Parsed Tool: {final_name}")
                        
                    except Exception as e:
                        print(f"[OllamaBridge] JSON Parse Warn: {e}")

            return LLMResponse(text=text, tool_calls=tool_calls)
        except Exception as e:
            print(f"Error calling Ollama Generate: {e}")
            return LLMResponse(text=f"Error: {str(e)}")

    def continue_with_result(self, function_result: str, function_name: str = "sync_biocognitive_state") -> LLMResponse:
        return self.generate(f"Tool {function_name} result: {function_result}\n\nPlease continue.")

    def reset(self):
        self.tools = []
