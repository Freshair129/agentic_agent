import sys
import os
from pathlib import Path

# Add root to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from operation_system.identity_manager import IdentityManager
from memory_n_soul_passport.user_registry_manager import UserRegistryManager

def test_id_generation():
    print("[1] Testing IdentityManager user_id generation...")
    test_cases = [
        ("founder", 1, "FD_01"),
        ("primary_admin", 2, "FD_02"),
        ("dev", 1, "DV_01"),
        ("admin", 1, "AD_01"),
        ("superuser", 1, "SU_01"),
        ("user", 5, "U_05"),
        ("unknown", 1, "U_01"), # Default fallback
    ]
    
    for role, index, expected in test_cases:
        gen_id = IdentityManager.generate_user_id(role, index)
        if gen_id == expected:
            print(f"  [OK] Role '{role}' Index '{index}' -> '{gen_id}'")
        else:
            print(f"  [ERROR] Role '{role}' Index '{index}' -> Expected '{expected}', got '{gen_id}'")
            return False
    return True

def test_registry_integration():
    print("\n[2] Testing UserRegistryManager integration...")
    temp_registry = root_path / "memory/test_user_registry.json"
    if temp_registry.exists():
        temp_registry.unlink()
        
    try:
        manager = UserRegistryManager(registry_path=str(temp_registry))
        
        # Register a new user
        uid = manager.register_user(username="TestUser", role="dev")
        
        if uid == "DV_01":
            print(f"  [OK] Registered Dev -> '{uid}' (Correct format from IdentityManager)")
        else:
            print(f"  [ERROR] Registered Dev -> Got '{uid}', expected 'DV_01'")
            return False
            
        # Register another user
        uid2 = manager.register_user(username="AnotherUser", role="user")
        if uid2 == "U_01":
            print(f"  [OK] Registered User -> '{uid2}'")
        else:
            print(f"  [ERROR] Registered User -> Got '{uid2}', expected 'U_01'")
            return False
            
        return True
    finally:
        if temp_registry.exists():
            temp_registry.unlink()

if __name__ == "__main__":
    success = test_id_generation()
    if success:
        success = test_registry_integration()
        
    if success:
        print("\n[SUCCESS] User Registry Integration Verified Successfully!")
    else:
        print("\n[FAILED] Verification Failed!")
        sys.exit(1)
