#!/usr/bin/env python3
"""gks_standardizer.py
Utility to validate and standardize all Genesis block JSON files in the EVA project.
It enforces a unified schema:
    {
        "Block_ID": "<type>::<name>",
        "Type": "<Category>",
        "Version": "v1.0",
        "Core_Definition": "...",
        "Key_Trigger": ["..."],
        "Source_Memory": {
            "episode_ref": "...",
            "cite": "...",
            "summary": "..."
        },
        "Summary": "..."
    }
If a field is missing it will be added with a placeholder.
The script also removes any unapproved blocks (e.g., Time_When_Genesis_Block.json).
"""
import json, os, sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCHEMA_FIELDS = ["Block_ID", "Type", "Version", "Core_Definition", "Key_Trigger", "Source_Memory", "Summary"]
DEFAULTS = {
    "Version": "v1.0",
    "Key_Trigger": [],
    "Source_Memory": {},
    "Summary": "",
}

def load_json(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(fp, data):
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def standardize(data, filename):
    # Ensure required keys exist
    for key in SCHEMA_FIELDS:
        if key not in data:
            data[key] = DEFAULTS.get(key, "")
    # Add placeholder Block_ID if missing
    if "Block_ID" not in data or not data["Block_ID"]:
        stem = Path(filename).stem.replace("_", "::")
        data["Block_ID"] = f"{stem}"
    # Ensure Key_Trigger is a list
    if isinstance(data["Key_Trigger"], str):
        data["Key_Trigger"] = [data["Key_Trigger"]]
    return data

def main():
    json_files = [p for p in BASE_DIR.iterdir() if p.suffix == ".json"]
    for fp in json_files:
        if fp.name.startswith("Time_When"):  # unapproved block
            print(f"Removing unapproved file {fp.name}")
            fp.unlink()
            continue
        try:
            data = load_json(fp)
            data = standardize(data, fp.name)
            save_json(fp, data)
            print(f"Standardized {fp.name}")
        except Exception as e:
            print(f"Error processing {fp.name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
