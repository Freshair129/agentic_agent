"""
Test Script for Resonance Engine (4-Layer Integration)
Version: 9.4.3
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from operation_system.resonance_engine.resonance_engine import ResonanceEngine, ResonanceOutput

def test_resonance_pipeline():
    print("[START] Starting Resonance Engine Verification...")
    
    engine = ResonanceEngine()
    
    # Test Case 1: Simple input
    print("\n[Test 1] Simple Input: 'I love cats and warm blankets'")
    output1 = engine.process("I love cats and warm blankets")
    print(f"RI Score: {output1.ri_score}")
    print(f"Layer Depth: {output1.layer_depth}")
    
    # Test Case 2: Paradox input (Triggering MRF -> Umbrella)
    print("\n[Test 2] Paradox Input (Simulated context)")
    context = {"paradox_detected": True}
    output2 = engine.process("This statement is false.", context=context)
    print(f"Layer Depth: {output2.layer_depth}")
    print(f"Umbrella Deployed: {output2.umbrella_deployed}")
    assert output2.umbrella_deployed is True
    
    # Test Case 3: Retracting Umbrella
    print("\n[Test 3] Retracting Umbrella")
    engine.umbrella.retract()
    assert engine.umbrella_active is False
    print("Umbrella retracted successfully.")

    print("\n[SUCCESS] All Resonance Engine tests passed!")

if __name__ == "__main__":
    try:
        test_resonance_pipeline()
    except Exception as e:
        print(f"[FAIL] Test Failed: {str(e)}")
        sys.exit(1)

