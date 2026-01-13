"""
EVA 9.1.0 - GraphRAG Engine
The central engine for Interaction with the Neo4j Knowledge Graph.
Integrates Semantic Search (Chroma), Graph Traversal (Neo4j), and Bio-State Resonance.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from services.graph_bridge.graph_client import EVAGraphClient
# Assuming VectorBridge interface exists or we use the client directly
# from services.vector_bridge.chroma_bridge import ChromaVectorBridge 

logger = logging.getLogger(__name__)

class GraphRAGEngine:
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", 
                 neo4j_password: Optional[str] = None):
        
        # Connect to Neo4j
        self.graph = EVAGraphClient(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
        
        # TODO: Initialize Vector Store (Chroma) connection if needed for hybrid search
        # self.vector_store = ChromaVectorBridge(...)

    def add_episode_interaction(self, 
                              episode_id: str, 
                              text: str, 
                              bio_state: Dict[str, float], 
                              qualia: Optional[Dict[str, str]] = None,
                              gks_links: Optional[List[str]] = None,
                              concepts: Optional[List[str]] = None,
                              session_id: str = "UNKNOWN_SESSION",
                              trauma_flag: bool = False,
                              encoding_level: str = "L2_standard"):
        """
        Record a full interaction episode into the Knowledge Graph.
        
        Args:
            episode_id: Unique ID for the episode (e.g., EVA_EP_123456)
            text: Content of the interaction
            bio_state: Dictionary of hormones (cortisol, dopamine) AND Matrix (pleasure, arousal, dominance)
            qualia: Optional dictionary {id, name, modality, texture} for AQI
            gks_links: List of GKS Genesis Block IDs used (e.g., ['ALGO_MRF', 'CONCEPT_EMPATHY'])
            concepts: List of topics/concepts derived from text (e.g., ['Quantum Physics', 'Love'])
            session_id: Current session identifier
            trauma_flag: Boolean flag for high-impact resonance
            encoding_level: String enum (L0-L4)
        """
        try:
            # 1. Add Base Episode (with Trauma flags)
            # Use current time if not provided
            timestamp_iso = datetime.now().isoformat()
            
            self.graph.add_episode(
                episode_id=episode_id,
                text=text,
                session_id=session_id,
                timestamp=timestamp_iso,
                resonance_index=bio_state.get('arousal', 0.5), # Fallback RI
                trauma_flag=trauma_flag,
                encoding_level=encoding_level
            )

            # 2. Add Bio-State (Graph + Vector)
            bio_id = f"BIO_{episode_id}"
            self.graph.add_bio_state(bio_id, bio_state, episode_id)

            # 3. Add & Link Qualia (AQI)
            if qualia and 'id' in qualia:
                # Ensure qualia exists or merge it
                self.graph.add_qualia(
                    qualia_id=qualia['id'],
                    name=qualia.get('name', 'Unknown Qualia'),
                    modality=qualia.get('modality', 'Abstract'),
                    texture=qualia.get('texture', 'Undefined intensity')
                )
                self.graph.link_qualia(episode_id, qualia['id'])

            # 4. Link GKS (Knowledge)
            if gks_links:
                for block_id in gks_links:
                    # We assume the block exists from bootstrap or we lazily create stub?
                    # For safety, we only link if we know it should theoretically exist. 
                    # Here we just link to Genesis block generally.
                    self.graph.link_knowledge(episode_id, genesis_id=block_id)

            logger.info(f"Successfully added Episode {episode_id} to Graph (Trauma: {trauma_flag}).")
            return True

        except Exception as e:
            logger.error(f"Failed to add episode to graph: {e}")
            return False

    def retrieve_hybrid(self, query_text: str, current_bio_state: Dict[str, float], top_k: int = 5) -> Dict[str, Any]:
        """
        Perform Hybrid RAG:
        1. Semantic Search (Vector) -> Find conceptually similar episodes (Content)
        2. Bio-Resonance Search (Graph) -> Find numerically similar bio-states (Feeling)
        3. Trauma Recall -> Check for safety/continuity
        """
        results = {
            "semantic": [],
            "resonance": [],
            "trauma": [],
            "merged": []
        }
        
        # 1. Bio-Resonance (Feeling)
        # Finds memories where EVA felt the same way she feels now
        try:
            resonance_matches = self.graph.find_similar_bio_states(current_bio_state, limit=3)
            results["resonance"] = resonance_matches
            logger.info(f"Found {len(resonance_matches)} resonance matches")
        except Exception as e:
            logger.error(f"Resonance search failed: {e}")

        # 2. Trauma Recall (Safety)
        # Always check if we have deep scars related to context (Improvement: use semantic query to filter trauma)
        try:
            trauma_matches = self.graph.find_trauma_episodes(limit=2)
            results["trauma"] = trauma_matches
        except Exception as e:
            logger.error(f"Trauma search failed: {e}")

        # 3. Semantic Search (Content)
        # TODO: Integrate actual ChromaVectorBridge here. 
        # For now, we trust the Orchestrator/AgenticRAG to handle the Vector part 
        # and we focus on the Graph part. 
        # But to be a full engine, we should eventually call:
        # semantic_matches = self.vector_store.query(query_text)
        
        # 4. Merge Logic (Simple concatenation for now, Re-ranking later)
        # Prioritize Trauma > Resonance > Semantic
        seen_ids = set()
        final_list = []

        # Add Trauma first (Critical context)
        for match in results["trauma"]:
            if match['id'] not in seen_ids:
                match['source'] = 'trauma_store'
                final_list.append(match)
                seen_ids.add(match['id'])

        # Add Bio-Resonance (Affective Context)
        for match in results["resonance"]:
            eid = match['episode_id']
            if eid not in seen_ids:
                match['id'] = eid # Normalize ID key
                match['source'] = 'bio_resonance'
                final_list.append(match)
                seen_ids.add(eid)

        results["merged"] = final_list[:top_k]
        return results

    def close(self):
        self.graph.close()
