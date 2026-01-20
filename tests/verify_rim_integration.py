
import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from operation_system.resonance_engine.resonance_engine import ResonanceEngine, ResonanceOutput

def test_rim_integration():
    print("Testing RIM Integration in ResonanceEngine...")
    
    # Initialize Engine
    engine = ResonanceEngine()
    
    # Simulate SLM Input (Trend: Rising)
    # Turn 1
    slm_1 = {"emotional_signal": "affection", "salience_anchor": "love you"}
    res_1 = engine.process("I love you", context={}, slm_data=slm_1)
    print(f"Turn 1: Score={res_1.ri_score}, Trend={res_1.mrf_interpretation.get('rim_trend') if res_1.mrf_interpretation else 'N/A'}")
    
    # Update History manual simulation (since context is stateless in simple test)
    history = [res_1.ri_score]
    
    # Turn 2
    slm_2 = {"emotional_signal": "affection", "salience_anchor": "really love you"}
    res_2 = engine.process("I really love you", context={"rim_history": history}, slm_data=slm_2)
    print(f"Turn 2: Score={res_2.ri_score}, Trend={res_2.mrf_interpretation.get('rim_trend') if res_2.mrf_interpretation else 'N/A'}")
    
    history.append(res_2.ri_score)
    
    # Turn 3
    slm_3 = {"emotional_signal": "affection", "salience_anchor": "really really love you"}
    res_3 = engine.process("I really really love you", context={"rim_history": history}, slm_data=slm_3)
    print(f"Turn 3: Score={res_3.ri_score}, Trend={res_3.mrf_interpretation.get('rim_trend') if res_3.mrf_interpretation else 'N/A'}")

    assert res_1.ri_score > 0, "RIM Score should be positive"
    assert res_2.ri_score > res_1.ri_score, "Score should rise with stronger anchor"
    
    print("\n✅ Verification Successful: RIM is active and integrated.")

if __name__ == "__main__":
    test_rim_integration()
