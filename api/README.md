# EVA v9.6.2 API Layer

**Directory**: `api/`  
**Purpose**: Exposure of EVA Organism via REST and WebSocket interfaces.  
**Version**: 9.6.2 (Cognitive Flow 2.0 Ready)

---

## 📋 Overview

The API layer serves as the primary communication gateway for external interfaces (Web, Mobile, VR). It handles session management, WebSocket connections for real-time emotional feedback, and REST endpoints for stateless interactions.

---

## 📂 Components

### 1. `chat_endpoint.py`

The main FastAPI server providing:

- **WebSocket (`/ws/chat/{client_id}`)**: Real-time bidirectional communication with state updates (Matrix, RMS).
- **REST (`POST /api/chat`)**: Standard request-response interaction.
- **Health Check (`GET /api/health`)**: System status and active session count.

### 2. `eva_lite.py`

A lightweight implementation or wrapper for simplified deployments.

### 3. `run_server.py`

Entry point for starting the FastAPI development server.

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r api/requirements.txt
```

### Running the Server

```bash
python api/run_server.py
```

By default, the server runs on `http://0.0.0.0:8000`.

---

## 📡 API Specification (v9.6.2)

### WebSocket Flow

1. **Connect**: `ws://localhost:8000/ws/chat/{session_id}`
2. **Send**: `{"message": "Hello"}`
3. **Receive (Thinking)**: `{"type": "status", "status": "thinking"}`
4. **Receive (Response)**:

   ```json
   {
     "type": "response",
     "text": "Hello there!",
     "state": {
       "matrix": { "valence": 0.1, "arousal": 0.2, ... },
       "rms": { "color": "#... ", "intensity": 0.5 },
       "emotion_label": "calm"
     }
   }
   ```

### REST Endpoint

`POST /api/chat`

```json
{
  "message": "Hello",
  "conversation_id": "user_123"
}
```

---

## ⚖️ Governance & Policy

- **CORS**: Restricted to approved origins (Pronpon/Netlify/Vercel) and localhost.
- **Session Isolation**: Each session ID spawns an independent `EVAOrchestrator` instance.
- **Registry Compliance**: All runtime hooks and system sequences follow `eva_master_registry.yaml`.

---

*Maintained by EVA Infrastructure Team*
