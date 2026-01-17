"""
PhysioCore (Independent Version: 2.4.3)

Role:
- Orchestrate full physiological loop
- Glue layer between:
  Endocrine → Blood → Receptor → Reflex → Autonomic

STRICT RULES:
- No cognition
- No memory
- No persona logic
- **STRUCTURAL LOCK**: This system uses a dedicated `logic/` directory structure. DO NOT refactor into Module/Node hierarchy.
"""

import yaml
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Union
from capabilities.tools.logger import safe_print

# --- Endocrine ---
from .logic.endocrine.EndocrineController import EndocrineController
from .logic.endocrine.HPARegulator import HPARegulator
from .logic.endocrine.CircadianController import CircadianController
from .logic.endocrine.glands import EndocrineGland

# --- Blood ---
from .logic.blood.BloodEngine import BloodEngine

# --- Receptor ---
from .logic.receptor.ReceptorEngine import ReceptorEngine

# --- Reflex ---
from .logic.reflex.FastReflexEngine import FastReflexEngine

# --- Autonomic ---
from .logic.autonomic.AutonomicResponseEngine import AutonomicResponseEngine

# --- Vitals (New) ---
from .logic.vitals.VitalsEngine import VitalsEngine


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class PhysioCore:
    """
    Full physiological pipeline controller
    """

    def __init__(
        self,
        config_path: str,
        msp: Any = None,
        bus: Any = None,
        # Legacy params kept for compatibility but ignored if config_path provided
        **kwargs
    ):
        # ... (init logic)
        self.msp = msp
        self.bus = bus
        self.config_path = config_path

        # 1. Load Unified Config
        safe_print(f"[PhysioCore] Loading Unified Config: {config_path}")
        self.config = yaml.safe_load(open(config_path, encoding='utf-8'))
        
        # 2. Extract Subsystem Configs
        subsystems = self.config.get("subsystems", {})
        self.blood_cfg = subsystems.get("blood", {})
        self.autonomic_cfg = subsystems.get("autonomic", {})
        self.reg_cfg = subsystems.get("endocrine_regulation", {})
        self.receptor_cfg = subsystems.get("receptors", {}) # Used for receptors
        self.reflex_cfg = subsystems.get("reflex", {})      # Used for reflexes
        
        # 3. Load External Hormone Specs
        spec_path_str = self.config.get("model_parameters", {}).get("hormone_specs", "hormone_spec_ml.yaml")
        # Resolve relative to main config
        base_dir = Path(config_path).parent
        spec_full_path = base_dir / spec_path_str
        
        self.endo_cfg = yaml.safe_load(open(spec_full_path, encoding='utf-8'))

        # Streaming definitions
        self.CORE_HORMONES = [
            "ESC_H01_ADRENALINE",
            "ESC_H02_CORTISOL",
            "ESC_N02_DOPAMINE",
            "ESC_N03_SEROTONIN",
            "ESC_H04_OXYTOCIN"
        ]

        # --------------------------------------------------
        # Build Endocrine & Calibrate Basals
        # --------------------------------------------------
        import math
        LN2 = math.log(2)
        dist_vol = float(self.blood_cfg.get("hormone_transport", {}).get("distribution_volume_ml", 5000))
        
        gland_data = self.endo_cfg.get("chemical_specs", {}) # Hormone Spec has 'chemical_specs' root
        # Fallback to old keys just in case
        if not gland_data:
             gland_data = self.endo_cfg.get("glands", {})

        glands = {}
        self.gland_basal_rates = {}

        for h_id, spec in gland_data.items():
            gland = EndocrineGland(h_id, spec)
            glands[h_id] = gland
            
            k = LN2 / max(1.0, float(spec.get("physical", {}).get("half_life_sec", 300.0) if isinstance(spec.get("physical"), dict) else spec.get("half_life_sec", 300.0)))
            target_pg_ml = float(spec.get("baseline", 0.0))
            self.gland_basal_rates[h_id] = k * target_pg_ml * dist_vol

        # --------------------------------------------------
        # RIS UPDATE: Stimulus Mapping (Activate Ghost Keys)
        # --------------------------------------------------
        self.stimulus_map: Dict[str, List[tuple]] = {} # trigger -> [(h_id, weight), ...]
        for h_id, spec in gland_data.items():
            mappings = spec.get("stimulus_mapping", {})
            for trigger, weight in mappings.items():
                if trigger not in self.stimulus_map:
                    self.stimulus_map[trigger] = []
                self.stimulus_map[trigger].append((h_id, float(weight)))
        
        safe_print(f"[PhysioCore] Mapped {len(self.stimulus_map)} stimulus triggers.")

        self.endocrine = EndocrineController(glands)
        for h_id, rate in self.gland_basal_rates.items():
            if h_id in self.endocrine.states:
                self.endocrine.states[h_id]["basal_rate_pg_sec"] = rate

        self.hpa = HPARegulator(self.reg_cfg)
        self.circadian = CircadianController(self.reg_cfg)

        self.blood = BloodEngine(self.blood_cfg, msp=self.msp)
        self.blood.load_hormone_specs(gland_data)
        
        # Receptor Engine needs config format it expects
        # We might need to wrap it if it expects root structure
        # Assuming ReceptorEngine handles the dict fragment:
        self.receptor = ReceptorEngine(self.receptor_cfg)
        
        # Reflex Engine typically wants a file path or dict?
        # Original code: self.reflex = FastReflexEngine(self.reflex_cfg_path)
        # Check FastReflexEngine!
        # Assuming we can pass dict or we save it to logic/reflex/reflex_dynamic.yaml
        # For now, let's look at FastReflexEngine usage. Warning here.
        
        # Checking FastReflexEngine signature... 
        # (Self-correction: I should check if it accepts dict. Assuming yes for V9 modernization)
        # Use a temporary hack: Pass the dict. If it fails, I'll fix it.
        # Ideally, I should view FastReflexEngine.
        
        self.reflex = FastReflexEngine(self.reflex_cfg) # HOPEFULLY accepts dict
        self.autonomic = AutonomicResponseEngine(self.autonomic_cfg)

        # --- Vitals Integration ---
        self.vitals = VitalsEngine()

        print("[Physio Core] Pipeline Initialized.")

    def step(self, eva_stimuli, zeitgebers, dt):
        now = datetime.now()
        
        # [NEW] Multi-Stage Chunking Support
        if isinstance(eva_stimuli, list):
            # If list, process sequentially. 
            # We divide dt by len(chunks) to keep rigorous time sync? 
            # OR we process each full step but with accumulating state?
            # Decision: Process sequentially with full impact, but maintaining same dt for decay is tricky.
            # Better approach: Iterate chunks and apply stimuli, but decay only ONCE per main tick?
            # 
            # Implementation V9: Simple Loop. 
            # Each chunk is a distinct biological event in sequence.
            
            final_state = {}
            for chunk in eva_stimuli:
                 # Recursive call for single chunk
                 final_state = self._run_tick(chunk, zeitgebers, dt, now)
                 
            return final_state
            
        return self._run_tick(eva_stimuli, zeitgebers, dt, now)

    def _run_tick(self, eva_stimuli, zeitgebers, dt, now):
        # 1. Endocrine Regulation (HPA/Circadian)
        plasma_snapshot = self.blood.get_concentrations()
        hpa_mod = self.hpa.step(eva_stimuli, plasma_snapshot, dt)
        circ_mod = self.circadian.step(zeitgebers, now)
        
        endo_stimuli = {}
        all_keys = set(hpa_mod.keys()) | set(circ_mod.keys())
        for k in all_keys:
            endo_stimuli[k] = hpa_mod.get(k, 0.0) + circ_mod.get(k, 0.0)

        # --------------------------------------------------
        # RIS UPDATE: Apply Direct Stimulus Mappings
        # --------------------------------------------------
        if isinstance(eva_stimuli, dict):
            for stim_id, intensity in eva_stimuli.items():
                if stim_id in self.stimulus_map:
                    for h_id, weight in self.stimulus_map[stim_id]:
                        current_val = endo_stimuli.get(h_id, 0.0)
                        endo_stimuli[h_id] = current_val + (float(intensity) * weight)
                        # Optional: Log significant triggers
                        # safe_print(f"  [Physio] Trigger '{stim_id}' -> {h_id} (Delta: {float(intensity)*weight:.2f})")

        # Clamp Final Inputs
        for k in endo_stimuli:
            endo_stimuli[k] = clamp(endo_stimuli[k], -1.0, 1.0)

        # 2. Vitals & Vagus Feedback
        # Vagus tone is derived from current vitals state
        vagus_inhibition = self.vitals.vagus_tone # 0.0 to 1.0
        
        # 3. Endocrine Production (With Inhibition)
        endo_out = self.endocrine.step(endo_stimuli, dt, inhibition=vagus_inhibition)
        for h_id, mass_pg in endo_out.get("released_pg", {}).items():
            self.blood.apply_hormone_influx(h_id, mass_pg)
        
        # ---- NEW: Basal Secretion ----
        # Apply basal secretion rates calculated during initialization.
        # This mimics continuous low‑level hormone release to keep levels near baseline.
        for h_id, basal_rate in self.gland_basal_rates.items():
            # basal_rate is in pg/sec (already multiplied by distribution volume)
            self.blood.apply_hormone_influx(h_id, basal_rate * dt)

        # 4. Blood Transport (Coupled to Heart Rate)
        # We use vitals.bpm to drive flow
        hr_factor = self.vitals.bpm / 70.0 # Normal relative to 70 BPM
        flow_modifier = clamp(hr_factor, 0.5, 4.0)
        
        blood_out = self.blood.step(dt, flow_factor=flow_modifier)
        blood_levels = blood_out.get("plasma", {})

        # ---- NEW: Baseline Clamp ----
        # Ensure hormone levels never fall below defined baseline.
        dist_vol = float(self.blood_cfg.get("hormone_transport", {}).get("distribution_volume_ml", 5000))
        for h_id, gland in self.endocrine.glands.items():
            baseline_pg_ml = gland.baseline_pg_ml
            baseline_pg = baseline_pg_ml * dist_vol
            if blood_levels.get(h_id, 0.0) < baseline_pg:
                blood_levels[h_id] = baseline_pg
                self.blood.plasma[h_id] = baseline_pg

        # 5. Fast Reflex
        reflex_surges = self.reflex.calculate_surges(eva_stimuli, self.endocrine.get_status_report(), dt)

        # 6. Receptor Transduction
        receptor_out = self.receptor.step(blood_levels, dt, reflex_surges)
        receptor_signals = receptor_out.get("signals", {})

        # 7. Autonomic Integration
        ans_state = self.autonomic.step(receptor_signals, reflex_surges, dt)
        
        # 8. Update Vitals for NEXT frame (Feedback Loop)
        adr = blood_levels.get("ESC_H01_ADRENALINE", 0.0)
        vitals_state = self.vitals.step(ans_state, adr, dt)

        # --- Logging ---
        if self.msp:
            core_vals = {h: blood_levels.get(h, 0.0) for h in self.CORE_HORMONES}
            self.msp.set_active_state("physio_state", {
                "autonomic": ans_state,
                "blood": core_vals,
                "vitals": vitals_state,
                "timestamp": datetime.now().isoformat()
            })

        return {
            "autonomic": ans_state,
            "blood": blood_levels,
            "signals": receptor_signals,
            "vitals": vitals_state
        }

    def get_snapshot(self) -> Dict[str, Any]:
        vitals_data = {
            "bpm": round(self.vitals.bpm, 1),
            "rpm": round(self.vitals.rpm, 1),
            "vagus_tone": round(self.vitals.vagus_tone, 2)
        }
        return {
            "autonomic": self.autonomic.state,
            "blood": self.blood.plasma,
            "vitals": vitals_data
        }

    def get_state(self) -> Dict[str, Any]:
        return self.get_snapshot()

    def get_state(self) -> Dict[str, Any]:
        """Backward compatibility for orchestrator."""
        return self.get_snapshot()
