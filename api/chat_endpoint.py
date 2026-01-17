from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.orchestrator import EVAOrchestrator

# Load Env
load_dotenv(Path(__file__).parent / ".env.api")

app = FastAPI(
    title="EVA Chat API",
    description="WebSocket & REST API for EVA 9.4.3",
    version="9.4.3"
)

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://pronpon.netlify.app",
    "https://pornpon.netlify.app",
    "https://resume-ecru-five-15.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrchestratorManager:
    """Manages multiple EVA Orchestrator instances."""
    def __init__(self):
        self.orchestrators: Dict[str, EVAOrchestrator] = {}

    def get_orchestrator(self, session_id: str) -> EVAOrchestrator:
        if session_id not in self.orchestrators:
            print(f"[API] Initializing new Orchestrator for session: {session_id}")
            # Initialize EVA
            self.orchestrators[session_id] = EVAOrchestrator(
                enable_physio=os.getenv("EVA_ENABLE_PHYSIO", "true").lower() == "true",
                llm_backend=os.getenv("EVA_LLM_BACKEND", "gemini")
            )
        return self.orchestrators[session_id]

# Singleton manager
manager = OrchestratorManager()

# --- Data Models ---

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    emotional_state: Optional[Dict[str, Any]] = None

# --- REST Endpoints ---

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Legacy REST endpoint for non-streaming interactions"""
    try:
        conv_id = request.conversation_id or f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        orch = manager.get_orchestrator(conv_id)
        
        # Process
        result = orch.process_user_input(request.message)
        
        bot_response = result.get("final_response", "")
        emotional_data = {
            "label": result.get("emotion_label", "neutral"),
            "axes": result.get("psychological_state", {})
        }
        
        return ChatResponse(
            response=bot_response,
            conversation_id=conv_id,
            emotional_state=emotional_data
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "agent": "EVA 9.4.3",
        "active_sessions": len(manager.orchestrators)
    }

# --- WebSocket Endpoint ---

@app.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    orch = manager.get_orchestrator(client_id)
    
    try:
        while True:
            # 1. Receive Message
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_message = payload.get("message", "")
            
            # 2. Acknowledge Receipt (Thinking State)
            await websocket.send_json({
                "type": "status",
                "status": "thinking",
                "message": "EVA is processing..."
            })
            
            # 3. Process (Synchronous for now, essentially blocking)
            # In a future async-native version, this could stream intermediate thoughts
            result = orch.process_user_input(user_message)
            
            # 4. Extract Data
            bot_response = result.get("final_response", "")
            matrix_state = result.get("psychological_state", {})
            rms_coloring = result.get("bio_state", {}).get("rms_coloring", {})
            
            # 5. Send Full State Update
            await websocket.send_json({
                "type": "response",
                "text": bot_response,
                "state": {
                    "matrix": matrix_state,
                    "rms": rms_coloring,
                    "emotion_label": result.get("emotion_label", "neutral")
                }
            })
            
    except WebSocketDisconnect:
        print(f"Client #{client_id} disconnected")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
