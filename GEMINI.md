# EVA v9.6.2 - Gemini Development Context

This document provides a comprehensive overview of the EVA v9.6.2 project, its architecture, and development conventions. It is intended to be used as a primary context file for Gemini AI assistants working on this project.

## 1. Project Overview

EVA is a highly complex, modular AI agent framework designed to simulate a "digital organism." It features a sophisticated architecture that models biological, psychological, and cognitive processes.

### Core Concepts:

*   **Digital Organism:** EVA is structured as a collection of interconnected "organs" or systems, each with a specific function (e.g., physiology, psychology, memory).
*   **Registry-Centric Governance:** The entire system is defined and governed by a central file, `registry/eva_master_registry.yaml`. This "master registry" specifies all systems, their dependencies, communication channels, and the boot sequence.
*   **Cognitive Flow 2.0:** The agent's reasoning process follows a three-phase cycle:
    1.  **Perception:** Initial processing of user input.
    2.  **The Gap:** Internal simulation of biological and psychological state changes.
    3.  **Reasoning:** Generation of a response based on the internal state.
*   **Resonance Bus:** A central messaging system that allows different components of the "organism" to communicate with each other in real-time.

### Key Systems:

*   **Orchestrator (`orchestrator/`):** The "Central Nervous System" that directs the cognitive flow and coordinates all other systems.
*   **PhysioCore (`physio_core/`):** Simulates the agent's physiological state (e.g., hormones, vitals).
*   **EVA_Matrix (`eva_matrix/`):** Manages the agent's 9-dimensional psychological and emotional state.
*   **MSP (Memory & Soul Passport) (`memory_n_soul_passport/`):** The long-term memory system responsible for storing and retrieving "episodes" and managing the agent's identity.
*   **GKS (Genesis Knowledge System) (`genesis_knowledge_system/`):** A curated, read-only repository of foundational knowledge, philosophies, and a-priori wisdom.
*   **API (`api/`):** A FastAPI application that exposes EVA to the outside world through REST endpoints and WebSockets for real-time interaction.

### Technology Stack:

*   **Language:** Python 3
*   **API Framework:** FastAPI
*   **Web Server:** Uvicorn
*   **Key Libraries:** Pydantic, python-dotenv, websockets

## 2. Building and Running

The primary entry point for running EVA is through the API server.

### Prerequisites:

Ensure all Python dependencies are installed:

```bash
pip install -r api/requirements.txt
```

### Running the Server:

To start the EVA API server, run the following command from the project root:

```bash
python api/run_server.py
```

By default, the server will be available at `http://0.0.0.0:8000`.

### API Endpoints:

*   **WebSocket:** `ws://localhost:8000/ws/chat/{session_id}` for real-time, stateful interaction.
*   **REST:** `POST /api/chat` for stateless request-response interaction.
*   **Health Check:** `GET /api/health` to check the system's status.

## 3. Development Conventions

This project follows a set of strict development conventions, primarily enforced by the `eva_master_registry.yaml`.

*   **Modularity:** The project is divided into numerous independent, single-responsibility modules (systems). Each module resides in its own directory.
*   **Documentation:** Every module should contain a `README.md` file explaining its purpose, structure, and interaction protocols.
*   **Configuration:** Configuration is managed through YAML files, with `registry/eva_master_registry.yaml` as the central authority. Individual systems may have their own `configs/` directory.
*   **Current Task:** The ongoing development task, as detailed in the `.planning/` directory, is to **Fix MSP Data Flow Gaps**. This involves modifying several schemas and Python files to ensure complete logging of the agent's internal state. Any development work should be aligned with the goals and steps outlined in `MSP_IMPLEMENTATION_CHECKLIST.md`.
*   **Branching:** For the current task, create a feature branch named `feature/msp-logging-gaps`.
*   **Code Style:** Follow existing code style and patterns. The code is heavily object-oriented and makes extensive use of type hints.
