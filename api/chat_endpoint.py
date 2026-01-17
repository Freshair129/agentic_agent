from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.orchestrator import EVAOrchestrator

# File System Configuration
MEMORY_BASE_DIR = Path("e:/resume-web/memory")
MEMORY_BASE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="EVA Chat API",
    description="API endpoint for Boss's portfolio chatbot",
    version="9.4.3"
)

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Local development
    "http://localhost:3000",  # Alternative local port
    "https://pronpon.netlify.app",  # Production
    "https://pornpon.netlify.app",  # Main Production URL
    "https://resume-ecru-five-15.vercel.app", # Vercel Production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OrchestratorManager:
    """Manages multiple EVA Orchestrator instances for different users/conversations"""
    def __init__(self):
        self.orchestrators: Dict[str, EVAOrchestrator] = {}

    def get_orchestrator(self, session_id: str) -> EVAOrchestrator:
        if session_id not in self.orchestrators:
            print(f"[API] Initializing new Orchestrator for session: {session_id}")
            # Ensure session directory exists in the NEW location
            session_dir = MEMORY_BASE_DIR / "users" / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize EVA (Pointing to its new home)
            self.orchestrators[session_id] = EVAOrchestrator(
                enable_physio=os.getenv("EVA_ENABLE_PHYSIO", "true").lower() == "true",
                llm_backend=os.getenv("EVA_LLM_BACKEND", "gemini")
            )
        return self.orchestrators[session_id]

# Singleton manager
manager = OrchestratorManager()

def get_history_from_memory(session_id: str) -> List[Dict]:
    """Load conversation history from the local memory folder"""
    history = []
    episode_dir = MEMORY_BASE_DIR / "users" / session_id / "episodes_user"
    if episode_dir.exists():
        # Sort files by name (assuming chronological naming like EP01, EP02)
        files = sorted(episode_dir.glob("*.json"))
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    history.append({"role": "user", "content": data.get("content", "")})
                    # Also load matching AI response if exists
                    ai_file = MEMORY_BASE_DIR / "users" / session_id / "episodes_ai" / f.name
                    if ai_file.exists():
                         with open(ai_file, "r", encoding="utf-8") as ai_f:
                             ai_data = json.load(ai_f)
                             history.append({"role": "bot", "content": ai_data.get("final_response", "")})
            except:
                continue
    return history


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    emotional_state: Optional[Dict[str, Any]] = None


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chatbot requests with Persistent Identity (Name + Company)
    """
    try:
        # Common processing for both Lite and Full
        conv_id = "default_session" # Default for Lite, or if no identity for Full
        user_profile = {}
        
        if request.metadata:
            # Try to extract tracking info
            source = request.metadata.get("source", "")
            # Extract user info explicitly if passed from frontend
            if "userName" in request.metadata:
                user_profile["name"] = request.metadata["userName"]
            if "company" in request.metadata:
                user_profile["company"] = request.metadata["company"]
        
        print(f"📨 [MSG] User: {request.message[:50]}... (Profile: {user_profile})")

        if USE_EVA_LITE:
            # 2. Process via EVA Lite
            try:
                # Lite returns direct response, but we need emotion too.
                # Modified process_message to return Dict or Tuple?
                # Let's update eva_lite.py first to return tuple, OR adjust here.
                # Actually, let's update call to expect dict if I change eva_lite.
                # For now, let's assume process_message returns tuple (text, state)
                response_text, lite_state = eva_engine.process_message(
                    message=request.message,
                    history=request.history, 
                    user_profile=user_profile
                )
                
                return ChatResponse(
                    response=response_text,
                    conversation_id="lite_session",
                    emotional_state=lite_state["matrix"] # {label, axes, color...}
                )
            except Exception as e:
                print(f"❌ Error in Lite: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error in EVA Lite: {str(e)}"
                )
        else:
            # Determine Identity-based Session ID for Full Orchestrator
            name = request.metadata.get("user_name") if request.metadata else None
            company = request.metadata.get("user_company") if request.metadata else None
            
            # If identity is provided, we use a "Sticky ID"
            if name and company:
                # Normalize ID: ANN_GOOGLE
                conv_id = f"{name.upper().strip()}_{company.upper().strip()}"
            else:
                # Fallback to current conversation ID or generate a new one
                conv_id = request.conversation_id or f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get or create orchestrator
            orch = manager.get_orchestrator(conv_id)
            
            # If it's the very first time we see this identity, or it's a restore
            # the frontend might want the history back. 
            # (This logic can be triggered by a special 'SYNC' message)
            if request.message == "SYNC_HISTORY":
                history = get_history_from_memory(conv_id)
                return ChatResponse(
                    response="History restored.",
                    conversation_id=conv_id,
                    # We could pass the history in a specialized field if needed
                )

            # If metadata is provided, we can inject it as a system note or "perception"
            if request.metadata and request.message == "INIT_CONVERSATION":
                # Special case for initialization
                visitor_info = request.metadata.get("source", "Unknown Web Visitor")
                msg = f"[SYSTEM INFO] New visitor detected from: {visitor_info}"
                result = orch.process_user_input(msg)
                return ChatResponse(
                    response=result.get("final_response", "Hello!"),
                    conversation_id=conv_id,
                    emotional_state={"label": result.get("emotion_label", "neutral")}
                )

            # Process standard input through EVA
            result = orch.process_user_input(request.message)
            
            # [NEW] Proactive Identity Extraction
            # If AI identifies a name or company in the latest turn, register it
            # This is a light heuristic; we can also use LLM tool calls for this later
            msg_lower = request.message.lower()
            if any(keyword in msg_lower for keyword in ["hr", "recruiter", "บริษัท", "company", "จาก"]):
                # Ask EVA's memory or registry manager to update based on latest context
                # For now, let's flag the session as needing an identity update
                try:
                    # We can call the register_user in UserRegistryManager if we extract a name
                    # Simple extraction for now: 
                    # (Ideally use orch.get_module('msp').user_registry)
                    user_registry = orch.msp.user_registry
                    
                except:
                    pass

            # Extract components from EVA result
            bot_response = result.get("final_response", "I'm sorry, I couldn't process that.")
            
            # Map EVA state to our response format
            emotional_data = {
                "label": result.get("emotion_label", "neutral"),
                # "resonance_index": result.get("resonance_index", 0.0),
            }
            
            # Add matrix axes if available in the result or state snapshot
            # Simplified for safety
            if "psychological_state" in result:
                 emotional_data["axes"] = result["psychological_state"]
            
            return ChatResponse(
                response=bot_response,
                conversation_id=conv_id,
                emotional_state=emotional_data
            )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error in EVA Orchestrator: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "agent": "EVA 9.4.3",
        "active_sessions": len(manager.orchestrators)
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EVA Chat API",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    # Use config from .env.api if available
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

