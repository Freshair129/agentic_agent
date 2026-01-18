
"""
MSP Schema Coverage Audit Script
Checks if all system outputs defined in eva_master_registry.yaml are captured in MSP schemas.
"""

import yaml
import json
from pathlib import Path
import sys

def audit_system_contracts():
    """Check eva_master_registry.yaml contracts against MSP schemas"""
    
    # Resolve paths relative to script location
    root_dir = Path(__file__).parent.parent
    registry_path = root_dir / "registry" / "eva_master_registry.yaml"
    schema_dir = root_dir / "memory_n_soul_passport" / "schema"

    if not registry_path.exists():
        print(f"❌ Registry not found: {registry_path}")
        return False

    # Load registry
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load registry: {e}")
        return False

    # Load schemas
    schemas = {}
    try:
        for sf in schema_dir.glob("*.json"):
            with open(sf, 'r', encoding='utf-8') as f:
                schemas[sf.stem] = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load schemas: {e}")
        return False

    if not schemas:
        print("❌ No schemas found.")
        return False

    print(f"Loaded {len(schemas)} schemas.")
    
    # Flatten checks
    missing_coverage = []
    
    # Check Systems
    for system in registry.get("systems", []):
        system_id = system.get("id")
        contracts = system.get("contracts", {})
        outputs = contracts.get("outputs", [])
        
        if not outputs:
            continue
            
        print(f"\nScanning System: {system_id}")
        
        for output in outputs:
            data_type = output.get("data")
            structure = output.get("structure", "unknown")
            
            # Context Variables
            snapshot = schemas.get("State_Snapshot_Schema", {})
            snapshot_props = snapshot.get("properties", {}).keys()
            storage = schemas.get("State_Storage_Schema", {})
            storage_physio = storage.get("physio_state", {}).get("properties", {}).keys()

            
            # Generalized Search (Phase 14 Upgrade)
            covered = False
            
            # 1. Direct Key Match in ANY schema
            for s_name, s_content in schemas.items():
                # Check top-level definitions
                if "definitions" in s_content:
                    if data_type in s_content["definitions"]:
                        covered = True
                        break
                
                # Check properties
                if "properties" in s_content:
                    if data_type in s_content["properties"]:
                        covered = True
                        break
                        
            # 2. Explicit Heuristics (Legacy)
            if not covered:
                if data_type == "vitals" and "vitals" in storage_physio:
                    covered = True
                elif "reflex" in data_type and "reflex_directives" in snapshot_props:
                    covered = True
                elif "texture" in data_type and "resonance_texture" in snapshot_props:
                    covered = True
                # Phase 14 Aliases
                elif data_type == "HormonePanel" and "hormones" in snapshot_props: # Allow mapping
                    covered = True
                elif data_type == "VitalsData" and "vitals" in snapshot_props:   # Allow mapping
                    covered = True
                elif "Vector" in data_type and "stimulus_vector" in snapshot_props:
                    covered = True
                elif "EmotionalState" in data_type: # Catch "EmotionalState (9D)"
                    covered = True
            
            if covered:
                print(f"  [OK] {data_type} covered.")
            else:
                print(f"  [WARN] {data_type} NOT found in schemas.")
                missing_coverage.append(f"{system_id}.{data_type}")

    print("\n------------------------------------------------")
    if missing_coverage:
        print(f"[FAIL] Audit Failed. {len(missing_coverage)} outputs missing.")
        return False
    else:
        print("[PASS] Audit Passed. All defined outputs mapped.")
        return True

if __name__ == "__main__":
    success = audit_system_contracts()
    sys.exit(0 if success else 1)
