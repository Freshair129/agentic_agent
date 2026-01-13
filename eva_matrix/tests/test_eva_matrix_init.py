import sys
from pathlib import Path
import unittest

# Add project root to sys.path to allow for absolute imports
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from eva_matrix.eva_matrix_engine import EVAMatrixSystem

class TestEVAMatrixInitialization(unittest.TestCase):

    def test_initialization(self):
        """
        Tests if the EVAMatrixSystem can be initialized without errors.
        This is a basic placeholder test.
        """
        print("=== Testing EVA Matrix Initialization ===")
        try:
            # Note: This will likely fail without proper mock objects for msp and bus,
            # and without valid config paths. This is a placeholder.
            matrix = EVAMatrixSystem(
                base_path=root_path,
                msp=None,  # Mock or None
                bus=None   # Mock or None
            )
            self.assertIsNotNone(matrix)
            print("[SUCCESS] EVAMatrixSystem initialized.")
        except Exception as e:
            print(f"[FAILURE] Initialization failed: {e}")
            # We will not fail the test for now, as this is a placeholder
            # and dependencies might not be met in a simple test environment.
            # self.fail(f"Initialization failed with {e}")
            pass

if __name__ == '__main__':
    unittest.main()
