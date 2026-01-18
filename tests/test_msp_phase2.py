
"""
Integration Test for MSP Phase 2: Data Pipeline Integration
Validates that write_episode() correctly aggregates full bio-cognitive state.
"""
import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_n_soul_passport.memory_n_soul_passport_engine import MSP

class TestMSPPhase2(unittest.TestCase):
    
    def setUp(self):
        # Mock dependencies
        with patch('memory_n_soul_passport.memory_n_soul_passport_engine.UserRegistryManager') as mock_user_reg, \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.EpisodicMemoryModule') as mock_ep_mod, \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.SemanticMemoryModule') as mock_sem_mod, \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.SensoryMemoryModule') as mock_sen_mod, \
             patch('memory_n_soul_passport.memory_n_soul_passport_engine.RMSEngineV6') as mock_rms:
             
            self.msp = MSP(cache_size=10)
            
            # Setup mock episodic module
            self.mock_episodic = self.msp.episodic_module
            self.mock_episodic.consolidate_interaction.return_value = "EP_TEST_001"
            
    def test_write_episode_aggregates_state(self):
        """Test that write_episode aggregates all active states into snapshot"""
        
        # 1. Setup Active State (Mocking system inputs)
        matrix_state = {
            "axes_9d": {"stress": 0.5, "warmth": 0.8},
            "emotion_label": "Content",
            "momentum": {"intensity": 0.2}
        }
        physio_state = {
            "vitals": {"bpm": 75, "rpm": 16, "vagus_tone": 0.8}
        }
        qualia_state = {
            "intensity": 0.7,
            "tone": "warm",
            "coherence": 0.9,
            "depth": 0.5,
            "texture": {"softness": 0.8}
        }
        
        # Set states manually in cache
        timestamp = datetime.now().isoformat()
        self.msp._active_state_cache["matrix_state"] = {"data": matrix_state, "timestamp": timestamp}
        self.msp._active_state_cache["physio_state"] = {"data": physio_state, "timestamp": timestamp}
        self.msp._active_state_cache["qualia_state"] = {"data": qualia_state, "timestamp": timestamp}
        self.msp._active_state_cache["resonance_texture"] = {"data": {"stress": 0.2, "calm": 0.8}, "timestamp": timestamp}
        self.msp._active_state_cache["trauma_flag"] = {"data": False, "timestamp": timestamp}
        self.msp._active_state_cache["reflex_directives"] = {"data": {"freeze": False}, "timestamp": timestamp}
        # Scalars also need wrapping 
        self.msp._active_state_cache["resonance_index"] = {"data": 0.0, "timestamp": timestamp}
        self.msp._active_state_cache["memory_encoding_level"] = {"data": "L1_light", "timestamp": timestamp}
        self.msp._active_state_cache["memory_color"] = {"data": "#808080", "timestamp": timestamp}
        
        # 2. Call write_episode
        episode_data = {
            "turn_user": {"text": "Hello"},
            "turn_llm": {"text": "Hi there"}
        }
        ep_id = self.msp.write_episode(episode_data)
        
        # 3. Verify
        self.assertEqual(ep_id, "EP_TEST_001")
        
        # Check call arguments
        # args[0] is episode_data
        args, _ = self.mock_episodic.consolidate_interaction.call_args
        passed_data = args[0]
        
        snapshot = passed_data["state_snapshot"]
        
        # Check Keys
        self.assertIn("EVA_matrix", snapshot)
        self.assertIn("physio", snapshot)
        self.assertIn("qualia", snapshot)
        self.assertIn("resonance_texture", snapshot)
        
        # Check Inner Values
        self.assertEqual(snapshot["EVA_matrix"]["emotion_label"], "Content")
        self.assertEqual(snapshot["EVA_matrix"]["momentum"]["intensity"], 0.2)
        
        self.assertEqual(snapshot["physio"]["vitals"]["bpm"], 75)
        
        self.assertEqual(snapshot["qualia"]["tone"], "warm")
        self.assertEqual(snapshot["qualia"]["texture"]["softness"], 0.8)
        
        self.assertEqual(snapshot["resonance_texture"]["calm"], 0.8)
        
        print("\n✅ write_episode() successfully aggregated full state snapshot.")

if __name__ == '__main__':
    # Fix Windows console UTF-8 encoding
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
    unittest.main()
