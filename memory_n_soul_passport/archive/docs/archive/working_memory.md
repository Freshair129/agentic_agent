├── consciousness/              # [STORAGE] Database Files, MSP Chain
│   ├── 01_episodic_memory/     # [Narrative]
│   │   ├── episodes/           # Consolidated Full Episodes ({uuid}.json)
│   │   │   └── EVA_EP01.json
│   │   ├── episodes_user/      # User Input Artifacts
│   │   │   └── USER_EP01.json
│   │   ├── episodes_llm/       # EVA Response Artifacts
│   │   │   └── LLM_EP01.json
│   │   ├── schema/             # [Strict] Validation 
│   │   │   ├── Episodic_Memory_Schema_v2.json
│   │   │   ├── Episodic_User_Schema.json
│   │   │   ├── Episodic_LLM_Schema.json
│   │   │   ├── Episodic_Log_Schema.jsonl
│   │   │   └── Episodic_Index_Schema.json
│   │   ├── episodic_log.jsonl  # Linear History Logs
│   │   └── Episodic_memory_index.json # Search Index
│   │
│   ├── 02_semantic_memory/     # Semantic Knowledge Graph
│   │   ├── semantic/           # Consolidated Full Episodes ({uuid}.json)
│   │   │   └── EVA_SM01.json
│   │   ├── schema/             # [Strict] Validation Schemas
│   │   │   ├── Semantic_Memory_Schema_v2.json
│   │   │   ├── Semantic_Log_Schema.jsonl
│   │   │   └── Semantic_Index_Schema.json
│   │   ├── semantic_log.jsonl  # Linear History Log
│   │   └── Semantic_memory_index.json # Search Index
│   │   
│   ├── 03_sensory_memory/      # Sensory Vectors & Artifacts
│   │   ├── Artifacts/          # evidence pics, videos, etc.
│   │   ├── schema/             # [Strict] Validation Schemas
│   │   │   ├── Sensory_Memory_Schema_v2.json
│   │   │   └── Sensory_Log_Schema.jsonl
│   │   │   └── Sensory_Index_Schema.json
│   │   ├── sensory/            # sensory vectors
│   │   │   └── EVA_SEN01.json
│   │   ├── sensory_log.jsonl  # Linear History Log
│   │   └── Sensory_memory_index.json # Search Index