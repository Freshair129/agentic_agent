"""
EVA GraphRAG Python Client - Simple wrapper for Neo4j operations
"""

from neo4j import GraphDatabase
from typing import Dict, List, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)


class EVAGraphClient:
    """
    Simple Graph Database client for EVA 9.1.0
    Provides high-level methods for common GraphRAG operations
    """
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password=None):
        # Use env var or fall back to local dev default
        if password is None:
            password = os.environ.get("NEO4J_PASSWORD", "123456789")
            
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info(f"Connected to Neo4j at {uri}")
    
    def close(self):
        self.driver.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # === Episode Operations ===
    
    def add_episode(self, episode_id: str, text: str, session_id: str, 
                   timestamp: str, resonance_index: float = 0.0,
                   trauma_flag: bool = False, encoding_level: str = "L0_trace",
                   text_embedding: Optional[List[float]] = None) -> bool:
        """Add a new episode to the graph"""
        with self.driver.session() as session:
            result = session.run("""
                MERGE (e:EPISODE {id: $id})
                SET e.text = $text,
                    e.session_id = $session_id,
                    e.timestamp = datetime($timestamp),
                    e.resonance_index = $ri,
                    e.trauma_flag = $trauma,
                    e.encoding_level = $level,
                    e.text_embedding = $embedding
                RETURN e.id as id
            """, id=episode_id, text=text, session_id=session_id,
                timestamp=timestamp, ri=resonance_index, 
                trauma=trauma_flag, level=encoding_level,
                embedding=text_embedding)
            return result.single() is not None
    
    def add_bio_state(self, state_id: str, bio_metrics: Dict[str, float],
                     episode_id: Optional[str] = None) -> bool:
        """
        Add a bio-state snapshot (Hormones + EVA Matrix PAD)
        Expected bio_metrics keys: cortisol, dopamine, serotonin, pleasure, arousal, dominance, etc.
        """
        with self.driver.session() as session:
            # Create bio-state node
            session.run("""
                MERGE (b:BIO_STATE {id: $id})
                SET b += $metrics
            """, id=state_id, metrics=bio_metrics)
            
            # Link to episode if provided
            if episode_id:
                session.run("""
                    MATCH (e:EPISODE {id: $ep_id})
                    MATCH (b:BIO_STATE {id: $bio_id})
                    MERGE (e)-[:HAS_STATE]->(b)
                """, ep_id=episode_id, bio_id=state_id)
            return True

    # === GKS Operations (Knowledge) ===

    def add_master_block(self, block_id: str, name: str, definition: str) -> bool:
        """Add a GKS Master Block (Essence)"""
        with self.driver.session() as session:
            session.run("""
                MERGE (m:MASTER_BLOCK {id: $id})
                SET m.name = $name,
                    m.definition = $defn
            """, id=block_id, name=name, defn=definition)
            return True

    def add_genesis_block(self, block_id: str, block_type: str, content: str, 
                         derived_from_master_id: Optional[str] = None) -> bool:
        """Add a GKS Genesis Block and optionally link to Master"""
        with self.driver.session() as session:
            session.run("""
                MERGE (g:GENESIS_BLOCK {id: $id})
                SET g.type = $type,
                    g.content = $content
            """, id=block_id, type=block_type, content=content)
            
            if derived_from_master_id:
                session.run("""
                    MATCH (g:GENESIS_BLOCK {id: $gid})
                    MATCH (m:MASTER_BLOCK {id: $mid})
                    MERGE (g)-[:DERIVED_FROM]->(m)
                """, gid=block_id, mid=derived_from_master_id)
            return True

    def link_knowledge(self, episode_id: str, genesis_id: Optional[str] = None, 
                      master_id: Optional[str] = None):
        """Link an episode to the knowledge used"""
        with self.driver.session() as session:
            if genesis_id:
                session.run("""
                    MATCH (e:EPISODE {id: $eid})
                    MATCH (g:GENESIS_BLOCK {id: $gid})
                    MERGE (e)-[:APPLIED_KNOWLEDGE]->(g)
                """, eid=episode_id, gid=genesis_id)
            if master_id:
                session.run("""
                    MATCH (e:EPISODE {id: $eid})
                    MATCH (m:MASTER_BLOCK {id: $mid})
                    MERGE (e)-[:APPLIED_KNOWLEDGE]->(m)
                """, eid=episode_id, mid=master_id)

    # === AQI Operations (Qualia) ===

    def add_qualia(self, qualia_id: str, name: str, modality: str, texture: str) -> bool:
        """Add a Qualia node"""
        with self.driver.session() as session:
            session.run("""
                MERGE (q:QUALIA {id: $id})
                SET q.name = $name,
                    q.modality = $modality,
                    q.texture = $texture
            """, id=qualia_id, name=name, modality=modality, texture=texture)
            return True

    def link_qualia(self, episode_id: str, qualia_id: str):
        """Link an episode to a specific Qualia"""
        with self.driver.session() as session:
            session.run("""
                MATCH (e:EPISODE {id: $eid})
                MATCH (q:QUALIA {id: $qid})
                MERGE (e)-[:HAS_QUALIA]->(q)
            """, eid=episode_id, qid=qualia_id)
    
    # === Query Operations ===
    
    def find_episodes_by_session(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get all episodes in a session"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:EPISODE {session_id: $session_id})
                RETURN e.id as id, e.text as text, e.timestamp as timestamp
                ORDER BY e.timestamp
                LIMIT $limit
            """, session_id=session_id, limit=limit)
            return [record.data() for record in result]
    
    def find_similar_bio_states(self, target_state: Dict[str, float], 
                               threshold: float = 0.5, limit: int = 5) -> List[Dict]:
        """
        Find episodes with similar biological states using 6D Euclidean distance:
        3 Hormones (Cortisol, Dopamine, Serotonin) + 3 Matrix (Pleasure, Arousal, Dominance)
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:EPISODE)-[:HAS_STATE]->(b:BIO_STATE)
                WITH e, b,
                     abs(coalesce(b.cortisol, 0.5) - $cortisol) +
                     abs(coalesce(b.dopamine, 0.5) - $dopamine) +
                     abs(coalesce(b.serotonin, 0.5) - $serotonin) +
                     abs(coalesce(b.pleasure, 0.0) - $pleasure) +
                     abs(coalesce(b.arousal, 0.0) - $arousal) +
                     abs(coalesce(b.dominance, 0.0) - $dominance) as distance
                WHERE distance < $threshold
                RETURN e.id as episode_id,
                       e.text as text,
                       e.timestamp as timestamp,
                       b.pleasure as pleasure,
                       distance
                ORDER BY distance ASC
                LIMIT $limit
            """, 
                cortisol=target_state.get("cortisol", 0.5),
                dopamine=target_state.get("dopamine", 0.5),
                serotonin=target_state.get("serotonin", 0.5),
                pleasure=target_state.get("pleasure", 0.0),
                arousal=target_state.get("arousal", 0.0),
                dominance=target_state.get("dominance", 0.0),
                threshold=threshold * 6, # Normalize threshold for 6 dimensions
                limit=limit
            )
            return [record.data() for record in result]

    def find_trauma_episodes(self, limit: int = 3) -> List[Dict]:
        """Find recent high-impact trauma episodes"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:EPISODE)
                WHERE e.trauma_flag = true
                RETURN e.id as id,
                       e.text as text,
                       e.encoding_level as level,
                       e.timestamp as timestamp
                ORDER BY e.timestamp DESC
                LIMIT $limit
            """, limit=limit)
            return [record.data() for record in result]
    
    def find_temporal_sequence(self, concept: str, limit: int = 5) -> List[Dict]:
        """Find episodes that share a concept and occurred in sequence"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e1:EPISODE)-[:EVOKES]->(c:CONCEPT {name: $concept})
                      <-[:EVOKES]-(e2:EPISODE)
                WHERE e1.timestamp > e2.timestamp
                  AND e1.id <> e2.id
                RETURN e2.text as past_episode,
                       e1.text as current_episode,
                       c.name as shared_concept
                ORDER BY e1.timestamp DESC
                LIMIT $limit
            """, concept=concept, limit=limit)
            return [record.data() for record in result]
    
    # === Stats ===
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        with self.driver.session() as session:
            # Node counts
            node_result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
            """)
            nodes = {record["label"]: record["count"] for record in node_result}
            
            # Relationship counts
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
            """)
            relationships = {record["type"]: record["count"] for record in rel_result}
            
            return {
                "nodes": nodes,
                "relationships": relationships,
                "total_nodes": sum(nodes.values()),
                "total_relationships": sum(relationships.values())
            }


# === Example Usage ===
if __name__ == "__main__":
    # Test connection
    with EVAGraphClient() as client:
        print("Testing EVA Graph Client...")
        
        # Add sample episode
        client.add_episode(
            episode_id="EVA_EP_TEST_001",
            text="Testing GraphRAG integration",
            session_id="SES_TEST",
            timestamp="2026-01-11T20:30:00",
            resonance_index=0.75
        )
        
        # Add bio-state
        client.add_bio_state(
            state_id="BIO_TEST_001",
            hormone_levels={
                "cortisol": 0.6,
                "dopamine": 0.4,
                "serotonin": 0.5
            },
            episode_id="EVA_EP_TEST_001"
        )
        
        # Query similar states
        similar = client.find_similar_bio_states({
            "cortisol": 0.65,
            "dopamine": 0.35,
            "serotonin": 0.55
        })
        
        print(f"\nFound {len(similar)} similar bio-states:")
        for match in similar:
            print(f"  - {match['episode_id']}: Distance = {match['distance']:.3f}")
        
        # Show stats
        stats = client.get_stats()
        print(f"\nDatabase Stats:")
        print(f"  Total Nodes: {stats['total_nodes']}")
        print(f"  Total Relationships: {stats['total_relationships']}")
        print(f"  Node Types: {stats['nodes']}")
