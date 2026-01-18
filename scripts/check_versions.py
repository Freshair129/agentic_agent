import yaml
import re
import os
import sys
from pathlib import Path

# Force UTF-8 for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
REGISTRY_PATH = Path("registry/eva_master_registry.yaml")
AGENT_ROOT = Path(__file__).parent.parent

# Mapping System ID to likely file paths (Heuristic)
# In a perfect world, this would be in the registry too, but for now we map manually or search
SYSTEM_FILE_MAP = {
    "PhysioCore": "physio_core/physio_core.py",
    "EVA_Matrix": "eva_matrix/eva_matrix.py",
    "MSP": "memory_n_soul_passport/memory_n_soul_passport_engine.py",
    "Orchestrator": "orchestrator/orchestrator.py",
    "GKS": "genesis_knowledge_system/gks_interface.py",
    "RMS": "consciousnes/resonance_memory_system/resonance_memory_system.py", # Check path
    "Artifact_Qualia": "artifact_qualia/artifact_qualia.py",
    "AgenticRAG": "capabilities/services/agentic_rag/agentic_rag_service.py",
    "Resonance_Bus": "operation_system/resonance_bus/resonance_bus.py",
    "Identity_Manager": "operation_system/identity_manager.py",
    "TrajectoryStrategy": "operation_system/trajectory/trajectory_manager.py",
    "ResonanceEngine": "operation_system/resonance_engine/resonance_engine.py",
    "UmbrellaEngine": "operation_system/umbrella/umbrella_engine.py",
    "AppraisalEngine": "operation_system/mrf_engine/mrf_engine.py", # MRF
    "EngramSystem": "capabilities/services/engram_system/engram_engine.py"
}

def find_system_file(system_id):
    """Resolve system ID to a file path."""
    if system_id in SYSTEM_FILE_MAP:
        path = AGENT_ROOT / SYSTEM_FILE_MAP[system_id]
        if path.exists():
            return path
        
        # Try finding anywhere if explicit map fails
        # This is expensive, so mainly use map
        pass
        
    return None

def extract_version_from_code(file_path):
    """Extract Version: X.Y.Z from file header."""
    try:
        content = file_path.read_text(encoding='utf-8')
        match = re.search(r'Version:\s*([\d\.]+)', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return "Missing"

def check_system_versions():
    print(f"🔍 Starting Version Audit against {REGISTRY_PATH}...")
    
    if not (AGENT_ROOT / REGISTRY_PATH).exists():
        print(f"❌ Critical: Registry not found at {AGENT_ROOT / REGISTRY_PATH}")
        return False

    try:
        registry = yaml.safe_load((AGENT_ROOT / REGISTRY_PATH).read_text(encoding='utf-8'))
    except Exception as e:
        print(f"❌ Critical: Registry YAML invalid: {e}")
        return False
    
    errors = []
    checked_count = 0

    # 1. Check Systems
    if 'systems' in registry:
        systems_data = registry['systems']
        # Handle if systems is a dict (categorized) or list (flat)
        if isinstance(systems_data, dict):
            # Flatten dict values into a single list
            all_systems = []
            for category, sys_list in systems_data.items():
                if isinstance(sys_list, list):
                    all_systems.extend(sys_list)
            systems_data = all_systems
            
        if isinstance(systems_data, list):
            for system in systems_data:
                if not isinstance(system, dict): continue
                
                system_id = system.get('id')
                expected_version = system.get('version')
                
                if not system_id or not expected_version:
                    continue

                # Find corresponding Python file
                file_path = find_system_file(system_id)
                
                if not file_path:
                    # Optional: Warn if file not mapped/found
                    # print(f"⚠️  Skipping {system_id} (File not mapped)")
                    continue
                    
                checked_count += 1
                code_version = extract_version_from_code(file_path)
                
                if code_version != expected_version:
                    errors.append(f"❌ {system_id}: Registry[{expected_version}] != Code[{code_version}] in {file_path.name}")
                else:
                    print(f"✅ {system_id}: v{expected_version}")

    # 2. Check Capabilities (if versioned)
    # (Optional expansion)

    print("\n" + "="*40)
    print(f"Summary: Checked {checked_count} systems.")
    
    if errors:
        print(f"🚨 FAILED: Found {len(errors)} version mismatches.")
        for error in errors:
            print(error)
        return False
    else:
        print("✨ SUCCESS: All code headers match the Registry (SSOT).")
        return True

if __name__ == "__main__":
    success = check_system_versions()
    exit(0 if success else 1)
