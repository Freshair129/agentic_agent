
"""
Integration Test for MSP Phase 3: Context & Persistence
Validates Session Digest upgrades and Enhanced Retrieval Logic.
"""
import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_n_soul_passport.memory_n_soul_passport_engine import MSP

class TestMSPPhase3(unittest.TestCase):
    
    def setUp(self):
        # Mock dependencies to prevent real initialization
        with patch('memory_n_soul_passport.memory_n_soul_passport_engine.UserRegistryManager'), \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.EpisodicMemoryModule'), \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.SemanticMemoryModule'), \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.SensoryMemoryModule'), \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.RMSEngineV6'):
             
            self.msp = MSP(cache_size=10)
            
    def test_calculate_session_biostats(self):
        """Test bio-stat aggregation logic"""
        episodes = [
            {
                "episode_id": "EP1", 
                "state_snapshot": {
                    "physio": {"vitals": {"bpm": 60, "vagus_tone": 0.5}},
                    "trauma_flag": False,
                    "resonance_texture": {"stress": 0.1, "calm": 0.9}
                }
            },
            {
                "episode_id": "EP2", 
                "state_snapshot": {
                    "physio": {"vitals": {"bpm": 80, "vagus_tone": 0.4}},
                    "trauma_flag": True,
                    "resonance_texture": {"stress": 0.5, "calm": 0.5}
                }
            }
        ]
        
        stats = self.msp._calculate_session_biostats(episodes)
        
        self.assertEqual(stats["avg_bpm"], 70.0)
        self.assertEqual(stats["avg_vagus"], 0.45)
        self.assertEqual(stats["trauma_count"], 1)
        self.assertEqual(stats["avg_texture"]["stress"], 0.3)
        self.assertEqual(stats["avg_texture"]["calm"], 0.7)
        print("\n✅ Bio-Stats Calculation verified.")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_session_memory_content(self, mock_file):
        """Test markdown generation includes new section"""
        session_data = {
            "session_id": "SES_TEST",
            "digest_summary": {
                "avg_bpm": 72.5,
                "avg_vagus": 0.6,
                "trauma_count": 2,
                "avg_texture": {"stress": 0.4, "calm": 0.6}
            }
        }
        
        self.msp.session_memory_dir = Path("/tmp")
        self.msp.write_session_memory(session_data)
        
        # Check written content
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        
        self.assertIn("## 🧬 Bio-Cognitive Profile (Avg)", written_content)
        self.assertIn("BPM 72.5", written_content)
        # Fix markdown assertion: matches "**Trauma Flags:** 2"
        self.assertIn("**Trauma Flags:** 2", written_content)
        self.assertIn("Resonance Texture:", written_content)
        print("\n✅ Session Digest Markdown verified.")

    def test_retrieve_by_state_similarity(self):
        """Test enhanced retrieval logic (Unit Test Module Logic Directly)"""
        # Import the real module locally to avoid MSP mock interference
        from memory_n_soul_passport.Module.EpisodicMemory.EpisodicMemoryModule import EpisodicMemoryModule
        
        # Mock config
        mock_config = {"module_definitions": {"episodic_memory_module": {"parameters": {}}}}
        
        # Instantiate real module
        module = EpisodicMemoryModule(mock_config)
        module.journal = MagicMock()
        
        # Setup Journal Mocks
        module.journal.read_log.return_value = [
            {"episode_id": "EP1"}, {"episode_id": "EP2"}
        ]
        
        def mock_read_full(ep_id):
            if ep_id == "EP1":
                return {
                    "episode_id": "EP1",
                    "state_snapshot": {
                        "resonance_index": 0.8, # Renamed
                        "qualia": {"intensity": 0.8},
                        "resonance_texture": {"stress": 0.8}, # High stress match
                        "eva_matrix": {} # Added
                    }
                }
            if ep_id == "EP2":
                return {
                    "episode_id": "EP2",
                    "state_snapshot": {
                        "resonance_index": 0.2, # Renamed
                        "qualia": {"intensity": 0.2},
                        "resonance_texture": {"stress": 0.1}, # Low stress match
                        "eva_matrix": {} # Added
                    }
                }
            return None

        module.journal.read_full_episode.side_effect = mock_read_full
        
        # Search Target: High Intensity, High Stress
        target_state = {
            "Resonance_index": 0.9,
            "qualia": {"intensity": 0.9},
            "resonance_texture": {"stress": 0.9}
        }
        
        # We expect EP1 to be ranked first (closest)
        results = module.retrieve_by_state_similarity(target_state, limit=2)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["episode_id"], "EP1")
        self.assertEqual(results[1]["episode_id"], "EP2")
        print("\n✅ Retrieval Logic (Similarity Search) verified.")

if __name__ == '__main__':
    # Windows fix
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
    unittest.main()
