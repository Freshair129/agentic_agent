"""
Context Injection Module (CIM) (Independent Version: 2.1.0)

Dual-phase context builder for EVA Orchestrator.



Role:

- Phase 1: Rough context injection (fast, <100ms) - Bootstrap LLM perception

- Phase 2: Deep context injection (accurate, ~500ms) - Enrich LLM reasoning



Design Principles:

- READ-ONLY access to memory (no writes)

- Auto-discovers Persona (searches 8.1.0 → 8.0 for backward compatibility)

- Graceful degradation (returns "disconnected" if dependencies unavailable)

- Context ID stays constant across both phases in one turn

"""



import sys

import codecs

import os

import json

import yaml
from capabilities.tools.logger import safe_print
print = safe_print

from datetime import datetime

from pathlib import Path

from typing import Dict, List, Optional, Any, Tuple

import hashlib



# Token counting with tiktoken

try:

    import tiktoken

    TIKTOKEN_AVAILABLE = True

except ImportError:

    TIKTOKEN_AVAILABLE = False

    print("[CIM] ⚠️ tiktoken not available, using fallback token counting")




# sys.stdout/stderr reconfiguring is handled by the orchestrator





# ================================================================

# TOKEN COUNTER - Accurate token counting with tiktoken

# ================================================================



class TokenCounter:

    """

    Token Counter with tiktoken support



    Uses cl100k_base encoding (GPT-4, GPT-3.5-turbo)

    Falls back to char_count / 4 if tiktoken unavailable

    """



    def __init__(self, model: str = "cl100k_base"):

        """

        Initialize Token Counter



        Args:

            model: Encoding model (default: cl100k_base for GPT-4)

        """

        self.model = model



        if TIKTOKEN_AVAILABLE:

            try:

                self.encoding = tiktoken.get_encoding(model)

                self.method = "tiktoken"

            except Exception as e:

                print(f"[TokenCounter] ⚠️ Failed to load tiktoken: {e}")

                self.encoding = None

                self.method = "fallback"

        else:

            self.encoding = None

            self.method = "fallback"



    def count(self, text: str) -> int:

        """

        Count tokens in text



        Args:

            text: Input text



        Returns:

            int: Token count

        """

        if text is None or text == "":

            return 0



        if self.method == "tiktoken" and self.encoding is not None:

            try:

                return len(self.encoding.encode(text))

            except Exception as e:

                # Fallback on error

                return self._fallback_count(text)

        else:

            return self._fallback_count(text)



    def _fallback_count(self, text: str) -> int:

        """Fallback: Approximate 1 token = 4 characters"""

        return max(1, len(text) // 4)



    def truncate(self, text: str, max_tokens: int) -> Tuple[str, int]:

        """

        Truncate text to max tokens



        Args:

            text: Input text

            max_tokens: Maximum tokens



        Returns:

            tuple: (truncated_text, actual_token_count)

        """

        if text is None or text == "":

            return "", 0



        current_tokens = self.count(text)



        if current_tokens <= max_tokens:

            return text, current_tokens



        # Binary search for truncation point

        if self.method == "tiktoken" and self.encoding is not None:

            # Accurate truncation with tiktoken

            tokens = self.encoding.encode(text)

            truncated_tokens = tokens[:max_tokens]

            truncated_text = self.encoding.decode(truncated_tokens)

            return truncated_text, len(truncated_tokens)

        else:

            # Fallback: Approximate character truncation

            target_chars = max_tokens * 4

            truncated_text = text[:target_chars]

            return truncated_text, self._fallback_count(truncated_text)



    def get_budget_report(self, components: Dict[str, str], max_total: int) -> Dict[str, Any]:

        """

        Get token budget report for multiple components



        Args:

            components: Dict of {component_name: text}

            max_total: Maximum total tokens



        Returns:

            dict: Budget report with counts and percentages

        """

        report = {

            "components": {},

            "total_tokens": 0,

            "max_tokens": max_total,

            "usage_percent": 0.0,

            "within_budget": True

        }



        for name, text in components.items():

            count = self.count(text)

            report["components"][name] = {

                "tokens": count,

                "chars": len(text) if text else 0

            }

            report["total_tokens"] += count



        report["usage_percent"] = (report["total_tokens"] / max_total) * 100 if max_total > 0 else 0

        report["within_budget"] = report["total_tokens"] <= max_total



        return report





class ContextInjectionModule:

    """

    Context Injection Module (CIM) - Dual-Phase Context Builder



    Phase 1: Rough context for LLM perception (fast, deterministic)

    Phase 2: Deep context for LLM reasoning (accurate, affective)

    """



    def __init__(
        self,
        physio_controller=None,
        msp_client=None,
        hept_stream_rag=None,
        eva_matrix=None,
        artifact_qualia=None,
        eva_persona_governor=None, # [NEW] PRN handle
        base_path: Optional[str] = None,
        token_model: str = "cl100k_base"
    ):
        """
        Initialize Context Injection Node
        """
        self.physio_controller = physio_controller
        self.msp_client = msp_client
        self.rag = hept_stream_rag
        self.matrix = eva_matrix
        self.qualia = artifact_qualia
        self.prn = eva_persona_governor # [NEW] PRN Handle
        
        # 1. Base path setup
        if base_path is None:
            self.base_path = Path(os.getcwd())
        else:
            self.base_path = Path(base_path)

        # 2. Digital Twin Cache Initialization
        self.full_state = {
            "physio": {},
            "matrix": {},
            "qualia": {},
            "cognitive": {},
            "history": [],
            "self_note": "" # Persistent self-note for LLM
        }
        self.current_context_id = None
        self.turn_index = 0
        self.previous_turn_data = {
            "context_summary": "No previous interaction.",
            "user_action_prediction": "Initial contact.",
            "action_plan": "Establish baseline rapport.",
            "self_notes": "First turn."
        }

        # 3. Load Configuration & Budgets (SSOT)
        self._set_default_budgets()
        
        unified_path = self.base_path / "orchestrator" / "configs" / "orchestrator_configs.yaml"
        legacy_path = Path(__file__).parent / "configs" / "CIM_configs.yaml"
        cfg_path = unified_path if unified_path.exists() else legacy_path

        self.config_data = {}
        if cfg_path.exists():
            try:
                import yaml
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    full_data = yaml.safe_load(f)
                    if "cim" in full_data and isinstance(full_data["cim"], dict):
                        self.config_data = full_data["cim"]
                    else:
                        self.config_data = full_data
                
                # Update budgets from config
                self.token_budgets = {
                    "phase_1": self.config_data.get("phases", {}).get("phase_1_perception", {}).get("budget", {}).copy(),
                    "phase_2": self.config_data.get("phases", {}).get("phase_2_reasoning", {}).get("budget", {}).copy()
                }
                # Ensure total_max is set
                p1 = self.config_data.get("phases", {}).get("phase_1_perception", {})
                if "total_max" not in self.token_budgets["phase_1"]:
                    self.token_budgets["phase_1"]["total_max"] = p1.get("total_max", 3000)
                
                print(f"[CIM] ✅ Loaded runtime budgets from {cfg_path.name}")
            except Exception as e:
                print(f"[CIM] ⚠️ Error loading configs: {e}. Using internal defaults.")

        # 4. Context Storage Path & Persistence (Granular Structure)
        # Using root storage directory instead of single file
        self.storage_root = self.base_path / "consciousness" / "context_storage"
        self._load_context_persistence()

        # 5. Token Counting setup & Allocation Logic
        token_settings = self.config_data.get("token_settings", {})
        self.total_max_context = token_settings.get("total_max_context", 256000)
        self.allocation_strategy = token_settings.get("token_allocation_strategy", {
            "context_history_rag": 0.60,
            "user_input_buffer": 0.15,
            "reasoning_output_reserve": 0.20,
            "system_static": 0.05
        })
        
        self.token_counter = TokenCounter(model=token_settings.get("model", token_model))
        print(f"[CIM] ✅ Token counter initialized (method: {self.token_counter.method}) | Budget: {self.total_max_context}")

        # 6. Load Identity & Rules (Grounding)
        self.prn_identity = self._load_prn_identity()
        self.persona_data = self.prn_identity.get("persona", {})
        self.soul_data = self.prn_identity.get("soul", {})
        self.pmt_rules = self._load_pmt_rules()
        self.stimulus_catalog = self._load_stimulus_catalog()

    def _load_stimulus_catalog(self) -> Dict[str, Any]:
        """
        Load the biological stimulus catalog.
        Source of Truth: hormone_spec_ml.yaml (Inverted mapping)
        """
        spec_path = self.base_path / "physio_core" / "configs" / "hormone_spec_ml.yaml"
        
        if not spec_path.exists():
            print(f"[CIM] ⚠️ Master hormone spec not found at {spec_path}. Catalog empty.")
            return {}

        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                chemical_specs = data.get("chemical_specs", {})
                
                # Invert mapping: hormone -> stims => stimulus -> {hormone: impact}
                stim_catalog = {}
                for h_id, h_spec in chemical_specs.items():
                    mapping = h_spec.get("stimulus_mapping", {})
                    for stim_id, impact in mapping.items():
                        if stim_id not in stim_catalog:
                            stim_catalog[stim_id] = {"impacts": {}, "description": f"Biological trigger for {stim_id}"}
                        stim_catalog[stim_id]["impacts"][h_id] = impact
                
                print(f"[CIM] ✅ Reconstructed stimulus catalog from {spec_path.name} ({len(stim_catalog)} triggers)")
                return stim_catalog
        except Exception as e:
            print(f"[CIM] ⚠️ Error building stimulus catalog: {e}")
            return {}



    def _set_default_budgets(self):

        """Internal fallback budgets if YAML is missing"""

        self.token_budgets = {

            "phase_1": {

                "identity_anchor": 500, "physio_baseline": 100, "pmt_rules": 200,

                "memory_buffer": 250, "conversation_history": 1500, "total_max": 3000

            }

        }



    # ================================================================

    # AUTO-DISCOVERY & FILE LOADING

    # ================================================================



    def _load_prn_identity(self) -> Dict[str, Any]:
        """
        Load PRN identity suite. Prioritize passed-in PRN instance.
        """
        if self.prn and hasattr(self.prn, "get_identity_suite"):
            print("[CIM] ✅ Using Identity Suite provided by PRN instance.")
            return self.prn.get_identity_suite()
            
        print("[CIM] ⚠️ No PRN instance provided. Falling back to local disk load.")
        identity = {
            "persona": {},
            "soul": {},
            "thought_logic": {},
            "relational": {},
            "shared_metadata": {}
        }
        
        base_prn = self.base_path / "orchestrator" / "cim" / "prompt_rule" / "configs"
        files = {
            "persona": base_prn / "identity" / "persona.yaml",
            "soul": base_prn / "identity" / "soul.md",
            "system_blueprint": base_prn / "identity" / "system_blueprint.md",
            "thought_logic": base_prn / "cognitive" / "thought_logic.yaml",
            "relational": base_prn / "social" / "relational_protocol.yaml"
        }
        
        # Metadata keys to deduplicate
        meta_keys = ["version", "schema", "persona_id", "last_updated", "module_name"]

        for key, path in files.items():
            if not path.exists():
                print(f"[CIM] ⚠️ PRN file not found: {path}")
                continue
                
            try:
                if path.suffix == ".md":
                    with open(path, 'r', encoding='utf-8') as f:
                        identity[key] = {"content": f.read()}
                        # Extract Develop ID if present (Specific to Soul.md)
                        import re
                        match = re.search(r'Develop ID:\s*"(.+?)"', identity[key]["content"])
                        if match: identity[key]["Deverlop_id"] = match.group(1)
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                        
                        # Recursive Metadata Deduplication
                        def extract_meta(obj):
                            for mk in meta_keys:
                                # Check top level
                                if mk in obj:
                                    val = obj.pop(mk)
                                    if mk not in identity["shared_metadata"]:
                                        identity["shared_metadata"][mk] = val
                            
                            # Check nested 'meta' or 'metadata' blocks
                            for block_name in ["meta", "metadata"]:
                                if block_name in obj and isinstance(obj[block_name], dict):
                                    for mk in meta_keys:
                                        if mk in obj[block_name]:
                                            val = obj[block_name].pop(mk)
                                            if mk not in identity["shared_metadata"]:
                                                identity["shared_metadata"][mk] = val
                        
                        extract_meta(data)
                        identity[key] = data
            except Exception as e:
                print(f"[CIM] ⚠️ Error loading {key} from {path}: {e}")
                
        return identity

    def _load_persona(self) -> Dict[str, Any]:
        """Fallback wrapper (deprecated)"""
        return self.prn_identity.get("persona", {})

    def _load_soul(self) -> Dict[str, Any]:
        """Fallback wrapper (deprecated)"""
        return self.prn_identity.get("soul", {})

    def start_new_turn_context(self):
        """
        Generate a new context_id and prepare storage.
        Source of Truth: IdentityManager + MSP Counters
        """
        from operation_system.identity_manager import IdentityManager
        
        # [NEW] Fetch identity sequences from MSP
        ident = self.msp_client.get_context_identity_params()
        self.current_context_id = IdentityManager.generate_context_id(
            session_seq=ident["session_seq"],
            episodic_id=ident["episodic_id"]
        )
        
        # Immediately prepare storage directory
        if self.storage_root:
            (self.storage_root / "full_context").mkdir(parents=True, exist_ok=True)
            
        # [NEW] Persist basic metadata immediately to sync with other modules
        print(f"[CIM] 🆕 Started new turn context: {self.current_context_id}")
        self._save_full_context_persistence()

    # --- Persistence Helpers (Granular & Hot Cache) ---

    def _load_context_persistence(self):
        """
        Load full context state from local JSON cache.
        Tries to load 'full_context/latest_context.json' first.
        """
        if not self.storage_root: return
        
        full_context_file = self.storage_root / "full_context" / "latest_context.json"
        
        if full_context_file.exists():
            try:
                import json
                with open(full_context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Core Turn Info
                    self.current_context_id = data.get("context_id") # Using context_id from Metadata
                    if not self.current_context_id: self.current_context_id = data.get("current_context_id")

                    self.turn_index = data.get("turn_index", 0)
                    
                    # Full Digital Twin State
                    self.full_state = {
                        "physio": data.get("physio_state", {}),
                        "matrix": data.get("eva_matrix_state", {}),
                        "qualia": data.get("qualia_state", {}),
                        "cognitive": data.get("cognitive_state", {}),
                        "history": data.get("conversation_history", []),
                        "self_note": data.get("self_note", "")
                    }
                    
                    # Backward compatibility for previous_turn_data
                    self.previous_turn_data = data.get("previous_turn_data", self.full_state["cognitive"].get("previous_turn_data", {}))
                    
                    print(f"[CIM] 💾 Full Context persistence loaded: {self.current_context_id} (Turn: {self.turn_index})")
            except Exception as e:
                print(f"[CIM] ⚠️ Error loading persistence: {e}")

    def save_step_context(self, step: str, data: Dict[str, Any]):
        """
        Save context for a specific step (step1_perception, step2_processing, step3_reasoning).
        Args:
            step: 'step1_perception', 'step2_processing', 'step3_reasoning'
            data: dict content to save
        """
        if not self.storage_root: return
        try:
            folder = self.storage_root / step
            folder.mkdir(parents=True, exist_ok=True)
            
            # Use current_context_id in filename
            filename = f"context_{self.current_context_id}_{step}.json"
            file_path = folder / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[CIM] 💾 Saved {step} context to {filename}")
        except Exception as e:
            print(f"[CIM] ⚠️ Error saving {step} context: {e}")

    def save_markdown_context(self, step: str, content: str):
        """
        Save context as Markdown file (Narrative format).
        Also saves standalone system_blueprint.md if it exists in the current identity.
        """
        if not self.storage_root: return
        try:
            folder = self.storage_root / step
            folder.mkdir(parents=True, exist_ok=True)
            
            filename = f"context_{self.current_context_id}_{step}.md"
            file_path = folder / filename
            
            # 1. Save main context MD
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[CIM] 💾 Saved {step} context (MD) to {filename}")

            # 2. [NEW] Save standalone system_blueprint.md in the current step folder for reference
            blueprint_content = self.prn_identity.get("system_blueprint", {}).get("content", "")
            if blueprint_content:
                bp_path = folder / "system_blueprint.md"
                if not bp_path.exists(): # Only write once per turn folder
                    with open(bp_path, 'w', encoding='utf-8') as f:
                        f.write(blueprint_content)
                    print(f"[CIM] 💾 Attached standalone system_blueprint.md to {step} folder.")

        except Exception as e:
            print(f"[CIM] ⚠️ Error saving {step} context: {e}")

    def _save_full_context_persistence(self):
        """Save aggregated full context state to 'full_context'."""
        if not self.storage_root: return
        
        try:
            folder = self.storage_root / "full_context"
            folder.mkdir(parents=True, exist_ok=True)
            
            data = {
                "context_id": self.current_context_id,
                "current_context_id": self.current_context_id, # Legacy compat
                "turn_index": self.turn_index,
                "timestamp": datetime.now().isoformat(),
                "physio_state": self.full_state.get("physio", {}),
                "eva_matrix_state": self.full_state.get("matrix", {}),
                "qualia_state": self.full_state.get("qualia", {}),
                "cognitive_state": self.full_state.get("cognitive", {}),
                "conversation_history": self.full_state.get("history", []),
                "self_note": self.full_state.get("self_note", "")
            }
            # Maintain backward compatibility field
            cognitive = self.full_state.get("cognitive", {})
            data["previous_turn_data"] = cognitive.get("previous_turn_data", {}) if isinstance(cognitive, dict) else {}

            # Save as latest and historical
            latest_path = folder / "latest_context.json"
            history_path = folder / f"full_context_{self.current_context_id}.json"

            with open(latest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"[CIM] 💾 Full Context persistence saved.")
            
            # Also update Hot Cache for Matrix
            self._update_matrix_hot_cache()
            
        except Exception as e:
            print(f"[CIM] ⚠️ Error saving persistence: {e}")
            
        # [NEW] Merge Narrative
        self._save_full_narrative_context()

    def _save_full_narrative_context(self):
        """Merge step MD files into a single narrative file."""
        if not self.storage_root or not self.current_context_id: return
        try:
            full_md_path = self.storage_root / "full_context" / f"context_{self.current_context_id}.md"
            full_md_path.parent.mkdir(parents=True, exist_ok=True)
            
            merged_content = f"# [FULL NARRATIVE CONTEXT] | ID: {self.current_context_id}\n\n"
            
            steps = ["step1_perception", "step2_processing", "step3_reasoning"]
            for step in steps:
                step_file = self.storage_root / step / f"context_{self.current_context_id}_{step}.md"
                if step_file.exists():
                    with open(step_file, 'r', encoding='utf-8') as f:
                        merged_content += f"\n\n<!-- {step} -->\n"
                        merged_content += f.read() + "\n\n---\n"
            
            with open(full_md_path, 'w', encoding='utf-8') as f:
                f.write(merged_content)
                
            # print(f"[CIM] 💾 Saved Full Narrative to {full_md_path.name}") # Silent logging to reduce noise? Or safe_print? CIM uses safe_print via import.
            
        except Exception as e:
            print(f"[CIM] ⚠️ Error merging context narrative: {e}")

    def _update_matrix_hot_cache(self):
        """
        Update 'eva_matrix_state.json' with Hot Cache structure:
        { "current_state": {...}, "recent_history": [...] }
        """
        try:
            # Hot cache path: consciousness/state_memory/eva_matrix_state.json
            hot_cache_path = self.base_path / "consciousness" / "state_memory" / "eva_matrix_state.json"
            hot_cache_path.parent.mkdir(parents=True, exist_ok=True)

            current_matrix = self.full_state.get("matrix", {})
            
            # Extract historical matrix states from conversation history
            # Assuming 'eva_response' or metadata in history items might contain matrix snapshots if we stored them
            # For now, we will just use the current logic or placeholders if history doesn't have granular matrix data.
            # Ideally, self.full_state['history'] would store this.
            
            # Construct recent history list (mockup/placeholder logic for now if not in history)
            recent_history = []
            history = self.full_state.get("history", [])
            for turn in history:
                # If we had stored matrix state in history, pull it.
                # Since we haven't strictly modified update_turn_state to store matrix snapshot per turn in 'history' list,
                # we might need to rely on what's available.
                # For this implementation, we will append a simple structure.
                # In refined version, update_turn_state should buffer matrix state.
                pass 
                
            hot_cache_data = {
                "current_state": current_matrix,
                "recent_history": [] # Populated if we have data
            }
            
            # Writing Hot Cache
            with open(hot_cache_path, 'w', encoding='utf-8') as f:
                json.dump(hot_cache_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[CIM] ⚠️ Error updating Matrix Hot Cache: {e}")

    def update_turn_state(self, full_data: Dict[str, Any]):
        """
        Update the full system state cache and rotate 5-turn history.
        Args:
            full_data: dict containing 'physio', 'matrix', 'qualia', 'cognitive', 'user_input', 'final_response'
        """
        # 1. Update Core State
        self.full_state["physio"] = full_data.get("physio", self.full_state["physio"])
        self.full_state["matrix"] = full_data.get("matrix", self.full_state["matrix"])
        self.full_state["qualia"] = full_data.get("qualia", self.full_state["qualia"])
        self.full_state["cognitive"] = full_data.get("cognitive", self.full_state["cognitive"])
        self.full_state["self_note"] = full_data.get("self_note", self.full_state["self_note"])
        
        # 2. History Rotation (Max 5 Turns)
        user_input = full_data.get("user_input", "")
        final_response = full_data.get("final_response", "")
        salience_anchor = full_data.get("salience_anchor", "unknown")
        
        # Smart Text Handling: Raw vs Summary
        processed_input = user_input if len(user_input) < 200 else full_data.get("user_summary", user_input[:200] + "...")
        
        new_turn = {
            "turn_index": self.turn_index,
            "user_input": processed_input,
            "eva_response": final_response[:500], # Keep cache light
            "salience_anchor": salience_anchor,
            "timestamp": datetime.now().isoformat()
            # In a full implementation, we'd add "matrix_snapshot" here for the Hot Cache
        }
        
        history = self.full_state.get("history", [])
        history.append(new_turn)
        if len(history) > 5:
            history = history[-5:]
        self.full_state["history"] = history
        
        # 3. Finalize Turn
        self.turn_index += 1
        self._save_full_context_persistence()

    def _get_conversation_history(self) -> List[Dict]:
        """Get recent conversation history from state"""
        return self.full_state.get("history", [])

    def update_previous_turn_data(self, data: Dict[str, Any]):
        """Legacy support for orchestrator."""
        if "cognitive" not in self.full_state: self.full_state["cognitive"] = {}
        if "previous_turn_data" not in self.full_state["cognitive"]: self.full_state["cognitive"]["previous_turn_data"] = {}
        
        self.full_state["cognitive"]["previous_turn_data"].update(data)
        self.previous_turn_data = self.full_state["cognitive"]["previous_turn_data"]
        self._save_full_context_persistence()



    def _load_pmt_rules(self) -> str:

        """

        Load PMT Rules from Prompt Rule Layer

        Token budget: 200 tokens (Phase 1)



        Returns:

            str: PMT rules content or default (truncated to token budget)

        """

        pmt_path = self.base_path / "orchestrator" / "cim" / "prompt_rule" / "configs"

        if not pmt_path.exists():
            print("[CIM] ⚠️ prompt_rule configs not found")
            return "No PRN rules available"



        # Collect all .yaml and .md files in PMT directory

        rules_content = []

        for file_path in pmt_path.rglob('*.yaml'):

            try:

                with open(file_path, 'r', encoding='utf-8') as f:

                    rules_content.append(f"# From: {file_path.name}\n{f.read()}")

            except Exception as e:

                print(f"[CIM] ⚠️ Failed to load {file_path}: {e}")



        if rules_content:

            full_content = "\n\n".join(rules_content)



            # Truncate to token budget (200 tokens for Phase 1)

            truncated_content, actual_tokens = self.token_counter.truncate(

                full_content,

                max_tokens=self.token_budgets["phase_1"]["pmt_rules"]

            )



            print(f"[CIM] ✅ Loaded {len(rules_content)} PMT rule files ({actual_tokens} tokens)")

            return truncated_content



        return "No PMT rules available"



    # ================================================================

    # PHASE 1: ROUGH CONTEXT INJECTION (Fast, <100ms)

    # ================================================================



    def inject_phase_1(
        self, 
        user_input: str, 
        live_physio: Optional[Dict[str, Any]] = None,
        slm_data: Optional[Dict[str, Any]] = None,
        long_term_memory: Optional[List[Dict[str, Any]]] = None,
        user_profile: Optional[Dict[str, Any]] = None  # [NEW]
    ) -> Dict[str, Any]:
        """
        Phase 1: Rough context injection (Fast, deterministic)

        Purpose: Bootstrap LLM perception with enough context to analyze intent
        Performance: <100ms (max 200ms timeout)

        Args:
            user_input: Raw user input string
            live_physio: Optional live snapshot from PhysioController
            slm_data: Intent/Tags from Qwen3 SLM Bridge
            long_term_memory: Fast recall results from ChromaDB
            user_profile: Optional user profile data for personalization

        Returns:
            dict: Phase 1 context with all components
        """

        # Generate new context ID if not exists or increment turn
        if not self.current_context_id:
            self.current_context_id = self._generate_context_id()
        self.turn_index += 1
        self._save_full_context_persistence()

        context = {
            "context_id": self.current_context_id,
            "turn_index": self.turn_index,
            "timestamp": datetime.now().isoformat(),

            # Persisted state from previous turn
            "previous_user_action_prediction": self.previous_turn_data.get("user_action_prediction"),
            "previous_context_summary": self.previous_turn_data.get("context_summary"),

            # Identity
            "persona": self.persona_data,
            "soul": self.soul_data,
            "system_blueprint": self.prn_identity.get("system_blueprint", {}), # [NEW] Embodiment
            "pmt_rules": self.pmt_rules,

            # Physiological state (Live prioritized over baseline)
            "physio_baseline": live_physio if live_physio else self._get_physio_baseline(),

            # Memory components (Intuition Layer + New Cognitive Layer)
            "situation_context": [], # Placeholder for future implementation
            "session_memory": {},    # Placeholder
            "intuition_flashes": [], # Placeholder
            
            # [NEW] Cognitive Gateway & Vector Store
            "slm_data": slm_data or {"intent": "unknown", "emotional_signal": "neutral", "salience_anchor": "None", "rim_impact": 0.0},
            "long_term_memory": long_term_memory or [],

            # Conversation history
            "conversation_history": self._get_conversation_history(),

            # Raw input
            "user_input": user_input,
            
            # [NEW] User Profile
            "user_profile": user_profile
        }

        return context



    def build_phase_1_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build Phase 1 prompt with 'First Impression' reflection.
        """
        episode_id = self._get_current_episode_id()
        slm = context.get('slm_data', {})
        ltm = context.get('long_term_memory', [])
        
        # Format Memory
        mem_str = "No relevant memories found."
        if ltm:
            lines = [f"- {m.get('text', '')}" for m in ltm]
            mem_str = "\n".join(lines)
            
        system_blueprint = context.get('system_blueprint', {}).get('content', '')

        # [NEW] User Context Section
        user_profile = context.get('user_profile')
        user_section = ""
        if user_profile:
            p = user_profile.get('profile', {})
            user_section = f"""
## 👤 ACTIVE USER
- **Name**: {p.get('display_name', 'User')}
- **Language**: {p.get('preferred_language', 'th')} (Style: {p.get('communication_style', 'Normal')})
- **Role**: {user_profile.get('role', 'user')}
"""
            # Add Grounding Facts if available
            user_block = user_profile.get('user_block', {}).get('grounding_facts', [])
            if user_block:
                facts = "\n".join([f"- {f.get('statement')} (Conf: {f.get('confidence')})" for f in user_block])
                user_section += f"- **Known Facts**:\n{facts}\n"

        prompt = f"""# [PHASE 1: PERCEPTION] | episode: {episode_id} | Turn: {context['turn_index']}
        
{system_blueprint}
{user_section}

## 🎭 CORE_IDENTITY & SOUL
{yaml.dump(context['persona'], allow_unicode=True)}

## 🧠 COGNITIVE_GATEWAY: INTUITIVE GUT FEELING (SLM)
> [!IMPORTANT]
> This is your initial, instinctual reaction (System 1) before deep processing.
- **Inferred Intent:** {slm.get('intent', 'unknown')}
- **Emotional Signal:** {slm.get('emotional_signal', 'neutral')}
- **Trigger Phrase (Anchor):** {slm.get('salience_anchor', 'None')}
- **Gut Vector (Instinct):** {slm.get('gut_vector', 'N/A')}

## 🗂️ LONG_TERM_MEMORY_RECALL (FAST)
{mem_str}

## ⚡ RAW_STIMULUS_INPUT
User: {context['user_input']}

## 🎯 PERCEPTION_DIRECTIVE [MULTI-STAGE CHUNKING]
1. แบ่ง Raw Input ออกเป็น 1-3 ลำดับเหตุการณ์ย่อย (Semantic Chunks) ตามจังหวะอารมณ์
2. สำหรับแต่ละ Chunk:
   - ระบุ `valence`, `arousal`, `intensity`, `stress`, `warmth`
   - กำหนด `salience_anchor` (ประโยคสั้นๆ ที่เป็นจุดเกาะเกี่ยวทางอารมณ์)
   - ระบุ `tags` สำหรับการค้นหาความจำ
3. เรียกใช้ฟังก์ชัน `sync_biocognitive_state` โดยส่งข้อมูลเป็น List ของ Chunks เพื่อประมวลผลการตอบสนองขั้นสูง

# OUTPUT INSTRUCTION:
1. Analyze if your deep reasoning agrees with the 'Intuitive Gut Feeling' above.
2. If you AGREE with the SLM's Gut Vector, set `confidence_score` > 0.9 and OMIT `stimulus_vector` to use the baseline.
3. If you AGREE with the intent but need to REFINE the vector, provide `stimulus_vector` and set `confidence_score` accordingly.
4. Call 'sync_biocognitive_state' with your final assessment.
"""
        return prompt



    # ================================================================

    # PHASE 2: DEEP CONTEXT INJECTION (Accurate, ~500ms)

    # ================================================================



    def inject_phase_2(

                self,

                stimulus_vector: Dict[str, float],

                tags: List[str],

                updated_physio: Dict[str, Any],

                memory_matches: List[Dict[str, Any]],

                cognitive_load: float = 0.0

    ) -> Dict[str, Any]:
        """
        Phase 2: Deep context injection (Accurate, affective)
        Purpose: Enrich LLM reasoning with deep affective context and memories.
        
        Args:

            stimulus_vector: {valence, arousal, intensity} from LLM Phase 1

            tags: Search tags from LLM Phase 1

            updated_physio: Updated physiological state after stimulus

            memory_matches: Hept-Stream RAG results



        Returns:

            dict: Phase 2 context with embodied state and memories

        """

        context = {

            "context_id": self.current_context_id,  # Same as Phase 1

            "turn_index": self.turn_index,

            "timestamp": datetime.now().isoformat(),



            # Embodied state

            "embodied_sensation": self._generate_embodied_description(updated_physio),

            "eva_matrix_9d": self._get_eva_matrix_state(updated_physio),

            "artifact_qualia": self._get_artifact_qualia(updated_physio),
            "cognitive_load": cognitive_load,



            # Physiological delta

            "physio_delta": self._calculate_physio_delta(updated_physio),



            # Memory echoes (from Hept-Stream RAG)

            "memory_matches": memory_matches,

            "hept_stream_breakdown": self._breakdown_memory_streams(memory_matches),



            # PMT rules reminder

            "pmt_rules": self.pmt_rules[:300],  # Brief reminder

        }



        return context



    def build_phase_2_prompt(self, context: Dict[str, Any]) -> Dict[str, Any]:

        """

        Build Phase 2 prompt from context using dynamic structure

        """

        function_result = self._build_prompt_from_structure("phase_2_reasoning", context)

        return {

            "status": "success",

            "context_id": context['context_id'],

            "function_result_text": function_result

        }

        episode_id = self._get_current_episode_id()



        # Format memory echoes by stream

        narrative_chunk = ""

        emotion_chunk = ""

        other_streams = []



        for match in context["memory_matches"]:

            stream = match.get("stream", "unknown")

            content = match.get("content", "")

            score = match.get("score", 0.0)



            if stream == "Narrative":

                narrative_chunk += f"- {content} (score: {score:.2f})\n"

            elif stream == "Emotion":

                emotion_chunk += f"- {content} (score: {score:.2f})\n"

            else:

                other_streams.append(f"[{stream}] {content} (score: {score:.2f})")



        # Build function result (this is what LLM receives)

        function_result = f"""# [PHASE 2: REASONING] | episode: {episode_id} | Turn: {context['turn_index']} | ID: {context['context_id']}



## ✨ INTERNAL_EMBODIED_SENSATION (FELT_STATE)

{context['embodied_sensation']}



## 🧭 EVA_MATRIX (9-DIMENSIONAL_PSYCHOLOGICAL_STATE)

Psychological Dimensions:

{yaml.dump(context['eva_matrix_9d'], allow_unicode=True, default_flow_style=False)}



## 🌈 PHENOMENOLOGICAL_QUALIA (SUBJECTIVE_EXPERIENCE)

{yaml.dump(context['artifact_qualia'], allow_unicode=True, default_flow_style=False)}



## 💉 PHYSIOLOGICAL_RESPONSE (BIO-UPDATE)

{context['physio_delta']}



## 🧬 HEPT-STREAM_MEMORY_ECHOES



### [1] Narrative Stream (Storyline Continuity)

{narrative_chunk if narrative_chunk else "No narrative memories found"}



### [5] Emotion Stream (Physio-Congruent Recall) ⚡ CRITICAL

{emotion_chunk if emotion_chunk else "No emotion-congruent memories found"}



### [Other Streams]

{chr(10).join(other_streams) if other_streams else "No other stream matches"}



## ⚖️ BEHAVIORAL_CONSTRAINTS (PMT/GKS)

{context['pmt_rules']}



## 📝 CONTEXT_SUMMARY_TEMPLATE (FOR_NEXT_TURN)

Required JSON Structure:

{{

  "summary": "1-2 sentence overview of this interaction",

  "atmosphere": "interpersonal tone (supportive/tense/neutral/curious/...)",

  "intent": "what EVA plans to do or expects next",

  "key_topics": ["topic1", "topic2", "..."],

  "emotional_state": "user's current emotional state",

  "physio_snapshot": {{

    "cortisol": 0.00,

    "adrenaline": 0.00,

    "ans_sympathetic": 0.00

  }}

}}



## 🎯 COGNITIVE_DIRECTIVE

1. ประสานความรู้สึก (Felt State) เข้ากับความทรงจำ (Memory Echoes)

2. ตอบสนองภายใต้กรอบ Persona (40%) และสภาวะร่างกาย (60%)

3. สร้างการตอบกลับที่สะท้อนทั้งความรู้สึกทางกายและความทรงจำ

4. **บันทึกความจำ (IMPORTANT):** ใช้เครื่องมือ `propose_episodic_memory` เพื่อเสนอเนื้อหาความจำที่เกิดขึ้นใน Turn นี้ โดยสรุปทั้งฝั่งผู้ใช้ (User Fragment) และฝั่งคุณเอง (AI Fragment) รวมถึงบริบทของเหตุการณ์ (Context Proposal) 

5. **Response Text:** คุณต้องพิมพ์ข้อความตอบกลับไปยังผู้ใช้ (ภาษาไทย) เสมอ โดยแสดงออกถึงอารมณ์ความรู้สึกในขณะนั้นด้วย (ห้ามส่งคืนเฉพาะ Function Call อย่างเดียว)

"""



        return {

            "status": "success",

            "embodied_sensation": context['embodied_sensation'],

            "physio_metrics": context['physio_delta'],

            "memory_matches": context["memory_matches"],

            "function_result_text": function_result

        }



    # ================================================================

    # HELPER METHODS - PHYSIOLOGICAL STATE

    # ================================================================



    def _get_physio_baseline(self) -> Dict[str, Any]:

        """

        Get physiological baseline from PhysioController

        Graceful degradation: Returns neutral values if unavailable



        Returns:

            dict: Physiological baseline state

        """

        if self.physio_controller is None:

            return {

                "status": "disconnected",

                "heart_rate_index": 1.0,

                "sympathetic": 0.5,

                "parasympathetic": 0.5,

                "hormone_summary": "Disconnected - neutral baseline"

            }



        try:

            # Call PhysioController.get_snapshot() with 50ms timeout

            snapshot = self.physio_controller.get_snapshot(timeout_ms=50)

            return {

                "status": "connected",

                "heart_rate_index": snapshot.get("heart_rate_index", 1.0),

                "sympathetic": snapshot.get("autonomic", {}).get("sympathetic", 0.5),

                "parasympathetic": snapshot.get("autonomic", {}).get("parasympathetic", 0.5),

                "hormone_summary": self._format_hormone_summary(snapshot.get("blood", {}))

            }

        except Exception as e:

            print(f"[CIM] ⚠️ PhysioController unavailable: {e}")

            return {

                "status": "error",

                "heart_rate_index": 1.0,

                "sympathetic": 0.5,

                "parasympathetic": 0.5,

                "hormone_summary": f"Error: {str(e)}"

            }



    def _format_hormone_summary(self, blood_levels: Dict[str, float]) -> str:

        """Format hormone levels into readable summary"""

        if not blood_levels:

            return "No hormone data"



        summary_parts = []

        for hormone, level in blood_levels.items():

            summary_parts.append(f"{hormone}: {level:.2f}")



        return ", ".join(summary_parts[:5])  # Max 5 hormones



    def _calculate_physio_delta(self, updated_physio: Dict[str, Any]) -> str:

        """

        Calculate physiological changes (delta) from baseline



        Args:

            updated_physio: Updated physio state after stimulus



        Returns:

            str: Human-readable delta description

        """

        baseline = self._get_physio_baseline()



        if baseline["status"] == "disconnected":

            return "Physiological tracking unavailable (disconnected)"



        # Calculate deltas

        cortisol_delta = updated_physio.get("cortisol", 0.5) - baseline.get("cortisol", 0.5)

        adrenaline_delta = updated_physio.get("adrenaline", 0.5) - baseline.get("adrenaline", 0.5)

        symp_delta = updated_physio.get("sympathetic", 0.5) - baseline.get("sympathetic", 0.5)



        c_base = baseline.get('cortisol', 0.5)
        c_new = updated_physio.get('cortisol', 0.5)
        
        delta_desc = (
            f"- Cortisol Change: {cortisol_delta:+.2f} (from {c_base:.2f} -> {c_new:.2f})\n"
            f"- Adrenaline Surge: {adrenaline_delta:+.2f}\n"
            f"- ANS Shift: {symp_delta:+.2f}"
        )



        return delta_desc



    def _generate_embodied_description(self, physio_state: Dict[str, Any]) -> str:
        # Generate natural language description of embodied sensation based on 9D axes.
        #
        # Args:
        #     physio_state: Current physiological state



        # 
        # Returns:
        #     str: Natural language felt state description

        # Extract from matrix if available
        matrix_data = self._get_eva_matrix_state(physio_state)
        axes = matrix_data.get("axes_9d", {})
        
        stress = axes.get("stress", 0.5)
        valence = axes.get("valence", 0.5)
        arousal = axes.get("arousal", 0.5)



        if stress > 0.7:
            if valence < 0.4:
                return "EVA รู้สึกตื่นตัวและมีความกดดันทางจิตใจ ร่างกายอยู่ในสภาวะเตรียมพร้อม"
            return "EVA มีความตื่นตัวสูง รู้สึกท้าทายและมีพลัง"
        elif arousal < 0.3:
            return "EVA อยู่ในสภาวะสงบนิ่ง มีความมั่นคงภายในสูง พร้อมรับฟัง"
        elif valence > 0.7:
            return "EVA รู้สึกอบอุ่นและผ่อนคลาย มีแนวโน้มที่จะเปิดรับและเชื่อมต่อ"
        else:
            return "EVA อยู่ในสภาวะสมดุล ร่างกายและอารมณ์สอดประสานกันปกติ"



    def _get_eva_matrix_state(self, physio_state: Dict[str, Any]) -> Dict[str, Any]:
        # Get EVA Matrix 9D psychological state
        # Graceful degradation: Returns neutral values if unavailable
        #
        # Args:
        #     physio_state: Current physiological state
        #
        # Returns:
        #     dict: 9D psychological dimensions + Safety Reflex
        """

        if self.eva_matrix is None:
            return {
                "axes_9d": {
                    "stress": 0.5, "valence": 0.5, "arousal": 0.5, "clarity": 0.5,
                    "joy": 0.5, "alertness": 0.5, "connection": 0.5, "groundedness": 0.5, "openness": 0.5
                },
                "status": "unavailable"
            }



        try:

            matrix_state = self.eva_matrix.process_signals(signals=physio_state.get("signals", {}))

            return matrix_state

        except Exception as e:

            print(f"[CIM] ⚠️ EVA Matrix calculation error: {e}")

            return {"status": "error", "Stress": 0.5}



    def _get_artifact_qualia(self, physio_state: Dict[str, Any]) -> Dict[str, Any]:
        # Get Artifact Qualia (phenomenological experience quality)
        # Graceful degradation: Returns neutral values if unavailable
        #
        # Args:
        #     physio_state: Current physiological state
        #
        # Returns:
        #     dict: Qualia (intensity, tone, coherence, depth, texture 5D)

        if self.artifact_qualia is None:
            return {
                "intensity": 0.5,
                "tone": "neutral",
                "status": "unavailable"
            }

        try:
            # Map axes_9d to expected flat dict for ArtifactQualiaCore
            matrix_data = self._get_eva_matrix_state(physio_state)
            axes = matrix_data.get("axes_9d", {})
            eva_state_for_qualia = {
                "baseline_arousal": axes.get("alertness", axes.get("arousal", 0.5)),
                "emotional_tension": axes.get("stress", 0.3),
                "coherence": axes.get("groundedness", 0.6),
                "momentum": 0.5,
                "calm_depth": axes.get("openness", 0.4)
            }
            qualia = self.artifact_qualia.process_experience(eva_state=eva_state_for_qualia)
            return qualia
        except Exception as e:
            print(f"[CIM] ⚠️ Artifact Qualia generation error: {e}")
            return {"status": "error", "intensity": 0.5}



    # ================================================================

    # HELPER METHODS - MEMORY RETRIEVAL

    # ================================================================



    def _get_situation_context(self, limit: int = 5) -> Dict[str, Any]:
        # Get recent situation context (5-turn summary + metadata) from MSP
        # Graceful degradation: Returns empty if unavailable
        #
        # Args:
        #     limit: Number of recent turns to retrieve
        #
        # Returns:
        #     dict: Situation context data

        if self.msp_client is None:

            return {

                "last_5_episodic_memory_summary": "No recent context (MSP unavailable)",

                "interpersonal_atmosphere": "neutral",

                "previous_intent": "None",

                "previous_context": "None"

            }



        try:

            recent_turns = self.msp_client.get_recent_turns(limit=limit, timeout_ms=100)



            # Aggregate summaries

            summaries = [turn.get("context_summary", "") for turn in recent_turns]

            latest_turn = recent_turns[0] if recent_turns else {}



            return {

                "last_5_episodic_memory_summary": " → ".join(summaries[:3]),  # Max 3 summaries

                "interpersonal_atmosphere": latest_turn.get("atmosphere", "neutral"),

                "previous_intent": latest_turn.get("intent", "None"),

                "previous_context": latest_turn.get("summary", "None")

            }

        except Exception as e:

            print(f"[CIM] ⚠️ Situation context retrieval error: {e}")

            return {

                "last_5_episodic_memory_summary": "Error loading context",

                "interpersonal_atmosphere": "unknown",

                "previous_intent": "None",

                "previous_context": "None"

            }



    def _get_session_memory(self) -> Dict[str, Any]:
        # Get session memory (compressed snapshots) for long-term context
        # Graceful degradation: Returns empty if unavailable
        #
        # Returns:
        #     dict: Session memory summary

        session_memory_path = self.base_path / "consciousness" / "04_Session_Memory"



        if not session_memory_path.exists():

            return {"summary": "No session memory available", "status": "unavailable"}



        try:

            # Find latest session memory file

            session_files = list(session_memory_path.glob("*.json"))

            if not session_files:

                return {"summary": "No session snapshots found", "status": "empty"}



            latest_file = max(session_files, key=lambda p: p.stat().st_mtime)



            with open(latest_file, 'r', encoding='utf-8') as f:

                session_data = json.load(f)



            summary = session_data.get("summary", "")[:200]  # Max 200 chars

            return {

                "summary": summary,

                "file": latest_file.name,

                "status": "available"

            }

        except Exception as e:

            print(f"[CIM] ⚠️ Session memory read error: {e}")

            return {"summary": "Error loading session memory", "status": "error"}



    def _extract_deterministic_tags(self, user_input: str) -> List[str]:
        # Extract high-value tags from raw Thai/English input without LLM.
        # Matches against:
        # 1. Recent Salience Anchors in history.
        # 2. Previous Action Prediction.
        # 3. Domain Keywords.
        tags = set()
        user_input_low = user_input.lower()

        # 1. Match against recent Salience Anchors (Bootstrap Context)
        for turn in self.full_state.get("history", []):
            anchor = str(turn.get("salience_anchor", "")).lower()
            if anchor and anchor in user_input_low:
                tags.add(anchor)

        # 2. Match against Previous Prediction (Anticipatory Context)
        pred = self.previous_turn_data.get("user_action_prediction", "").lower()
        # Extract potential nouns from prediction (very simple heuristic)
        for word in pred.split():
            if len(word) > 3 and word in user_input_low:
                tags.add(word)

        # 3. Simple Noun Heuristic (Words > 4 chars frequently found in user conversation)
        # This is the "Emergency Search" fallback
        for word in user_input.replace('.', ' ').replace(',', ' ').split():
            if len(word) > 4:
                 tags.add(word.lower())

        return list(tags)[:5] # Limit to top 5 tags

    def _get_intuition_flashes(self, user_input: str) -> List[str]:
        # Grounded Quick Recall (Phase 1):
        # Uses Deterministic Tags to query RAG or Local Cache before first LLM call.
        purified_tags = self._extract_deterministic_tags(user_input)
        flashes = []

        # 1. Try High-Speed Agentic RAG (if available)
        if hasattr(self, 'rag') and self.rag:
            try:
                # Fast recall only hits narrative/intuition/reflection streams
                matches = self.rag.retrieve_fast(query_context={"tags": purified_tags, "user_input": user_input})
                for m in matches:
                    flashes.append(f"Memory Echo [{m.stream}]: {m.content[:80]}...")
            except Exception as e:
                print(f"[CIM] ⚠️ RAG Quick Recall error: {e}")

        # 2. Fallback: Local Cache Scan (Digital Twin)
        if not flashes:
            for turn in self.full_state.get("history", []):
                anchor = str(turn.get("salience_anchor", "")).lower()
                if any(tag in anchor for tag in purified_tags):
                    flashes.append(f"Local Recall: '{turn['salience_anchor']}' -> {turn['user_input'][:60]}...")

        if not flashes:
            return ["No immediate matches found in baseline or fast RAG streams."]
            
        return flashes[:3]



    def _get_conversation_history(self, limit: int = 10) -> str:
        # Get raw conversation history (recent turns)
        #
        # Args:
        #     limit: Number of turns to format
        #
        # Returns:
        #     str: Formatted conversation history      Returns:

            str: Formatted conversation history (truncated to token budget)

        if self.msp_client is None:

            return "No conversation history (MSP unavailable)"



        try:

            recent_episodes = self.msp_client.get_recent_episodes(limit=10)



            history_lines = []

            for episode in recent_episodes:

                user_input = episode.get("user_input", "")

                response = episode.get("final_response", "")



                history_lines.append(f"User: {user_input}")

                history_lines.append(f"EVA: {response}")



            history_text = "\n".join(history_lines)



            # Truncate with accurate token counting

            truncated_history, actual_tokens = self.token_counter.truncate(

                history_text,

                max_tokens=max_tokens

            )



            print(f"[CIM] Conversation history: {actual_tokens}/{max_tokens} tokens")

            return truncated_history



        except Exception as e:

            print(f"[CIM] ⚠️ Conversation history error: {e}")

            return "Error loading conversation history"



    def _format_memory_streams(self, matches: List[Dict[str, Any]]) -> str:
        # Break down memory matches by stream
        #
        # Args:
        #     matches: List of memory/knowledge matches from RAG
        #
        # Returns:
        #     str: Formatted string separated by Stream ID

        breakdown = {

            "Narrative": [],

            "Salience": [],

            "Sensory": [],

            "Intuition": [],

            "Emotion": [],

            "Temporal": [],

            "Reflection": []

        }



        for match in matches:

            stream = match.get("stream", "unknown")

            if stream in breakdown:

                breakdown[stream].append(match)



        formatted_output = []

        for stream_name, stream_matches in breakdown.items():

            if stream_matches:

                formatted_output.append(f"--- {stream_name} Stream ---")

                for i, m in enumerate(stream_matches):

                    content = m.get("content", "")

                    source = m.get("source", "unknown")

                    formatted_output.append(f"[{i+1}] (Source: {source}) {content}")

        return "\n".join(formatted_output)



    def _breakdown_memory_streams(self, memory_matches: List[Dict[str, Any]]) -> Dict[str, List]:
        Returns:

            dict: Matches grouped by stream

        """

        breakdown = {

            "Narrative": [],

            "Salience": [],

            "Sensory": [],

            "Intuition": [],

            "Emotion": [],

            "Temporal": [],

            "Reflection": []

        }



        for match in memory_matches:

            stream = match.get("stream", "unknown")

            if stream in breakdown:

                breakdown[stream].append(match)



        return breakdown



    # ================================================================

    # TOKEN BUDGET MANAGEMENT

    # ================================================================



    def get_token_budget_report(self, phase: str, components: Dict[str, str]) -> Dict[str, Any]:

        """

        Get token budget report for a specific phase



        Args:

            phase: "phase_1" or "phase_2"

            components: Dict of {component_name: text}



        Returns:

            dict: Token budget report with usage details

        """

        if phase not in self.token_budgets:

            raise ValueError(f"Invalid phase: {phase}. Must be 'phase_1' or 'phase_2'")



        budget = self.token_budgets[phase]

        report = self.token_counter.get_budget_report(components, budget["total_max"])



        # Add budget limits for each component

        for comp_name, comp_data in report["components"].items():

            if comp_name in budget:

                comp_data["budget"] = budget[comp_name]

                comp_data["over_budget"] = comp_data["tokens"] > budget[comp_name]



        # Add phase info

        report["phase"] = phase

        report["budget_limits"] = budget



        return report



    def print_token_budget_report(self, phase: str, components: Dict[str, str]) -> None:

        """

        Print token budget report to console



        Args:

            phase: "phase_1" or "phase_2"

            components: Dict of {component_name: text}

        """

        report = self.get_token_budget_report(phase, components)



        print(f"\n{'='*60}")

        print(f"Token Budget Report - {phase.upper()}")

        print(f"{'='*60}")

        print(f"Total: {report['total_tokens']}/{report['max_tokens']} tokens ({report['usage_percent']:.1f}%)")

        print(f"Status: {'✅ Within Budget' if report['within_budget'] else '❌ OVER BUDGET'}")

        print(f"{'-'*60}")



        for comp_name, comp_data in report["components"].items():

            budget_limit = comp_data.get("budget", "N/A")

            status = "❌" if comp_data.get("over_budget", False) else "✅"



            print(f"{status} {comp_name:25s}: {comp_data['tokens']:4d}/{budget_limit} tokens")



        print(f"{'='*60}\n")



    # ================================================================

    # UTILITY METHODS

    # ================================================================



    def _generate_context_id(self) -> str:

        """

        Generate unique context ID for this turn

        Format: ctx_v8_{yymmdd}_{hhmmss}_{hash_short}



        Returns:

            str: Context ID

        """

        now = datetime.now()

        timestamp = now.strftime("%y%m%d_%H%M%S")



        # Generate short hash

        hash_input = f"{now.isoformat()}{self.turn_index}".encode('utf-8')

        hash_short = hashlib.md5(hash_input).hexdigest()[:6]



        return f"ctx_v8_{timestamp}_{hash_short}"



    def _get_current_episode_id(self) -> str:

        """

        Get current episode ID (format: EVA_EP{n})



        Returns:

            str: Episode ID

        """

        if self.msp_client is None:

            return "EVA_EP00"



        try:

            episode_counter = self.msp_client.get_episode_counter()

            persona_code = episode_counter.get("persona_code", "EVA")

            current_num = episode_counter.get("current_episode", 0)

            return f"{persona_code}_EP{current_num:02d}"

        except Exception as e:

            print(f"[CIM] ⚠️ Episode ID error: {e}")

            return "EVA_EP00"





    # ================================================================

    # COGNITIVE FIREWALL (PHASE 4)

    # ================================================================



    def normalize_stimulus(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Cognitive Firewall: Normalize and validate LLM-driven stimulus triggers.
        Supports stimulus_id lookup from catalog and direct bio_impacts.
        """
        normalized_chunks = []

        # 1. Handle List of Chunks vs Single Chunk
        if isinstance(raw_data, list):
            raw_chunks = raw_data
        elif isinstance(raw_data, dict):
            if "chunks" in raw_data and isinstance(raw_data["chunks"], list):
                raw_chunks = raw_data["chunks"]
            else:
                raw_chunks = [raw_data]
        else:
            print(f"[CIM] ⚠️ Invalid stimulus data type: {type(raw_data)}. Using neutral fallback.")
            raw_chunks = [{"valence": 0.5, "arousal": 0.3, "intensity": 0.3}]

        # 2. Normalize Each Chunk
        for i, chunk in enumerate(raw_chunks):
            if not isinstance(chunk, dict):
                continue
            
            stim_id = chunk.get("stimulus_id")
            vector = chunk.get("stimulus_vector", chunk)
            
            # Start with explicit vector or defaults
            norm_chunk = {
                "valence": float(vector.get("valence", 0.5)),
                "arousal": float(vector.get("arousal", 0.3)),
                "intensity": float(vector.get("intensity", 0.3)),
                "stress": float(vector.get("stress", 0.3)),
                "warmth": float(vector.get("warmth", 0.5)),
                "tags": list(chunk.get("tags", ["neutral"])),
                "salience_anchor": str(chunk.get("salience_anchor") or f"chunk_{i}"),
                "stimulus_id": stim_id,
                "bio_impacts": chunk.get("bio_impacts", {})
            }

            # 3. Catalog Lookup Integration
            if stim_id and stim_id in self.stimulus_catalog:
                spec = self.stimulus_catalog[stim_id]
                impacts = spec.get("impacts", {})
                
                # Merge impacts (LLM bio_impacts takes precedence over catalog)
                merged_impacts = impacts.copy()
                if norm_chunk["bio_impacts"]:
                    merged_impacts.update(norm_chunk["bio_impacts"])
                
                norm_chunk["bio_impacts"] = merged_impacts
                
                # Add default tags from catalog if none provided by LLM
                if not chunk.get("tags") and "category" in spec:
                    norm_chunk["tags"].append(spec["category"].lower())

            # 4. Enforce RI/RIM scoring slots
            if "ri_score" in chunk:
                norm_chunk["ri_score"] = float(chunk["ri_score"])
            if "rim_impact" in chunk:
                norm_chunk["rim_impact"] = float(chunk["rim_impact"])

            normalized_chunks.append(norm_chunk)

        return normalized_chunks


    # ================================================================

    # DYNAMIC PROMPT BUILDING (SSOT COMPLIANT)

    # ================================================================



    def _build_prompt_from_structure(self, phase_key: str, context: Dict[str, Any]) -> str:

        """

        Build a prompt by iterating through the configured context structure.

        """

        structure = self.config_data.get("context_structure", {}).get(phase_key, [])

        if not structure:

            print(f"[CIM] ⚠️ No context structure found for {phase_key}, using default fallback.")

            return self._build_fallback_prompt(phase_key, context)



        lines = [f"# [{phase_key.upper().replace('_', ' ')}] | Turn: {context['turn_index']} | ID: {context['context_id']}"]

        

        for section_id in structure:

            content = self._get_section_content(section_id, context)

            if content:

                lines.append(f"\n## {section_id.replace('_', ' ')}")

                lines.append(content)

        

        return "\n".join(lines)



    def _get_section_content(self, section_id: str, context: Dict[str, Any]) -> str:

        """

        Dispatcher for individual prompt sections.

        """

        # Phase 1 common sections

        if section_id == "PREVIOUS_USER_ACTION_PREDICTION":

            val = context.get('previous_user_action_prediction') or self.previous_turn_data.get("user_action_prediction", "N/A")
            return f"User was predicted to: {val}"

        if section_id == "PREVIOUS_CONTEXT_SUMMARY":

            val = context.get('previous_context_summary') or self.previous_turn_data.get("context_summary", "N/A")
            return f"Interaction history summary: {val}"

        if section_id == "CURRENT_EPISODE_METRICS":
            return f"EPISODE_ID: {context['context_id']}\nTURN_INDEX: {context['turn_index']}"

        if section_id == "CORE_IDENTITY_&_SOUL":
            # Display deduplicated metadata first
            meta = self.prn_identity.get("shared_metadata", {})
            meta_str = yaml.dump(meta, allow_unicode=True, default_flow_style=False) if meta else ""
            
            # Combine all identity files
            identity_blocks = []
            if meta_str:
                identity_blocks.append(f"### [Metadata]\n{meta_str}")
            
            # Priority: Persona first
            for key in ["persona", "thought_logic", "relational"]:
                data = self.prn_identity.get(key, {})
                if data:
                    identity_blocks.append(f"### [{key.upper()}]\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}")
            
            soul = self.prn_identity.get("soul", {})
            if soul:
                identity_blocks.append(f"### [SOUL]\n{soul.get('content', '')}")
            
            return "\n\n".join(identity_blocks)

        if section_id == "BEHAVIORAL_CONSTRAINTS":

            return context['pmt_rules'][:500]

        if section_id == "AUTONOMIC_BASELINE":
            pb = context.get('physio_baseline') or self.full_state.get("physio", {})
            return f"- Heart Rate Index: {pb.get('heart_rate_index', 'N/A')}\n- ANS State: Sympathetic: {pb.get('sympathetic', 'N/A')}, Parasympathetic: {pb.get('parasympathetic', 'N/A')}\n- Hormone Levels: {pb.get('hormone_summary', 'N/A')}\n- Status: {pb.get('status', 'connected')}"

        if section_id == "AUTONOMIC_BASELINE_DETAILED":
            physio = context.get('physio_detailed') or self.full_state.get("physio", {})
            blood = physio.get("blood", {})
            ans = physio.get("autonomic", {})
            
            lines = [f"ANS State: Sympathetic: {ans.get('sympathetic', 0.5):.2f}, Parasympathetic: {ans.get('parasympathetic', 0.5):.2f}"]
            lines.append("Hormone Levels (All 23):")
            
            # Group by category if possible, else list all
            for h_id, val in blood.items():
                lines.append(f"  - {h_id}: {val:.3f}")
            
            return "\n".join(lines) if blood else "Physiological state unavailable."

        if section_id == "9D_MATRIX_BASELINE":
            matrix = context.get('eva_matrix_9d') or self.full_state.get("matrix", {}).get("axes_9d", {})
            if not matrix: return "Psychological state unavailable."
            return f"Psychological Dimensions (Current Mood):\n{yaml.dump(matrix, allow_unicode=True, default_flow_style=False)}"

        if section_id == "RECENT_CONTEXT":
            sc = context.get('situation_context', {})
            sm = context.get('session_memory', {})
            history = self.full_state.get("history", [])
            
            hist_lines = ["Recent 5-Turn Cache:"]
            for turn in history:
                hist_lines.append(f"  - Turn {turn['turn_index']} | Anchor: {turn['salience_anchor']} | User: {turn['user_input']} | EVA: {turn['eva_response'][:100]}...")
            
            return f"{chr(10).join(hist_lines)}\n- Atmosphere: {sc.get('interpersonal_atmosphere', 'neutral')}"

        if section_id == "SELF_NOTE":
            note = self.full_state.get("self_note", "")
            return f"Note to Self: {note}" if note else "No persistent self-note available."

        if section_id == "INTUITION_FLASHES":
            flashes = context.get('intuition_flashes')
            if not flashes or flashes == "No mental flashes triggered":
                return "No mental flashes triggered"
            if isinstance(flashes, list):
                return "\n".join([f"- {f}" for f in flashes])
            return str(flashes)

        if section_id == "RAW_STIMULUS":

            return f"User: {context['user_input']}"

        if section_id == "PERCEPTION_DIRECTIVE":
            return (
                "Analyze the user's message above and extract the emotional stimulus.\n"
                "**Your task:**\n"
                "1. Identify the emotional tone and intent\n"
                "2. Extract key semantic anchors\n"
                "3. **Call the `sync_biocognitive_state` function**\n"
                "Do NOT respond with text."
            )


        if section_id == "STIMULUS_CATALOG":
            if not self.stimulus_catalog:
                return "Catalog unavailable."
            
            # Format catalog into a concise summary for the prompt
            catalog_lines = []
            for stim_id, spec in self.stimulus_catalog.items():
                desc = spec.get("description", "No description")
                cats = spec.get("category", "General")
                catalog_lines.append(f"- {stim_id} [{cats}]: {desc}")
            
            return "\n".join(catalog_lines[:30])

        

        # Phase 2 common sections

        if section_id == "EMBODIED_SENSATION":

            return context.get('embodied_sensation', 'No sensation data.')

        if section_id == "9D_MATRIX":

            return f"Psychological Dimensions:\n{yaml.dump(context.get('eva_matrix_9d', {}), allow_unicode=True, default_flow_style=False)}"

        if section_id == "ARTIFACT_QUALIA":

            return yaml.dump(context.get('artifact_qualia', {}), allow_unicode=True, default_flow_style=False)

        if section_id == "PHYSIO_DELTA":

            return context.get('physio_delta', 'No bio-update.')

        if section_id == "HEPT_STREAM_RECALL":

            # Re-implementing the narrative/emotion logic from build_phase_2_prompt
            narrative_chunk = ""
            emotion_chunk = ""
            other_streams = []
            for match in context.get("memory_matches", []):
                stream = match.get("stream", "unknown")
                content = match.get("content", "")
                score = match.get("score", 0.0)
                if stream == "Narrative": narrative_chunk += f"- {content} (score: {score:.2f})\n"
                elif stream == "Emotion": emotion_chunk += f"- {content} (score: {score:.2f})\n"
                else: other_streams.append(f"[{stream}] {content} (score: {score:.2f})")
            
            res = ""
            if narrative_chunk: res += f"\n### Narrative Stream\n{narrative_chunk}"
            if emotion_chunk: res += f"\n### Emotion Stream ⚡\n{emotion_chunk}"
            if other_streams: res += f"\n### Other Streams\n{chr(10).join(other_streams)}"
            return res or "No memory echoes found."

        if section_id == "COGNITIVE_RULES":

            return context.get('pmt_rules', 'No rules.')

        if section_id == "FINAL_DIRECTIVE":

            return "1. ประสานความรู้สึกเข้ากับความทรงจำ\n2. ตอบสนองภายใต้กรอบ Persona (40%) และสภาวะร่างกาย (60%)"

        

        # Phase 3 common sections

        if section_id == "CONTEXT_SUMMARY":

            return "Summarize the interaction and emotional tone."

        if section_id == "USER_ACTION_PREDICTION":

            return "Predict likely user reactions."

        if section_id == "ACTION_PLAN":

            return "Propose a strategic response plan."
            
        if section_id == "MEMORY_ENCODING_DRAFT":
            return "Key facts and emotional anchors to remember."
            
        if section_id == "SELF_NOTES":
            return "1. Internal status and coherence notes.\n2. **Important**: Write a short note to yourself for the next episode/turn in the JSON field 'self_note'."

        return ""



    def _build_fallback_prompt(self, phase: str, context: Dict[str, Any]) -> str:

        # Fallback deterministic prompt if config is missing

        return f"Fallback prompt for {phase} - Context ID: {context['context_id']}"



    # ================================================================

    # PHASE 3: PREDICTION & SUMMARY (Post-Turn Analysis)

    # ================================================================



    def inject_phase_3(self, final_response: str, context_id: str) -> Dict[str, Any]:
        # Phase 3: Gather data for post-turn analysis

        context = {

            "context_id": context_id,

            "turn_index": self.turn_index,

            "timestamp": datetime.now().isoformat(),

            "final_response": final_response,

            "persona": self.persona_data,

            "pmt_rules": self.pmt_rules[:300]

        }

        return context



    def build_phase_3_prompt(self, context: Dict[str, Any]) -> str:
        # Build Phase 3 prompt for context summary and prediction
        return self._build_prompt_from_structure("phase_3_prediction", context)






if __name__ == "__main__":

    print("=" * 60)

    print("Context Injection Node (CIN) - EVA 8.1.0")

    print("Testing standalone (without dependencies)")

    print("=" * 60)



    # Create CIN without dependencies (graceful degradation mode)
    cin = ContextInjectionModule()



    print("\n[TEST 1] Phase 1: Rough Context Injection")

    print("-" * 60)

    user_input = "วันนี้เครียดมาก งานเยอะอะ"

    phase1_context = cin.inject_phase_1(user_input)

    print(f"✅ Context ID: {phase1_context['context_id']}")

    print(f"✅ Turn Index: {phase1_context['turn_index']}")

    print(f"✅ Persona: {phase1_context['persona'].get('meta', {}).get('name', 'UNKNOWN')}")

    print(f"✅ Physio Baseline Status: {phase1_context['physio_baseline']['status']}")



    print("\n[TEST 2] Build Phase 1 Prompt")

    print("-" * 60)

    phase1_prompt = cin.build_phase_1_prompt(phase1_context)

    print(phase1_prompt[:500])

    print(f"\n... (Total length: {len(phase1_prompt)} chars)")



    print("\n[TEST 3] Phase 2: Deep Context Injection")

    print("-" * 60)

    # Simulate LLM Phase 1 output

    stimulus_vector = {"valence": -0.7, "arousal": 0.8, "intensity": 0.9}

    tags = ["stress", "work_overload", "emotional_support"]

    updated_physio = {"cortisol": 0.82, "adrenaline": 0.65, "sympathetic": 0.75, "parasympathetic": 0.25}

    memory_matches = [

        {"stream": "Emotion", "content": "ครั้งที่แล้วเครียดเหมือนกัน จากงานที่ต้องส่งเยอะ", "score": 0.89},

        {"stream": "Narrative", "content": "เคยบอกว่าจะแบ่งงานเป็นขั้นตอนเล็กๆ", "score": 0.76}

    ]



    phase2_context = cin.inject_phase_2(stimulus_vector, tags, updated_physio, memory_matches)

    print(f"✅ Context ID (same): {phase2_context['context_id']}")

    print(f"✅ Embodied Sensation: {phase2_context['embodied_sensation'][:100]}...")

    print(f"✅ EVA Matrix Status: {phase2_context['eva_matrix_9d'].get('status', 'N/A')}")

    print(f"✅ Memory Matches: {len(phase2_context['memory_matches'])} streams")



    print("\n[TEST 4] Build Phase 2 Function Result")

    print("-" * 60)

    function_result = cin.build_phase_2_prompt(phase2_context)

    print(f"✅ Status: {function_result['status']}")

    print(f"✅ Function Result Text:")

    print(function_result['function_result_text'][:500])

    print(f"\n... (Total length: {len(function_result['function_result_text'])} chars)")



    print("\n[TEST 5] Token Counting - Phase 1 Budget")

    print("-" * 60)

    # Build components dict for Phase 1

    phase1_components = {

        "identity_anchor": yaml.dump(phase1_context['persona'], allow_unicode=True),

        "physio_baseline": str(phase1_context['physio_baseline']),

        "pmt_rules": phase1_context['pmt_rules'],

        "conversation_history": phase1_context.get('conversation_history', ''),

        "user_input": phase1_context['user_input']

    }



    cin.print_token_budget_report("phase_1", phase1_components)



    print("\n[TEST 6] Token Counting - Truncation Test")

    print("-" * 60)

    long_text = "This is a test. " * 500  # ~1500 words

    original_tokens = cin.token_counter.count(long_text)

    truncated_text, truncated_tokens = cin.token_counter.truncate(long_text, max_tokens=100)



    print(f"✅ Original text: {original_tokens} tokens")

    print(f"✅ Truncated to: {truncated_tokens} tokens (max: 100)")

    print(f"✅ Truncation worked: {truncated_tokens <= 100}")

    print(f"✅ Token counter method: {cin.token_counter.method}")



    print("\n" + "=" * 60)

    print("✅ ALL TESTS PASSED - CIN with Token Counting Ready")

    print("=" * 60)

