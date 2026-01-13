# ============================================================
# BloodEngine.py
# Compatible with:
# Circulation & Blood Physiology Configuration (cleaned v1.2)
# ============================================================

import time
import math
import yaml
from collections import defaultdict
from typing import Any, Dict, List

LN2 = math.log(2)

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

class BloodEngine:
    def __init__(self, config: dict, msp: Any = None):
        self.cfg = config
        self.msp = msp

        # ---------------- Runtime ----------------
        rt = self.cfg.get("runtime", {})
        self.max_dt = rt.get("max_dt_sec", 60.0)
        self.lazy_eval = rt.get("lazy_evaluation", True)

        self.last_update_ts = time.time()

        # ---------------- Blood ------------------
        blood_cfg = self.cfg.get("blood", {"total_volume_ml": 5000})
        self.total_blood_ml = float(blood_cfg["total_volume_ml"])

        # ---------------- Flow -------------------
        flow_cfg = self.cfg.get("flow", {"base_cardiac_output_ml_sec": 80.0, "safety": {"min_flow_ml_sec": 40.0, "max_flow_ml_sec": 300.0}})
        self.base_flow_ml_sec = float(flow_cfg["base_cardiac_output_ml_sec"])
        self.min_flow = flow_cfg["safety"]["min_flow_ml_sec"]
        self.max_flow = flow_cfg["safety"]["max_flow_ml_sec"]

        # ---------------- Hormone Transport ------
        ht = self.cfg.get("hormone_transport", {"distribution_volume_ml": 3000, "clearance": {"clearance_flow_coupling": False}})
        self.dist_volume_ml = ht["distribution_volume_ml"]
        self.dist_volume_ml = ht["distribution_volume_ml"]
        self.clearance_cfg = ht["clearance"]
        
        # Digestion / Uptake Delay (RIS Config Activation)
        # Note: digestion_delay_ms is usually in orchestrator_configs.yaml injection merge
        # or explicit blood_physiology.yaml if added there.
        self.digestion_delay_sec = float(self.cfg.get("digestion_delay_ms", 0.0)) / 1000.0
        self.influx_queue = [] # List of (release_time, hormone_id, mass_pg)

        # ---------------- Safety ----------------
        safety_cfg = self.cfg.get("safety", {}).get("concentration", {"min_floor": 0.0, "max_cap": 10000.0})
        self.conc_min = float(safety_cfg["min_floor"])
        self.conc_max = float(safety_cfg["max_cap"])

        # ---------------- Plasma State ----------
        self.plasma = defaultdict(float)          # hormone_id -> concentration
        self.last_decay_ts = defaultdict(lambda: time.time())

        # injected externally
        self.hormone_specs = {}

        # Dashboard streaming
        self.CORE_HORMONES = [
            "ESC_H01_ADRENALINE",
            "ESC_H02_CORTISOL",
            "ESC_H05_DOPAMINE",
            "ESC_H06_SEROTONIN",
            "ESC_H09_OXYTOCIN"
        ]

    # ========================================================
    # External Setup
    # ========================================================
    def load_hormone_specs(self, hormone_specs: dict):
        """
        hormone_specs[hormone_id] = {
            "baseline": float,
            "half_life_sec": float,
            "ranges": {"min": ..., "basal": ...}
        }
        """
        self.hormone_specs = hormone_specs
        now = time.time()

        for h_id, spec in hormone_specs.items():
            # Support explicit 'baseline' or fallback to ranges (min/basal)
            ranges = spec.get("ranges", {})
            baseline = spec.get("baseline", ranges.get("min", ranges.get("basal", 0.0)))
            
            # Handle list/morning/night ranges (use first value if dict/list)
            if isinstance(baseline, dict):
                baseline = list(baseline.values())[0] if baseline else 0.0
            elif isinstance(baseline, list):
                baseline = baseline[0] if baseline else 0.0
            
            try:
                self.plasma[h_id] = float(baseline)
            except (TypeError, ValueError):
                self.plasma[h_id] = 0.0
                
            self.last_decay_ts[h_id] = now

    # ========================================================
    # Core Update
    # ========================================================
    def step(self, dt: float, flow_factor: float = 1.0):
        """
        dt: time delta in seconds
        flow_factor: external modifier
        """
        now = time.time()
        self.last_update_ts = now

        # ---- clamp flow ----
        eff_flow = clamp(
            self.base_flow_ml_sec * flow_factor,
            self.min_flow,
            self.max_flow
        )

        # ---- passive decay ----
        for h_id in list(self.plasma.keys()):
            self._apply_decay_with_dt(h_id, now, eff_flow, dt)
            
        # ---- Process Influx Queue (Digestion) ----
        remaining_queue = []
        for release_ts, h_id, mass in self.influx_queue:
            if now >= release_ts:
                self.apply_hormone_influx(h_id, mass)
            else:
                remaining_queue.append((release_ts, h_id, mass))
        self.influx_queue = remaining_queue

        return {
            "timestamp": now,
            "effective_flow_ml_sec": eff_flow,
            "plasma": dict(self.plasma)
        }

    def update(self, flow_factor: float = 1.0):
        """Legacy / BG loop update"""
        now = time.time()
        dt = clamp(now - self.last_update_ts, 0.0, self.max_dt)
        return self.step(dt, flow_factor)

    # ========================================================
    # Hormone Influx (from organs)
    # ========================================================
    def apply_hormone_influx(self, hormone_id: str, mass_pg: float):
        """
        Inject hormone mass into blood plasma.
        """
        now = time.time()
        self._apply_decay(hormone_id, now, flow=self.base_flow_ml_sec)

        delta_conc = mass_pg / self.dist_volume_ml
        self.plasma[hormone_id] += delta_conc

        self.plasma[hormone_id] = clamp(
            self.plasma[hormone_id],
            self.conc_min,
            self.conc_max
        )

    def apply_delayed_influx(self, hormone_id: str, mass_pg: float, delay_sec: float = None):
        """
        Schedule a hormone influx after a delay (e.g. oral ingestion).
        Uses config 'digestion_delay_ms' as default base if delay_sec not provided.
        """
        if delay_sec is None:
            delay_sec = self.digestion_delay_sec
            
        release_time = time.time() + delay_sec
        self.influx_queue.append((release_time, hormone_id, mass_pg))

    # ========================================================
    # Read API
    # ========================================================
    def get_concentrations(self) -> Dict[str, float]:
        """
        Return all hormone concentrations after decay update.
        """
        now = time.time()
        for h_id in list(self.plasma.keys()):
            self._apply_decay(h_id, now, flow=self.base_flow_ml_sec)
        return dict(self.plasma)

    def read_hormone(self, hormone_id: str) -> float:
        now = time.time()
        self._apply_decay(hormone_id, now, flow=self.base_flow_ml_sec)
        return float(self.plasma.get(hormone_id, 0.0))

    # ========================================================
    # Internal: Decay / Clearance
    # ========================================================
    def _apply_decay(self, hormone_id: str, now: float, flow: float):
        last_ts = self.last_decay_ts[hormone_id]
        dt = now - last_ts
        self._apply_decay_with_dt(hormone_id, now, flow, dt)

    def _apply_decay_with_dt(self, hormone_id: str, now: float, flow: float, dt: float):
        spec = self.hormone_specs.get(hormone_id)
        if not spec:
            return
        
        if dt <= 0:
            return

        # Handle physical/half_life_sec or half_life_sec directly
        physical = spec.get("physical", {})
        if isinstance(physical, dict):
            half_life = float(physical.get("half_life_sec", 300.0))
        else:
            half_life = float(spec.get("half_life_sec", 300.0))
            
        # ---- clearance rate ----
        # Base decay constant k
        k = LN2 / max(1.0, half_life)

        # optional: flow-coupled clearance (Active Clearance)
        if self.clearance_cfg.get("clearance_flow_coupling", False):
            # As blood flow increases, clearance rate k increases
            flow_norm = clamp(flow / self.base_flow_ml_sec, 0.5, 4.0)
            k *= flow_norm

        current = self.plasma[hormone_id]

        # ---- PURE EXPONENTIAL DECAY ----
        # No more baseline target here. We decay strictly toward 0.0.
        # Homeostasis is now achieved by Basal Production in the Gland layer.
        if current > 0:
            current = current * math.exp(-k * dt)
        
        # Micro-floor for stability
        if current < self.conc_min:
            current = self.conc_min

        self.plasma[hormone_id] = clamp(
            current,
            self.conc_min,
            self.conc_max
        )
        self.last_decay_ts[hormone_id] = now
