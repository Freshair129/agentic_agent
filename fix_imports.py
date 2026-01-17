import os
from pathlib import Path

root = Path(r"e:\The Human Algorithm\T2\agent")

replacements = {
    "from eva.": "from ",
    "from tools.": "from capabilities.tools.",
    "import eva.": "import "
}

def fix_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {file_path}")
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

if __name__ == "__main__":
    for py_file in root.rglob("*.py"):
        # Skip this script
        if py_file.name == "fix_imports.py":
            continue
        fix_file(py_file)
    print("Done.")
