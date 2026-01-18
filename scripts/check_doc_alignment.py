
import os
import re
import yaml
from pathlib import Path

# Configuration: Which files define the 'version' truth?
REGISTRY_PATH = "registry/eva_master_registry.yaml"

# Which files MUST match the registry version?
CRITICAL_DOCS = [
    "docs/00_Governance/README.md",
    "docs/00_Governance/INDEX.md",
    "docs/03_Architecture/EVA_System_Architecture.md",
    "docs/00_Governance/RULES_ALIGNMENT_AUDIT.md",
    "docs/00_Governance/CHANGELOG.md"
]

def check_documentation_alignment():
    print(f"SCANNING: Documentation Alignment Check")
    print(f"   Root: {os.getcwd()}")
    
    # 1. Load Registry Truth
    if not os.path.exists(REGISTRY_PATH):
        print(f"CRITICAL: Registry not found at {REGISTRY_PATH}")
        return False
        
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f)
            # Assuming 'version' in registry root is the Organism Version
            truth_version = registry.get('version', 'UNKNOWN')
            print(f"   Organizer Version (SSOT): v{truth_version}")
    except Exception as e:
        print(f"Error loading registry: {e}")
        return False

    errors = []
    
    # 2. Check Critical Docs
    # Pattern: Match vX.X.X if it's not part of a URL or preceded by /
    # Specifically looking for headers or start of lines
    version_pattern = re.compile(r"(?:^|\s|#|\[)v\s*(\d+\.\d+\.\d+)", re.IGNORECASE | re.MULTILINE)
    
    for relative_path in CRITICAL_DOCS:
        doc_path = Path(relative_path)
        if not doc_path.exists():
            errors.append(f"MISSING: {relative_path}")
            continue
            
        content = doc_path.read_text(encoding='utf-8')
        
        # Heuristic: Check the first 1000 characters for "Version: X.X.X" or "vX.X.X" header
        # We skip matches that look like semver URLs
        header_chunk = content[:1000] 
        matches = version_pattern.finditer(header_chunk)
        
        doc_version = None
        for m in matches:
            v = m.group(1)
            # Simple heuristic: skip 2.0.0 if it's near semver.org (standard link)
            if v == "2.0.0" and "semver.org" in header_chunk:
                continue
            doc_version = v
            break
        
        if doc_version:
            if doc_version != truth_version:
                errors.append(f"MISMATCH: {relative_path} (Doc=v{doc_version}, Registry=v{truth_version})")
            else:
                print(f"   [OK] {relative_path} matches v{doc_version}")
        else:
            errors.append(f"NO VERSION FOUND: {relative_path} (Header missing 'vX.X.X')")

    # 3. Report
    print("-" * 40)
    if errors:
        print("ALIGNMENT FAILED:")
        for e in errors:
            print(f"   - {e}")
        print("\nACTION REQUIRED: Update these documents to match the Registry SSOT.")
    else:
        print("ALL SYSTEMS ALIGNED. Documentation matches Registry.")

if __name__ == "__main__":
    check_documentation_alignment()
