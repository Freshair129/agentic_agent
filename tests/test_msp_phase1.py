"""
Integration test for Phase 1 MSP logging improvements (Safe Output)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_phase1_schemas():
    """Test all Phase 1 schema files are valid"""
    import json
    from pathlib import Path

    schema_dir = Path("memory_n_soul_passport/schema")

    # Test 1: Stimulus schema exists and valid
    stimulus_schema = schema_dir / "Stimulus_Output_Schema.json"
    assert stimulus_schema.exists(), "Stimulus_Output_Schema.json not found"
    with open(stimulus_schema, encoding='utf-8') as f:
        schema = json.load(f)
    assert schema["title"] == "Stimulus_Output_Schema"
    print("[PASS] Stimulus_Output_Schema.json valid")

    # Test 2: State_Storage has vitals
    state_storage = schema_dir / "State_Storage_Schema.json"
    with open(state_storage, encoding='utf-8') as f:
        schema = json.load(f)
    assert "vitals" in schema["properties"]["physio_state"]["properties"]
    print("[PASS] State_Storage_Schema.json has vitals")

    # Test 3: State_Snapshot expanded
    state_snapshot = schema_dir / "State_Snapshot_Schema.json"
    with open(state_snapshot, encoding='utf-8') as f:
        schema = json.load(f)
    assert "resonance_texture" in schema["properties"]
    assert "trauma_flag" in schema["properties"]
    assert "depth" in schema["properties"]["qualia"]["properties"]
    print("[PASS] State_Snapshot_Schema.json expanded")

    # Test 4: Episodic Memory references stimulus
    episodic = schema_dir / "Episodic_Memory_Schema_v2.json"
    with open(episodic, encoding='utf-8') as f:
        schema = json.load(f)
    
    # Check definition of turn_llm
    turn_llm_props = schema["definitions"]["turn_llm"]["properties"]
    assert "stimulus_output" in turn_llm_props
    print("[PASS] Episodic_Memory_Schema_v2.json references stimulus")

def test_msp_method():
    """Test MSP has new method"""
    from memory_n_soul_passport.memory_n_soul_passport_engine import MSP

    assert hasattr(MSP, 'log_stimulus_output'), "MSP missing log_stimulus_output method"
    print("[PASS] MSP.log_stimulus_output() exists")

def test_orchestrator_hooks():
    """Test Orchestrator imports and syntax"""
    try:
        from orchestrator.orchestrator import EVAOrchestrator
        print("[PASS] Orchestrator imports successfully")
    except SyntaxError as e:
        print(f"[FAIL] Orchestrator syntax error: {e}")
        raise
    except ImportError as e:
        print(f"[FAIL] Orchestrator import error: {e}")
        raise

if __name__ == "__main__":
    print("\n=== Phase 1 Integration Test ===\n")

    try:
        test_phase1_schemas()
        test_msp_method()
        test_orchestrator_hooks()
        print("\n[ALL PASS] All Phase 1 tests passed!")
    except AssertionError as e:
        print(f"\n[FAIL] Assertion Failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        sys.exit(1)
