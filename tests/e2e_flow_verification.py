"""
E2E Flow Verification: Orchestrator + Resonance Engine 9.4.3
"""

import sys
import os
from pathlib import Path

# Add root and capabilities to path
root = Path(__file__).parent.parent
sys.path.append(str(root))
sys.path.append(str(root / "capabilities"))

from orchestrator.orchestrator import EVAOrchestrator
from capabilities.tools.logger import safe_print

def test_full_orchestration_flow():
    print("="*80)
    print("🚀 STARTING E2E FLOW VERIFICATION (Resonance Edition)")
    print("="*80)

    # Initialize Orchestrator in Mock Mode (Simulated LLM)
    orch = EVAOrchestrator(mock_mode=True, enable_physio=True)
    orch.process_user_input("/start") # Initialize recording session
    
    test_inputs = [
        "Hello EVA, how are you feeling today?",  # Neutral
        "I feel so lonely, I need a friend.",       # Emotional -> APM (Caregiver/Loner)
        "This statement is false and true."        # Paradox -> MRF -> Umbrella
    ]

    for i, user_input in enumerate(test_inputs):
        print(f"\n[TURN {i+1}] USER: {user_input}")
        
        # Process through Orchestrator
        # Note: In mock mode, generate() returns a dummy response
        result = orch.process_user_input(user_input)
        
        print(f"  > RI Score: {orch.resonance.current_ri:.2f}")
        print(f"  > Layer Depth: {orch.resonance.current_depth}")
        print(f"  > Umbrella Status: {'DEPLOYED ☂️' if orch.umbrella_active else 'Normal'}")
        
        # Check Trajectory
        turn_data = orch.trajectory.current_turn
        if turn_data:
             print(f"  > Trajectory Logged: {len(turn_data.get('steps', []))} steps executed.")

    print("\n" + "="*80)
    print("✅ E2E FLOW VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    try:
        test_full_orchestration_flow()
    except Exception as e:
        print(f"❌ E2E Verification Failed: {e}")
        import traceback
        traceback.print_exc()

