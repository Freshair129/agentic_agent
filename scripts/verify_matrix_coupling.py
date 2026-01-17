
import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physio_core.physio_core import PhysioCore
from eva_matrix.eva_matrix import EVAMatrixSystem

def verify_coupling():
    print("--- [FUNCTIONAL AUDIT] Bio-Psych Coupling Check ---")

    # 1. Initialize Systems
    print("\n[STEP 1: INITIALIZATION]")
    try:
        physio = PhysioCore(config_path="physio_core/configs/PhysioCore_configs.yaml")
        matrix = EVAMatrixSystem(base_path=Path("."))
        
        initial_matrix = matrix.axes_9d.copy()
        print(f"[OK] Systems initialized.")
        print(f"Initial Stress: {initial_matrix.get('stress')}")
        print(f"Initial Stability: {initial_matrix.get('stability')}")
    except Exception as e:
        print(f"[ERR] Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # 2. Trigger Biological Event
    print("\n[STEP 2: TRIGGERING BIO-EVENT]")
    # Massive threat to overcome high Serotonin baseline
    stimuli = {"acute_threat": 20.0, "threat": 20.0}
    print(f"Applying Stimuli: {stimuli}")
    
    # Run 1 step of Physio
    # We use a larger dt to allow more diffusion/reaction
    physio_out = physio.step(eva_stimuli=stimuli, zeitgebers={}, dt=2.0)
    receptor_signals = physio_out.get("signals", {})
    
    # 3. Process in Matrix
    print("\n[STEP 3: MIGRATING TO PSYCH-DOMAIN]")
    matrix.process_signals(signals=receptor_signals)
    
    new_matrix = matrix.axes_9d
    print(f"Post-Event Stress: {new_matrix.get('stress')}")
    print(f"Post-Event Stability: {new_matrix.get('stability')}")
    print(f"Emotion Label: {matrix.emotion_label}")

    # 5. Decay Test
    print("\n[STEP 5: DECAY TEST]")
    print("Simulating 5 minutes of rest...")
    # Empty stimuli
    physio_rest = physio.step(eva_stimuli={}, zeitgebers={}, dt=300.0)
    matrix.process_signals(signals=physio_rest.get("signals", {}))
    
    decay_matrix = matrix.axes_9d
    print(f"Post-Decay Stress: {decay_matrix.get('stress')}")
    print(f"Post-Decay Stability: {decay_matrix.get('stability')}")

    if decay_matrix.get('stress') < new_matrix.get('stress'):
        print(f"[OK] Stress axis decayed.")
    else:
        print(f"[!] FAILED: Stress axis did not decay.")

    print("\n[OK] Bio-Psych Coupling Audit Complete.")

if __name__ == "__main__":
    verify_coupling()
