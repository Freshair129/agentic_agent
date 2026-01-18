"""
Resonance Integrity Subagent (RIS)
Role: Architect & Health Auditor
Version: 1.1.0

Capabilities:
1. Config Auditor: Validates synchronization between YAML configs and Python code.
2. Structure Auditor: Validates file system against Master Registry SSOT.
"""

import os
import sys
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Set, Any

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [RIS] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("RIS")

# Force UTF-8 for Windows terminals
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class ConfigAuditorNode:
    def __init__(self):
        pass

    def flatten_yaml_keys(self, data: Any, prefix: str = "") -> Set[str]:
        """Recursively extracts all keys from a nested dictionary."""
        keys = set()
        if isinstance(data, dict):
            for k, v in data.items():
                full_key = f"{prefix}.{k}" if prefix else k
                keys.add(k) # Add the terminal key itself (heuristic)
                # keys.add(full_key) # Add full path? - Code usually accesses strict keys like config['orchestrator']['parameters']
                
                # Let's add the terminal key mainly, because in code: config['parameters']['mode'] -> we look for "mode"
                
                keys.update(self.flatten_yaml_keys(v, full_key))
        return keys

    def scan_codebase_for_keys(self, source_dir: Path, keys: Set[str]) -> Dict[str, List[str]]:
        """Scans Python files to check if keys are mentioned."""
        if not source_dir.exists():
            logger.error(f"Source directory not found: {source_dir}")
            return {}

        unused_keys = set(keys)
        used_keys = set()
        
        # Simple string matching heuristic
        # We look for "KEY" or 'KEY' in the text content
        
        py_files = list(source_dir.rglob("*.py"))
        logger.info(f"Scanning {len(py_files)} Python files in {source_dir.name}...")
        
        for fpath in py_files:
            try:
                content = fpath.read_text(encoding='utf-8')
                for k in list(unused_keys): # Iterate copy to allow removal
                    # Check for quotes to ensure it's used as a key/string
                    if f"'{k}'" in content or f'"{k}"' in content:
                        unused_keys.remove(k)
                        used_keys.add(k)
            except Exception as e:
                logger.warning(f"Could not read {fpath.name}: {e}")
                
        return {
            "unused": sorted(list(unused_keys)),
            "used_count": len(used_keys),
            "total_keys": len(keys)
        }

    def audit(self, config_path: str, source_dir: str):
        """Main audit execution flow."""
        c_path = Path(config_path)
        s_path = Path(source_dir)
        
        if not c_path.exists():
            logger.error(f"Config file not found: {c_path}")
            return

        logger.info(f"Auditing Config: {c_path.name}")
        
        # 1. Load Config
        try:
            with open(c_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load YAML: {e}")
            return

        # 2. Extract Keys
        all_keys = self.flatten_yaml_keys(data)
        logger.info(f"Examples of keys found: {list(all_keys)[:5]}")
        
        # Filter out generic high-level keys if needed? 
        # For now, keep all.
        
        # 3. Scan Code
        result = self.scan_codebase_for_keys(s_path, all_keys)
        
        # 4. Report
        print("\n" + "="*50)
        print("  RIS CONFIG AUDIT REPORT")
        print("="*50)
        print(f"Target Config: {c_path.name}")
        print(f"Source Code:   {s_path}")
        print("-" * 50)
        print(f"Total Keys:    {result['total_keys']}")
        print(f"Used Keys:     {result['used_count']}")
        print(f"Unused Keys:   {len(result['unused'])}")
        print("-" * 50)
        
        if result['unused']:
            print("[!] POTENTIALLY UNUSED KEYS (Ghosts):")
            for k in result['unused']:
                print(f"  - {k}")
            print("\n(Note: These keys were not found as string literals in the code.)")
        else:
            print("[OK] Integrity Check Passed: All keys appear to be referenced.")
            

class StructureAuditorNode:
    def __init__(self):
        pass

    def audit(self, registry_path: str, project_root: str):
        """Audits the file system against the Master Registry."""
        reg_path = Path(registry_path)
        root_path = Path(project_root)
        
        print("\n" + "="*60)
        print("  RIS STRUCTURE AUDIT REPORT")
        print("="*60)
        print(f"Registry: {reg_path.name}")
        print(f"Root:     {root_path}")
        print("-" * 60)

        if not reg_path.exists():
            logger.error(f"Registry not found: {reg_path}")
            return

        try:
            with open(reg_path, 'r', encoding='utf-8') as f:
                registry = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load Registry: {e}")
            return

        errors = []
        warnings = []

        # 1. Check Root Slots
        print("\n[1] Checking Root Slots...")
        root_slots = registry.get('root_slots', [])
        for slot in root_slots:
            # Handle both string (legacy) and dict (v9.6.2) formats
            slot_name = slot.get('name') if isinstance(slot, dict) else slot
            if not slot_name:
                continue
                
            slot_path = root_path / slot_name
            if not slot_path.exists():
                errors.append(f"[ROOT] Missing root slot: {slot_name}")
                print(f"  ❌ {slot_name} (Missing)")
            else:
                print(f"  ✅ {slot_name}")

        # 2. Check System Manifests
        print("\n[2] Checking System Manifests...")
        systems = registry.get('systems', [])
        for system in systems:
            sys_id = system.get('id', 'Unknown')
            manifest = system.get('manifest', {})
            
            print(f"  > Auditing {sys_id}...")
            
            # Check Root Presence
            if system.get('root_presence', False):
                # Assuming system folder name matches ID or is implicitly the first folder in manifest
                # But typically systems have a primary folder. 
                # Let's rely on manifest 'folders' and 'files' for now.
                pass

            # Check Folders
            for folder in manifest.get('folders', []):
                f_path = root_path / folder
                if not f_path.exists():
                    errors.append(f"[{sys_id}] Missing folder: {folder}")
                    print(f"    ❌ Folder Missing: {folder}")
                # else:
                #     print(f"    ✅ {folder}")

            # Check Files
            for file in manifest.get('files', []):
                f_path = root_path / file
                if not f_path.exists():
                    errors.append(f"[{sys_id}] Missing file: {file}")
                    print(f"    ❌ File Missing: {file}")
                # else:
                #     print(f"    ✅ {file}")
                    
            # Check Chains (for GKS, etc.)
            chains = system.get('chains', {})
            for folder in chains.get('folders', []):
                f_path = root_path / folder
                if not f_path.exists():
                    errors.append(f"[{sys_id}] Missing chain folder: {folder}")
                    print(f"    ❌ Chain Folder Missing: {folder}")
            
            for file in chains.get('files', []):
                f_path = root_path / file
                if not f_path.exists():
                    errors.append(f"[{sys_id}] Missing chain file: {file}")
                    print(f"    ❌ Chain File Missing: {file}")

        print("-" * 60)
        if errors:
            print(f"❌ AUDIT FAILED: Found {len(errors)} discrepancies.")
            for e in errors:
                print(f"  - {e}")
        else:
            print("✅ AUDIT PASSED: Structure matches Registry.")
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Resonance Integrity Subagent (RIS)")
    parser.add_argument("--audit-config", nargs=2, metavar=('CONFIG_PATH', 'SOURCE_DIR'), 
                        help="Check if config keys are used in the source code")
    parser.add_argument("--audit-structure", nargs=2, metavar=('REGISTRY_PATH', 'PROJECT_ROOT'),
                        help="Validate file system against Master Registry")
    
    args = parser.parse_args()
    
    if args.audit_config:
        node = ConfigAuditorNode()
        node.audit(args.audit_config[0], args.audit_config[1])
    elif args.audit_structure:
        node = StructureAuditorNode()
        node.audit(args.audit_structure[0], args.audit_structure[1])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
