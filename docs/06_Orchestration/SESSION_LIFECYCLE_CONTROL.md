# ⏳ AuthDoc: Session Lifecycle Control

> **Status**: OPERATIONAL (v1.3.0 CNS-Node)
> **Governs**: `orchestrator/Node/session_node.py`

## 1. Core Role
The **Session Lifecycle Control** (Session Manager) is a direct autonomic node of the **Orchestrator (CNS)**. It is responsible for the temporal boundary and validity of a user-agent interaction.

Unlike functional modules (like CIM), this node is an **Autonomic Utility** that operates underneath the main cognitive flow to ensure system state integrity.

## 2. Key Responsibilities

### 2.1 Session Initialization
- Generates unique `session_id` tokens (delegated to `IdentityManager` protocol).
- Sets the `start_time` and `last_active` timestamps.
- Seeds the initial `turn_index` (001).

### 2.2 Activity Tracking
- Updates the "Liveliness" of the session on every bus signal.
- Monitors `ticks_since_last_input`.

### 2.3 Timeout & Expiration
- Enforces the **Session Expiration Protocol** (standard: 30 minutes of inactivity).
- Triggers `SESSION_EXPIRED` signal to the Orchestrator for cleanup and final archival.

### 2.4 State Buffer Management
- Managed the transient `cim_state.json` during the 8-8-8 protocol latching.

## 3. Integration with CNS
The Orchestrator invokes the Session Node at:
1.  **Awakening**: To validate if a returning user belongs to an active context.
2.  **Turn-Start**: To increment the turn sequence.
3.  **Turn-End**: To update persistence headers.

## 4. Path Mapping
- **Physical Node**: `orchestrator/Node/session_node.py`
- **Registry Link**: `Session_Node`

---
*Authorized CNS Documentation*
