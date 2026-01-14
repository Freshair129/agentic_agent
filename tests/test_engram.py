import sys
import os
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from capabilities.services.engram_system.engram_engine import EngramEngine

def test_engram():
    print("[TEST] Testing Engram System...")
    
    # 1. Initialize
    engine = EngramEngine()
    print(f"  - Initialized (Enabled: {engine.enabled})")
    
    # 2. Test Memorization
    test_text = "Test Pattern Alpha"
    confidence = 0.99
    context = {"intent": "test", "response": "Cached Response"}
    
    print(f"  - Memorizing: '{test_text}' (Conf: {confidence})")
    success = engine.memorize(test_text, context, confidence)
    
    if success: 
        print("    [OK] Memorization successful.")
    else: 
        print("    [WARN] Memorization skipped (duplicate or low conf).")
        
    # 3. Test Lookup
    print(f"  - Looking up: '{test_text}'")
    result = engine.lookup(test_text)
    
    if result:
        print(f"    [HIT] Found: {result.get('context_data', {}).get('response')}")
    else:
        print("    [MISS] Lookup failed.")
        
    # 4. Test Miss
    print(f"  - Looking up: 'Unknown Pattern'")
    result_miss = engine.lookup("Unknown Pattern")
    if result_miss is None:
        print("    [OK] Correctly missed unknown pattern.")
    else:
        print("    [FAIL] False positive.")

if __name__ == "__main__":
    test_engram()
