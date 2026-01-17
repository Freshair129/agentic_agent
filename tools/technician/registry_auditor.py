import yaml
import os
import re
from pathlib import Path

class RegistryAuditor:
    def __init__(self, registry_path: str, root_path: str):
        self.registry_path = registry_path
        self.root_path = Path(root_path)
        with open(registry_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def audit_structure(self):
        print(f"--- [AUDIT] Registry Version: {self.data.get('version')} ---")
        
        # 1. Check Root Slots
        root_slots = self.data.get('root_slots', [])
        actual_dirs = [d.name for d in self.root_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        print("\n[STEP 1: ROOT SLOT AUDIT]")
        for d in actual_dirs:
            if d not in root_slots:
                print(f"[!] GHOST FOLDER FOUND: '{d}' (Not in root_slots)")
            else:
                print(f"[OK] Authorized slot: '{d}'")

        # 2. Check Manifests and Main Files
        print("\n[STEP 2: MANIFEST & FILE AUDIT]")
        for system in self.data.get('systems', []):
            sys_id = system.get('id')
            manifest = system.get('manifest', {})
            
            # Check Files in Manifest
            for file_path in manifest.get('files', []):
                full_path = self.root_path / file_path
                if not full_path.exists():
                    print(f"[ERR] MISSING FILE ({sys_id}): {file_path}")
                else:
                    print(f"[OK] Verified file: {file_path}")

        # 3. ID Matching with IdentityManager.py
        print("\n[STEP 3: CODE-ID SYNC AUDIT]")
        idm_path = self.root_path / "operation_system" / "identity_manager.py"
        if idm_path.exists():
            with open(idm_path, 'r', encoding='utf-8') as f:
                content = f.read()
                registry_ids = [s.get('id') for s in self.data.get('systems', [])]
                for rid in registry_ids:
                    if rid not in content:
                        print(f"[!] ID MISMATCH: '{rid}' exists in Registry but NOT found in IdentityManager.py constants.")
                    else:
                        print(f"[OK] ID Synced: '{rid}'")

        # 4. Dependency Visibility
        print("\n[STEP 4: DEPENDENCY VISIBILITY]")
        for system in self.data.get('systems', []):
            sys_id = system.get('id')
            print(f"System: {sys_id}")
            for module in system.get('modules', []):
                deps = module.get('dependencies', [])
                if deps:
                    print(f"  - Module '{module.get('id')}' depends on: {deps}")
                else:
                    print(f"  - Module '{module.get('id')}' has NO registered dependencies.")

if __name__ == "__main__":
    auditor = RegistryAuditor("registry/eva_master_registry.yaml", ".")
    auditor.audit_structure()
