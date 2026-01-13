import sys
from pathlib import Path
import codecs

# Add root to path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from eva.memory_n_soul_passport.memory_n_soul_passport_engine import MSP
from services.agentic_rag.agentic_rag_engine import AgenticRAG

def verify_retrieval():
    print("[RETRIEVAL VERIFICATION] Testing AgenticRAG + MSP integration...")
    
    msp = MSP()
    rag = AgenticRAG(msp_client=msp)
    
    query_ctx = {
        "tags": ["test"],
        "ans_state": {"sympathetic": 0.5},
        "blood_levels": {"cortisol": 0.3}
    }
    
    print("  - Querying memories...")
    matches = rag.retrieve(query_ctx)
    
    print(f"\n[RESULT] Found {len(matches)} matches:")
    for i, m in enumerate(matches):
        print(f"  {i+1}. [{m.stream.upper()}] score: {m.score:.2f} | content: {m.content[:50]}...")
    
    if len(matches) > 0:
        print("\nVERIFICATION SUCCESS: Memories are reachable via AgenticRAG.")
    else:
        print("\n⚠️ VERIFICATION WARNING: No memories found (have you run the orchestrator yet?)")

if __name__ == "__main__":
    verify_retrieval()
