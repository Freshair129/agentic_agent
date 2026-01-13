import sys
import os
from pathlib import Path
import time
from datetime import datetime

# Add root to path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

# Core imports
from operation_system.resonance_bus import ResonanceBus
from eva.memory_n_soul_passport.memory_n_soul_passport_engine import MSP
from eva.physio_core.physio_core import PhysioCore
from eva.eva_matrix.eva_matrix import EVAMatrixSystem
from eva.artifact_qualia.artifact_qualia import ArtifactQualiaSystem

def verify_resonance_loop():
    print("[ROOT VERIFICATION] Starting Resonance Loop Audit...")
    
    # 1. Infrastructure
    bus = ResonanceBus()
    bus.initialize_session("verify_session_001")
    msp = MSP() # Uses default storage path
    
    # 2. Organs
    print("  - Initializing Systems...")
    config_base = root_path / "eva/physio_core/configs"
    physio = PhysioCore(
        endocrine_cfg_path=str(config_base / "hormone_spec_ml.yaml"),
        endocrine_reg_cfg_path=str(config_base / "endocrine_regulation.yaml"),
        blood_cfg_path=str(config_base / "blood_physiology.yaml"),
        receptor_cfg_path=str(config_base / "receptor_configs.yaml"),
        reflex_cfg_path=str(config_base / "receptor_configs.yaml"),
        autonomic_cfg_path=str(config_base / "autonomic_response.yaml"),
        msp=msp,
        bus=bus
    )
    
    matrix = EVAMatrixSystem(base_path=root_path, msp=msp, bus=bus)
    qualia = ArtifactQualiaSystem(base_path=root_path, msp=msp, bus=bus)
    
    # 3. Listeners Audit
    print(f"\n[BUS AUDIT] Subscriptions:")
    for channel, subs in bus.channels.items():
        print(f"  - {channel}: {len(subs)} active listeners")
    
    # 4. Impact Simulation
    print("\n[SIMULATION] Injecting Stress Stimulus...")
    stimulus = [{"salience_anchor": "SUDDEN_LOUD_NOISE", "stress": 0.9, "intensity": 0.8, "valence": 0.2}]
    
    # Track bus events
    events_captured = []
    def monitor(payload):
        events_captured.append(payload["__metadata__"]["channel"])
    
    bus.subscribe("bus:physical", monitor)
    bus.subscribe("bus:psychological", monitor)
    bus.subscribe("bus:phenomenological", monitor)
    
    # Execute Physio Step
    physio.step(eva_stimuli=stimulus, zeitgebers={"active": 0.5}, dt=1.0)
    
    # Allow some time for bus propagation (though it's synchronous in this impl)
    print("\n[RESULT] Resonance Propagation Chain:")
    expected_chain = ["bus:physical", "bus:psychological", "bus:phenomenological"]
    
    # Verify chain
    success = True
    for channel in expected_chain:
        if channel in events_captured:
            print(f"  [OK] {channel} detected")
        else:
            print(f"  [MISSING] {channel} MISSING")
            success = False
            
    # Check states
    print(f"\n[STATE AUDIT]")
    print(f"  - Matrix Label: {matrix.emotion_label}")
    print(f"  - Qualia Tone: {qualia.last_qualia.tone if qualia.last_qualia else 'N/A'}")
    print(f"  - State Hash: {bus.generate_state_hash()}")
    
    if success:
        print("\nVERIFICATION SUCCESS: The bio-cognitive resonance loop is intact.")
    else:
        print("\nVERIFICATION FAILED: Loop interruption detected.")
    
if __name__ == "__main__":
    verify_resonance_loop()
