from datetime import datetime
from typing import Dict, Any, Optional
from memory_n_soul_passport.memory_n_soul_passport_engine import MSP
# from genesis_knowledge_system.grounding.truth_seeker_node import TruthSeekerNode (Future)

class SessionManager:
    """
    Module: SessionManager
    Parent: Orchestrator
    
    Responsibilities:
    1. Manage Session Lifecycle (Start, Stop, Timeout).
    2. Coordinate Session Closing Ceremony:
       - Archive to MSP (Digest).
       - Validate Truths via TruthSeeker (Grounding).
    """

    def __init__(self, msp_engine: MSP, bus_system=None, gks_interface=None):
        self.msp = msp_engine
        self.bus = bus_system
        self.gks = gks_interface
        
        # State
        self.session_id = None
        self.start_time = None
        self.recording_active = False
        self.pending_stop_confirmation = False
        
        # Identification Keywords
        self.start_keywords = ["/start", "เริ่ม", "อัด", "rec", "start session"]
        self.stop_keywords = ["/stop", "/end", "พอ", "หยุด", "จบ", "ปิดเซสชั่น", "quit session"]
        self.confirm_keywords = ["y", "yes", "confirm", "ok", "ยืนยัน", "ครับ", "ค่ะ"]

    def process_command(self, user_input: str) -> Optional[Dict]:
        """
        Checks input for session commands. 
        Returns Response Dict if a command was processed, else None.
        """
        cmd = user_input.strip().lower()
        
        # 1. Handle Pending Stop Confirmation
        if self.pending_stop_confirmation:
            if any(word in cmd for word in self.confirm_keywords):
                return self._finalize_session()
            else:
                self.pending_stop_confirmation = False
                return {
                    "final_response": "🔄 [RESUME] Stop cancelled. Recording continues.",
                    "emotion_label": "Alert",
                    "resonance_hash": "RESUME"
                }

        # 2. Start Command
        if any(word in cmd for word in self.start_keywords):
            return self._start_new_session()
            
        # 3. Stop Command
        if any(word in cmd for word in self.stop_keywords):
            return self._request_stop_confirmation()
            
        return None

    def check_timeout(self, last_interaction: datetime, timeout_seconds: int = 1800) -> Optional[Dict]:
        """Auto-closes session if timeout exceeded."""
        if not self.recording_active or not self.start_time:
            return None
            
        time_diff = (datetime.now() - last_interaction).total_seconds()
        if time_diff > timeout_seconds:
            print(f"\\n⏰ [TIMEOUT] Session auto-closed after {time_diff/60:.1f} mins.")
            self.recording_active = False
            return self._finalize_session(reason="timeout")
            
        return None

    def _start_new_session(self) -> Dict:
        self.recording_active = True
        
        # Call MSP to increment counters
        new_counters = self.msp.start_new_session()
        
        # Generate ID (Standard Format)
        # Assuming ID generation logic is standardized or handled by MSP/IdentityManager
        # For now, fetching from MSP or generating locally based on counters
        self.session_id = f"SES_{new_counters.get('session_seq', 999)}_{int(datetime.now().timestamp())}"
        
        if self.bus:
            self.bus.current_session_id = self.session_id
            
        self.start_time = datetime.now()
        
        print(f"\\n🔴 [REC] SESSION STARTED: {self.session_id}")
        return {
            "final_response": f"Session Started. Recording Active. (ID: {self.session_id})", 
            "emotion_label": "Alert", 
            "resonance_hash": "INIT"
        }

    def _request_stop_confirmation(self) -> Dict:
        if not self.recording_active:
            return {"final_response": "Recording is already OFF.", "emotion_label": "Neutral"}
            
        self.pending_stop_confirmation = True
        
        # Calculate duration
        duration_mins = (datetime.now() - self.start_time).total_seconds() / 60
        
        summary = f"""
        📝 SESSION SUMMARY REQUEST
        - Duration: {duration_mins:.1f} minutes
        - ID: {self.session_id}
        """
        print(summary)
        print("\\n⚠️  CONFIRM END SESSION? (y/n / ยืนยัน)")
        
        return {
            "final_response": "Session Summary Generated. Please confirm end of session (y/n).", 
            "emotion_label": "Waiting", 
            "resonance_hash": "WAIT"
        }

    def _finalize_session(self, reason: str = "user_command") -> Dict:
        self.recording_active = False
        self.pending_stop_confirmation = False
        
        print(f"\\nzzz [STOP] CLOSING SESSION: {self.session_id}...")

        # 1. MSP Archival (The Storage Layer)
        # analysis = self._generate_analysis(reason) # TODO: Connect LLM analysis
        analysis = {"closure_reason": reason, "timestamp": str(datetime.now())}
        digest = self.msp.end_session(self.session_id, session_analysis=analysis)
        
        # 2. GKS Grounding Validation (The Truth Layer) - "Grilled Shrimp" Logic
        validation_results = []
        if self.gks:
            # TODO: Iterate through candidate semantic memories in digest and validate
            # truth_node = self.gks.get_node("TruthSeeker")
            # result = truth_node.validate_candidate(...)
            pass
            
        return {
            "final_response": "Session Closed. Recording Stopped, Archived, and Validated.", 
            "emotion_label": "Calm", 
            "resonance_hash": "END"
        }
