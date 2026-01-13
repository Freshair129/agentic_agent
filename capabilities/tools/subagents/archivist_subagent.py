#!/usr/bin/env python3
"""
Archivist Subagent - EVA 9.1.0
A specialized maintenance agent for syncing memory folders, validating schemas, 
and formatting logs.

Usage:
  python archivist_subagent.py --sync
  python archivist_subagent.py --validate
  python archivist_subagent.py --format-log <input_file> <output_file>
"""

import os
import json
import re
import argparse
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger("Archivist")

class ArchivistSubagent:
    def __init__(self, root_path: Optional[str] = None, config_path: Optional[str] = None):
        import yaml
        
        # Load Config
        if not config_path:
            # Default to tools/subagents/configs/archivist_config.yaml
            base_dir = Path(__file__).parent
            config_path = base_dir / "configs" / "archivist_config.yaml"
        
        self.config = {}
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Loaded config from {config_path}")
        else:
            logger.warning(f"Config not found at {config_path}. Using defaults.")

        # Determine Root Path (Arg > Config > Current Dir)
        if root_path:
            self.root_path = Path(root_path)
        elif self.config.get('paths', {}).get('project_root'):
            self.root_path = Path(self.config['paths']['project_root'])
        else:
            self.root_path = Path(os.getcwd())
            
        self.archival_memory_path = self.root_path / "archival_memory"

    def sync_memories(self, dry_run: bool = False):
        """
        Synchronizes episodes_llm and episodes_user folders based on configuration.
        """
        logger.info(f"Starting Memory Sync (Dry Run: {dry_run})...")
        
        # Get targets from config or fallback
        config_targets = self.config.get('paths', {}).get('sync_targets', [])
        if not config_targets:
            # Fallback defaults
            config_targets = [
               "archival_memory/**/*episodic_memory",
               "eva/consciousness/session_memory"
            ]
            
        episodic_dirs = []
        for target_pattern in config_targets:
            # Resolve pattern relative to root
            # Note: glob doesn't support "**/episodic_memory" perfectly with just Path check if we want llm/user
            # Logic: We want folders that contain "episodes_llm"
            
            # Simple approach: If pattern is absolute/relative path
            # Let's support globbing manually
            search_root = self.root_path
            
            # recursive glob for python 3.10+
            for path in search_root.glob(target_pattern):
                if path.is_dir():
                    # Check if this dir HAS episodes_llm or IS episodes_llm parent?
                    # Config says: "archival_memory/**/*episodic_memory"
                    # So path matches .../episodic_memory.
                    # We expect episodes_llm inside it.
                    if (path / "episodes_llm").exists():
                         episodic_dirs.append(path)
                    
                    # Also handle "eva/consciousness/session_memory" which might contain subfolders "session_xx/assets"
                    # If target is "eva/.../session_memory", we need to recurse inside it to find assets?
                    # The pattern "eva/consciousness/session_memory" points to a folder.
                    # Inside are sessions. Inside sessions are assets.
                    # So we should probably make the config pattern more specific: "eva/consciousness/session_memory/**/assets"
                    
                    # Allow recurse search for episodes_llm from the hit point
                    for sub in path.rglob("episodes_llm"):
                        if sub.is_dir():
                            episodic_dirs.append(sub.parent)
                            
        # Deduplicate
        episodic_dirs = list(set(episodic_dirs))
        
        if not episodic_dirs:
            logger.warning("No episodic directories found matching config targets.")
            return

        for ep_dir in episodic_dirs:
            self._sync_folder_pair(ep_dir / "episodes_llm", ep_dir / "episodes_user", dry_run)

    def _sync_folder_pair(self, llm_dir: Path, user_dir: Path, dry_run: bool):
        """Syncs a specific pair of LLM/User episode folders."""
        if not llm_dir.exists() and not user_dir.exists():
            return

        logger.info(f"Scanning: {llm_dir.parent}")
        
        # Get all JSON files sorted by their embedded number
        def get_files_sorted(directory):
            files = []
            if directory.exists():
                for f in directory.glob("*.json"):
                    match = re.search(r"EVA_EP(\d+)", f.name)
                    sort_key = int(match.group(1)) if match else 9999
                    files.append((sort_key, f))
            return sorted(files, key=lambda x: x[0])

        llm_files = get_files_sorted(llm_dir)
        user_files = get_files_sorted(user_dir)
        
        # Determine strict prefix style by looking at the first file
        # Default to "EVA_EP{id}_llm.json" style if unknown
        
        def process_list(file_list, suffix_type):
            current_idx = 1
            for _, old_path in file_list:
                new_id = f"EVA_EP{current_idx:02d}"
                
                # Construct new filename based on old pattern or default
                # basic pattern: "EVA_EP{id}_{type}.json"
                # If old name was "THA..._EVA_EP01.json", we might lose prefix if we aren't careful.
                # But looking at logs, files are "EVA_EP01_llm.json".
                # Let's support preserving "THA" prefix if present.
                
                prefix = ""
                match = re.search(r"(.*)EVA_EP\d+", old_path.name)
                if match:
                    prefix = match.group(1) # e.g. "THA-06_..._" or ""
                
                new_filename = f"{prefix}{new_id}_{suffix_type}.json"
                # Clean up double underscores if any
                new_filename = new_filename.replace("__", "_")
                if not new_filename.endswith(f"_{suffix_type}.json"): 
                     # If prefix captured strictly, ensure suffix is there
                     pass 
                
                # Actually, simpler: just use standardized naming if we are syncing?
                # User asked for "Syncing ... folders". Standardization is usually implied.
                # Let's stick to "EVA_EP{id}_{suffix}.json" for standard purity unless specific prefix found.
                if "THA" in old_path.name:
                     # Keep the complex prefix
                     new_filename = f"{prefix}{new_id}.json" 
                else:
                     new_filename = f"EVA_EP{current_idx:02d}_{suffix_type}.json"

                new_path = old_path.parent / new_filename
                
                # Update Content
                try:
                    with open(old_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    needs_save = False
                    if data.get('episode_id') != new_id:
                        logger.info(f"[{suffix_type.upper()}] ID Update {old_path.name}: {data.get('episode_id')} -> {new_id}")
                        data['episode_id'] = new_id
                        needs_save = True
                    
                    if needs_save:
                        if not dry_run:
                            with open(old_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                        else:
                            logger.info(f"[DRY RUN] Update ID {new_id} in {old_path.name}")
                            
                except Exception as e:
                    logger.error(f"Failed to read/update {old_path}: {e}")

                # Rename
                if old_path.name != new_filename:
                    if not dry_run:
                        try:
                            # Verify target doesn't exist
                            if new_path.exists() and new_path != old_path:
                                logger.warning(f"Target {new_filename} exists, skipping rename of {old_path.name}")
                            else:
                                os.rename(old_path, new_path)
                                logger.info(f"Renamed {old_path.name} -> {new_filename}")
                        except Exception as e:
                            logger.error(f"Rename failed: {e}")
                    else:
                        logger.info(f"[DRY RUN] Rename {old_path.name} -> {new_filename}")
                
                current_idx += 1

        process_list(llm_files, "llm")
        process_list(user_files, "user")

    def validate_schemas(self):
        """Validates JSON files against the V2 Schema."""
        schema_path = self.root_path / "eva/memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json"
        
        if not schema_path.exists():
            logger.error(f"Schema not found at {schema_path}")
            return

        logger.info("Starting Schema Validation...")
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            required_fields = schema.get("required", [])
            logger.info(f"Required fields: {required_fields}")
        except Exception as e:
            logger.error(f"Failed to load schema: {e}")
            return
            
        # Scan all episodes
        episodic_files = list(self.archival_memory_path.rglob("*.json"))
        issues_found = 0
        
        for fpath in episodic_files:
            if "episodes" not in str(fpath.parent): continue # Skip non-episode JSONs if any
            
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                missing = [field for field in required_fields if field not in data]
                if missing:
                    logger.warning(f"Invalid Schema: {fpath.name} missing {missing}")
                    issues_found += 1
                    
            except Exception as e:
                logger.error(f"Corrupted File: {fpath.name} - {e}")
                issues_found += 1
        
        if issues_found == 0:
            logger.info("All files validated successfully!")
        else:
            logger.warning(f"Found {issues_found} invalid files.")

    def format_logs(self, input_path: str, output_path: str):
        """Converts raw logs to human-readable chat format."""
        logger.info(f"Formatting log: {input_path} -> {output_path}")
        
        # Add maintenance to path to allow import
        import sys
        maintenance_path = self.root_path / "maintenance"
        if str(maintenance_path) not in sys.path:
            sys.path.append(str(maintenance_path))
            
        try:
            from convert_chat_log_format import convert_chat_log
            
            formatted, stats = convert_chat_log(Path(input_path))
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            logger.info(f"Success! Stats: {stats}")
        except Exception as e:
            logger.error(f"Error formatting log: {e}")

def main():
    parser = argparse.ArgumentParser(description="EVA Archivist Subagent")
    parser.add_argument("--sync", action="store_true", help="Sync memory folders")
    parser.add_argument("--validate", action="store_true", help="Validate JSON schemas")
    parser.add_argument("--format-log", nargs=2, metavar=('INPUT', 'OUTPUT'), help="Format chat log")
    parser.add_argument("--root", type=str, default=r"e:\The Human Algorithm\T2\eva_core", help="Project root path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without writing")
    
    args = parser.parse_args()
    
    agent = ArchivistSubagent(args.root)
    
    if args.sync:
        agent.sync_memories(dry_run=args.dry_run)
    elif args.validate:
        agent.validate_schemas()
    elif args.format_log:
        agent.format_logs(args.format_log[0], args.format_log[1])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
