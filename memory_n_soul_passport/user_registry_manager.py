"""
User Registry Manager
Manages multiple user identities and speaker identification
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class UserRegistryManager:
    """
    Central registry for all known users.
    Handles speaker identification, auto-registration, and profile management.
    """
    
    def __init__(self, registry_path: str = "eva/memory/user_registry.json"):
        self.registry_path = Path(registry_path)
        self.users: Dict[str, dict] = {}
        self.active_user: Optional[str] = None
        self._load_registry()
    
    def _load_registry(self):
        """Load existing registry or create default"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.users = data.get("users", {})
                self.active_user = data.get("active_user")
        else:
            # Create default with primary admin (THA-06)
            self._create_default_registry()
    
    def _create_default_registry(self):
        """Initialize registry with primary admin (Founder)"""
        self.users = {
            "FD_01": {
                "user_id": "FD_01",
                "username": "THA-06",
                "display_name": "THA-06",
                "aliases": ["บอส", "Boss", "THA"],
                "role": "primary_admin",
                "level": "Founder / Dev",
                "priority": 1,
                "registration_date": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "interaction_count": 0,
                "trust_level": 1.0
            }
        }
        self.active_user = "FD_01"
        self._save_registry()
    
    def _save_registry(self):
        """Persist registry to disk"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "schema_version": "1.0.0",
            "users": self.users,
            "active_user": self.active_user,
            "auto_register": True
        }
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def register_user(
        self, 
        username: str, 
        role: str = "user",
        level: str = "User",
        priority: int = 10,
        aliases: List[str] = None
    ) -> str:
        """
        Register a new user and return assigned user_id
        
        Args:
            username: Display name (e.g., "แอน")
            role: User role (user, friend, colleague, admin)
            level: Priority level (e.g., "Founder / Dev", "Friend", "User")
            priority: Numeric priority (1=highest, 10=lowest)
            aliases: Alternative names
        
        Returns:
            user_id (e.g., "U_002", "FD_02")
        """
        # Determine prefix based on role
        prefix_map = {
            "founder": "FD",        # Founder
            "primary_admin": "FD",  # Founder/Primary Admin
            "dev": "DV",            # Developer
            "admin": "AD",          # Admin
            "superuser": "SU",      # Superuser (elevated privileges)
            "user": "U"             # Regular user
        }
        prefix = prefix_map.get(role, "U")
        
        # Generate next user_id for this prefix
        same_prefix_ids = [int(uid.split('_')[1]) for uid in self.users.keys() if uid.startswith(prefix)]
        next_id = max(same_prefix_ids) + 1 if same_prefix_ids else 1
        user_id = f"{prefix}_{next_id:02d}"
        
        # Create user entry
        self.users[user_id] = {
            "user_id": user_id,
            "username": username,
            "display_name": username,
            "aliases": aliases or [],
            "role": role,
            "level": level,
            "priority": priority,
            "registration_date": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "interaction_count": 0,
            "trust_level": 0.5 if role != "primary_admin" else 1.0
        }
        
        self._save_registry()
        return user_id
    
    def identify_speaker(
        self, 
        input_text: str,
        context: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Identify speaker from input text or context
        
        Args:
            input_text: User's raw input
            context: Optional context (previous speaker, etc.)
        
        Returns:
            {
                "user_id": "U_001",
                "username": "THA-06",
                "role": "primary_admin",
                "confidence": 0.95
            }
        """
        # Strategy 1: Use active_user if no switch detected
        if self.active_user:
            active_user_data = self.users.get(self.active_user)
            if active_user_data:
                return {
                    "user_id": self.active_user,
                    "username": active_user_data["username"],
                    "role": active_user_data["role"],
                    "confidence": 0.8  # Default confidence
                }
        
        # Strategy 2: Detect name in input (simple heuristic)
        input_lower = input_text.lower()
        for user_id, user_data in self.users.items():
            # Check username
            if user_data["username"].lower() in input_lower:
                return {
                    "user_id": user_id,
                    "username": user_data["username"],
                    "role": user_data["role"],
                    "confidence": 0.7
                }
            # Check aliases
            for alias in user_data.get("aliases", []):
                if alias.lower() in input_lower:
                    return {
                        "user_id": user_id,
                        "username": user_data["username"],
                        "role": user_data["role"],
                        "confidence": 0.9  # Higher confidence for explicit alias
                    }
        
        # Strategy 3: Return unknown
        return {
            "user_id": "unknown",
            "username": "unknown",
            "role": "unknown",
            "confidence": 0.0
        }
    
    def set_active_user(self, user_id: str):
        """Set the active speaker for current session"""
        if user_id in self.users:
            self.active_user = user_id
            self.users[user_id]["last_seen"] = datetime.now().isoformat()
            self._save_registry()
            return True
        return False
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user registry data by ID (Lightweight)"""
        return self.users.get(user_id)

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Load full detailed user profile from disk
        """
        user_entry = self.users.get(user_id)
        if not user_entry:
            return None
            
        profile_path = user_entry.get("profile_path")
        if not profile_path:
            # Fallback path if not explicit
            profile_path = f"user_profiles/{user_id}_profile.json"
            
        full_path = self.registry_path.parent / profile_path
        
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[UserRegistry] ⚠️ Error loading profile {full_path}: {e}")
                return user_entry # Return just registry data as fallback
        
        return user_entry # Return minimal data if no profile file

    def list_users(self) -> List[Dict]:
        """List all registered users"""
        return list(self.users.values())
    
    def increment_interaction(self, user_id: str):
        """Increment interaction count for user"""
        if user_id in self.users:
            self.users[user_id]["interaction_count"] += 1
            self.users[user_id]["last_seen"] = datetime.now().isoformat()
            self._save_registry()
