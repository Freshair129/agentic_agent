# Prompt Rule Node (PRN)

**System**: Orchestrator (CNS)  
**Parent**: Context Injection Module (CIM)  
**Role**: Behavioral Constraint & Identity Management

## Overview

The Prompt Rule Node (PRN) is responsible for injecting behavioral constraints, identity anchors, and social protocols into the agent's context. It ensures that the agent's "personality" is consistent, governed by "Soul" and "Body" rules.

## Data Classification: Context Assets

We distinguish between **System Configuration** (technical settings) and **Context Assets** (intellectual property).

- **`assets/` (Formerly `configs/`)**: Stores the knowledge graphs and rule-sets that defined *who* the agent is.
    - `identity/`: Persona and Soul definitions.
    - `social/`: Relational protocols.
    - `biological/`: Autonomic reflex rules.
    - `cognitive/`: Thought structuring logic.

## Logic Flow

The `prompt_rule_node.py` loads these assets at runtime and constructs a "Rule Block" string that CIM injects into the LLM context.

## Usage

```python
from orchestrator.Module.CIM.Node.prompt_rule.prompt_rule_node import PromptRuleNode

prn = PromptRuleNode()
rule_block = prn.get_active_rules(physio_state=current_state)
```
