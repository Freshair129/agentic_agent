import sys
import os
import json
import asyncio
import uvicorn
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List

# Add root to sys.path to access core modules
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from orchestrator.orchestrator import EVAOrchestrator
from capabilities.tools.logger import safe_print

from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
HOST = "127.0.0.1"
PORT = 8000

# --- FastAPI Setup ---
app = FastAPI(title="EVA Living Sandbox", version="9.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# --- EVA Core Instance ---
# We initialize this lazily or on startup
eva_node: EVAOrchestrator = None

class ConnectionManager:
    """Manages WebSocket connections for real-time state streaming."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                safe_print(f"[WS] Broadcast error: {e}")

manager = ConnectionManager()

# --- Models ---
class ChatInput(BaseModel):
    message: str
    session_id: str = "web_session_01" # Simplified for demo

# --- Lifecycle ---
# --- Background Simulation ---
async def simulate_life_loop():
    """
    Runs the physiological engine in a background loop at ~30Hz.
    This creates the 'living' baseline state.
    """
    global eva_node
    target_fps = 30
    frame_time = 1.0 / target_fps
    
    safe_print(f"[UI] Starting Life Loop at {target_fps}Hz...")
    
    last_time = asyncio.get_event_loop().time()
    
    while True:
        if eva_node and eva_node.physio:
            current_time = asyncio.get_event_loop().time()
            dt = current_time - last_time
            last_time = current_time
            
            # Run physio step
            # We pass empty stimuli as this is the "resting" loop
            # Real stimuli are injected via Orchestrator interaction
            try:
                # We need to run this potentially blocking sync code carefully
                # For 30Hz, overhead of run_in_executor might be high, but physio.step should be fast.
                # Let's try direct call if it's pure calc. If it lags, we move to thread.
                # physio.step is pure python math mostly.
                
                # Mock Zeitgebers for now (or get from system time)
                zeitgebers = {"light": 1.0} # Daytime default
                
                # --- TIME DILATION ---
                # User requested Real Time (1:1).
                # Reliance on Active Clearance (Heart Rate Coupling) for dynamics.
                TIME_DILATION_FACTOR = 1.0
                
                # Step the physics
                eva_node.physio.step(eva_stimuli=[], zeitgebers=zeitgebers, dt=dt * TIME_DILATION_FACTOR)
                
                # Get Snapshot
                # Optimize: Don't get full snapshot every frame if WS bandwidth is issue,
                # but user asked for 30Hz update.
                if len(manager.active_connections) > 0:
                    state = eva_node.physio.get_state()
                    
                    # Augment with Resonance Index if available
                    # We might need to fetch this from a shared state or cache
                    # For now just send physio state
                    
                    await manager.broadcast({
                        "type": "state_update",
                        "data": {
                            "physio_state": state,
                            "timestamp": current_time
                        }
                    })
                    
            except Exception as e:
                safe_print(f"[UI] Sim Loop Error: {e}")
                await asyncio.sleep(1) # Backoff
        
        # Maintain framerate
        elapsed = asyncio.get_event_loop().time() - last_time
        sleep_time = max(0, frame_time - elapsed)
        await asyncio.sleep(sleep_time)

@app.on_event("startup")
async def startup_event():
    global eva_node
    safe_print("[UI] Initializing EVA Orchestrator...")
    try:
        eva_node = EVAOrchestrator()
        safe_print("[UI] EVA Core Ready.")
        
        # Start Simulation Loop
        asyncio.create_task(simulate_life_loop())
        
    except Exception as e:
        safe_print(f"[UI] CRITICAL: Failed to load EVA Core: {e}")

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    """
    Process user message through EVA and return response.
    Also triggers a state broadcast.
    """
    if not eva_node:
        return {"error": "EVA Core not initialized"}

    user_text = input_data.message
    
    try:
        # Run synchronous orchestrator in threadpool to avoid blocking event loop
        # orchestration logic is sync, so we wrap it
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, eva_node.process_user_input, user_text)
        
        response_text = result.get("final_response", "...")
        
        # Prepare state update payload
        # Ensure we have robust defaults if keys are missing
        state_snapshot = result.get("state_snapshot", {})
        
        # Broadcast new state to all clients
        await manager.broadcast({
            "type": "state_update",
            "data": state_snapshot
        })

        # [NEW] Phase 4 Debug Info
        return {
            "response": response_text,
            "meta": {
                "confidence": result.get("confidence_score"),
                "resonance_index": result.get("resonance_index"),
                "anchor": result.get("salience_anchor"),
                "intent": result.get("intent", "N/A"),  # NEW
                "emotion": result.get("emotion_label", "N/A"),  # NEW
            },
            "debug": {  # NEW: Phase 4 Perception Delegation Debug
                "perception_delegated": result.get("confidence_score", 0) > 0.9,
                "slm_gut_vector": result.get("slm_gut_vector", {}),
                "step1_complete": True,
                "step2_complete": True,
                "step3_complete": True
            }
        }

    except Exception as e:
        safe_print(f"[UI] Chat Error: {e}")
        return {"error": str(e), "response": "⚠️ Critical Error in Cognitive Loop"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep client alive, maybe listen for specific commands
            data = await websocket.receive_text()
            # On connect/ping, we could send current state if we had access to it directly outside the loop
            # For now, we update on interaction. 
            pass 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        pass

@app.get("/health")
async def health_check():
    return {"status": "online", "eva_ready": eva_node is not None}

if __name__ == "__main__":
    # Use the app object directly to avoid import path issues when running from root
    uvicorn.run(app, host=HOST, port=PORT)
