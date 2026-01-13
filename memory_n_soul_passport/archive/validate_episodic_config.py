import yaml
import json
from pathlib import Path
import sys

def check_recursive(data, path=""):
    missing = []
    if isinstance(data, dict):
        # If it's a property definition, check for description
        # Skip if it's just a ref (documented at target) or if it's already a child of a documented property
        if ('type' in data or '$ref' in data) and 'description' not in data:
            # Special case: don't require description for refs if they are just pointing to definitions
            if not ('$ref' in data and data['$ref'].startswith('#/definitions/')):
                 if 'writes by' not in data.get('description', '').lower():
                     missing.append(path)
        elif 'type' in data and 'description' in data:
            if 'writes by' not in data['description'].lower():
                missing.append(path)
        
        for k, v in data.items():
            if k in ['properties', 'definitions']:
                missing.extend(check_recursive(v, path))
            elif k == 'additionalProperties':
                # Skip additionalProperties if it's just a ref to a definition
                if isinstance(v, dict) and '$ref' in v and v['$ref'].startswith('#/definitions/'):
                    continue
                missing.extend(check_recursive(v, path))
            elif isinstance(v, dict):
                new_path = f"{path}.{k}" if path else k
                missing.extend(check_recursive(v, new_path))
    return missing

def validate():
    root = Path(__file__).parent
    yaml_path = root / "episodic_Memory_configs.yaml"
    
    print(f"Validating {yaml_path.name}...")

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        print("YAML parsed successfully.")
    except Exception as e:
        print(f"YAML Parse Error: {e}")
        return False

    # Check for "writes by" recursively
    missing_desc = check_recursive(yaml_data.get('properties', {}), "properties")
    missing_desc.extend(check_recursive(yaml_data.get('definitions', {}), "definitions"))

    # Filter out known exceptions
    filtered_missing = [m for m in missing_desc if not any(x in m for x in ['.required', '.enum', '.items', '.minimum', '.maximum'])]

    if filtered_missing:
        print(f"Found missing 'writes by' descriptions in: {filtered_missing}")
        return False
    else:
        print("All relevant fields have 'writes by' declarations.")

    print("\nValidation Complete!")
    return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
