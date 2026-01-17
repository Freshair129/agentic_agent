import time
import sys
import os
from pathlib import Path

# Add root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from physio_core.physio_core import PhysioCore

def verify_physio():
    print("--- [FUNCTIONAL AUDIT] PhysioCore Integrity Check ---")
    
    # 1. Initialization
    config_path = "physio_core/configs/PhysioCore_configs.yaml"
    physio = PhysioCore(config_path=config_path)
    state = physio.get_state()
    print(f"[OK] PhysioCore initialized. Initial BPM: {state.get('vitals', {}).get('bpm')}")

    # 2. Endocrine Response Test (Spike & Decay)
    
    # Check Baselines
    h_adrenaline = "ESC_H01_ADRENALINE"
    blood_levels = state.get('blood', {})
    baseline_adr = blood_levels.get(h_adrenaline, 0.0)
    print(f"Baseline Adrenaline: {baseline_adr:.2f} pg/mL")

    # Apply Stimulus: Acute Threat + Reflex 'threat'
    print("Applying Stimuli: {'acute_threat': 1.0, 'threat': 1.0}")
    physio.step(eva_stimuli={"acute_threat": 1.0, "threat": 1.0}, zeitgebers={}, dt=1.0) # 1 second step
    
    spike_state = physio.get_state()
    spike_adr = spike_state.get('blood', {}).get(h_adrenaline, 0.0)
    print(f"Spiked Adrenaline: {spike_adr:.2f} pg/mL")
    
    if spike_adr > baseline_adr:
        print(f"[OK] Hormone spike detected: {baseline_adr:.2f} -> {spike_adr:.2f}")
    else:
        print(f"[!] FAILED: No hormone spike detected. Check mapping.")

    # 3. Autonomic Feedback (BPM Sync)
    print("\n[STEP 3: AUTONOMIC FEEDBACK]")
    baseline_bpm = 70.0 # Standard start
    current_bpm = spike_state.get('vitals', {}).get('bpm', 70)
    print(f"BPM: {baseline_bpm} (Baseline) -> {current_bpm:.1f} (Post-Spike)")
    
    if current_bpm > baseline_bpm:
        print(f"[OK] Vitals responded with a spike.")
    else:
        print(f"[!] FAILED: BPM did not increase after threat reflex.")

    # 4. Long Decay Test
    print("\n[STEP 4: DECAY TEST]")
    physio.step(eva_stimuli={}, zeitgebers={}, dt=300.0) # 5 minutes
    decay_state = physio.get_state()
    decay_adr = decay_state.get('blood', {}).get(h_adrenaline, 0.0)
    print(f"Adrenaline after 5min decay: {decay_adr:.2f} pg/mL")
    
    if decay_adr < spike_adr:
        print(f"[OK] Hormone decay function verified.")
    else:
        print(f"[!] FAILED: Adrenaline did not decay.")

if __name__ == "__main__":
    verify_physio()
