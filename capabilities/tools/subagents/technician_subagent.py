"""
Technician Subagent (The Worker)
Role: Deterministic Code Modifier (Token Saver)
Version: 1.0.0
Description: Reads a 'task_order.yaml' and executes precise file operations.
"""

import sys
import yaml
import re
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="[TECHNICIAN] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Technician")

class TechnicianAgent:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        logger.info(f"Worker initiated at: {self.root}")

    def execute_order(self, order_path: str):
        path = Path(order_path)
        if not path.exists():
            logger.error(f"Order file not found: {path}")
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                order = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to parse order: {e}")
            return

        logger.info(f"Executing Order: {order.get('mission_name', 'Unnamed')}")
        
        tasks = order.get('tasks', [])
        for i, task in enumerate(tasks):
            logger.info(f"--- Task {i+1}/{len(tasks)} ---")
            self.perform_task(task)

        logger.info("Mission Complete.")

    def perform_task(self, task: Dict[str, Any]):
        target = task.get('file')
        ops = task.get('ops', [])
        
        target_path = self.root / target
        
        # 0. Handle Deletion
        if task.get('action') == 'delete':
            if target_path.exists():
                try:
                    if target_path.is_dir():
                        # Simple recursive delete for directory
                        import shutil
                        shutil.rmtree(target_path)
                        logger.info(f"Deleted directory: {target}")
                    else:
                        target_path.unlink()
                        logger.info(f"Deleted file: {target}")
                except Exception as e:
                    logger.error(f"Failed to delete {target}: {e}")
            else:
                logger.warning(f"Deletion target not found: {target}")
            return

        # 1. Handle File Creation
        if not target_path.exists():
            if task.get('create_if_missing', False):
                logger.info(f"Creating new file: {target}")
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text("", encoding='utf-8')
            else:
                logger.error(f"Target file not found: {target}")
                return

        try:
            content = target_path.read_text(encoding='utf-8')
            modified = content
            
            for op in ops:
                op_type = op.get('type')
                
                if op_type == 'replace_exact':
                    find = op.get('find')
                    replace = op.get('replace')
                    if find in modified:
                        modified = modified.replace(find, replace)
                        logger.info(f"Applied 'replace_exact' on {target}")
                    else:
                        logger.warning(f"String not found for 'replace_exact' in {target}")

                elif op_type == 'regex_sub':
                    pattern = op.get('pattern')
                    repl = op.get('replace')
                    if re.search(pattern, modified, re.MULTILINE):
                        modified = re.sub(pattern, repl, modified, flags=re.MULTILINE)
                        logger.info(f"Applied 'regex_sub' on {target}")
                    else:
                        logger.warning(f"Pattern not found for 'regex_sub' in {target}")

                elif op_type == 'append':
                    text = op.get('text')
                    modified += "\n" + text
                    logger.info(f"Applied 'append' on {target}")

                elif op_type == 'rewrite':
                    modified = op.get('content')
                    logger.info(f"Applied 'rewrite' on {target}")

            if modified != content:
                target_path.write_text(modified, encoding='utf-8')
                logger.info(f"Saved changes to {target}")
            else:
                logger.info(f"No changes made to {target}")

        except Exception as e:
            logger.error(f"Error processing {target}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Technician Subagent")
    parser.add_argument("order_file", help="Path to task_order.yaml")
    args = parser.parse_args()
    
    agent = TechnicianAgent()
    agent.execute_order(args.order_file)

if __name__ == "__main__":
    main()
