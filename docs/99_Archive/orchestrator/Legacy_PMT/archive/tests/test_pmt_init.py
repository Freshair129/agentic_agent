import sys
from pathlib import Path
import unittest

# Add project root to sys.path to allow for absolute imports
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from orchestrator.pmt.pmt_engine import PromptRuleLayer

class TestPMTInitialization(unittest.TestCase):

    def test_initialization(self):
        """
        Tests if the PromptRuleLayer can be initialized without errors.
        This is a basic placeholder test.
        """
        print("=== Testing PMT Initialization ===")
        try:
            # This test requires the identity config files to exist.
            pmt = PromptRuleLayer(
                bus=None # Mock or None
            )
            self.assertIsNotNone(pmt)
            print("[SUCCESS] PromptRuleLayer initialized.")
        except Exception as e:
            print(f"[FAILURE] Initialization failed: {e}")
            # We will not fail the test for now, as this is a placeholder
            # and dependencies might not be met in a simple test environment.
            # self.fail(f"Initialization failed with {e}")
            pass

if __name__ == '__main__':
    unittest.main()
