from typing import Dict, List, Any, Optional

class ToolCall:
    def __init__(self, name: str, args: Dict[str, Any]):
        self.name = name
        self.args = args

class LLMResponse:
    def __init__(self, text: str = "", tool_calls: List[ToolCall] = None, usage: Dict = None):
        self.text = text
        self.tool_calls = tool_calls or []
        self.usage = usage or {"input_tokens": 0, "output_tokens": 0}

class MockLLM:
    """Mock LLM Bridge for testing flows without API calls."""
    
    def __init__(self):
        self.conversation_history = []

    def generate(self, prompt: str, tools: Optional[List[Dict]] = None, **kwargs) -> LLMResponse:
        # Check for paradox triggers in prompt to simulate tool calls
        if "statement is false" in prompt.lower():
            # Simulate paradox detection
            return LLMResponse(
                text="Thinking...",
                tool_calls=[ToolCall(
                    name="sync_biocognitive_state",
                    args={
                        "tags": ["paradox", "logic"],
                        "salience_anchor": "false and true",
                        "rim_impact": 0.8,
                        "confidence_score": 0.95
                    }
                )]
            )
        
        # Default mock response
        return LLMResponse(
            text="Mock response from EVA.",
            tool_calls=[ToolCall(
                name="sync_biocognitive_state",
                args={
                    "tags": ["greeting"],
                    "salience_anchor": "hello",
                    "rim_impact": 0.2,
                    "confidence_score": 0.95
                }
            )]
        )

    def continue_with_result(self, function_result: Dict[str, Any], **kwargs) -> LLMResponse:
        # Simulate final response and memory proposal
        return LLMResponse(
            text="I understand the situation. I will maintain stability.",
            tool_calls=[ToolCall(
                name="propose_episodic_memory",
                args={
                    "user_fragment_proposal": {"turn_user": {"affective_inference": {"emotion_signal": "neutral", "intensity": 0.5, "confidence": 0.9}}},
                    "llm_fragment_proposal": {"turn_llm": {"summary": "Processed input in mock mode.", "epistemic_mode": "reflect", "confidence": 1.0}},
                    "context_proposal": {"episode_tag": "mock_test", "interaction_mode": "meta"}
                }
            )]
        )

    def reset(self):
        self.conversation_history = []
