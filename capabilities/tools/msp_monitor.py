from typing import Dict, List, Any
from datetime import datetime

class MSPDataMonitor:
    """
    Monitors MSP data flow for gaps.
    Detects missing fields in bio-cognitive states before persistence.
    """

    def __init__(self):
        self.gap_log = []

    def check_state_completeness(self, state: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Check if state has all expected fields.
        Returns dict of missing fields by category.
        """
        gaps = {
            "physio": [],
            "matrix": [],
            "qualia": [],
            "rms": []
        }

        # Check PhysioCore
        if "physio_state" in state:
            physio = state.get("physio_state", {})
            # Soft check for data, might be in 'data' wrapper if cached
            if isinstance(physio, dict) and "data" in physio:
                 physio = physio["data"]
            
            if "vitals" not in physio:
                gaps["physio"].append("vitals")
            if "receptor_signals" not in physio:
                gaps["physio"].append("receptor_signals")

        # Check EVA Matrix
        if "matrix_state" in state:
            matrix = state.get("matrix_state", {})
            if isinstance(matrix, dict) and "data" in matrix:
                 matrix = matrix["data"]
                 
            if "momentum" not in matrix:
                gaps["matrix"].append("momentum")

        # Check Artifact Qualia
        if "qualia_state" in state:
            qualia = state.get("qualia_state", {})
            if isinstance(qualia, dict) and "data" in qualia:
                 qualia = qualia["data"]
                 
            if "depth" not in qualia:
                gaps["qualia"].append("depth")
            if "texture" not in qualia:
                gaps["qualia"].append("texture")

        # Log gaps if significant (ignore empty categories)
        significant_gaps = {k: v for k, v in gaps.items() if v}
        
        if significant_gaps:
            self.gap_log.append({
                "timestamp": datetime.now().isoformat(),
                "gaps": significant_gaps
            })
            return significant_gaps

        return {}

    def get_gap_report(self) -> Dict[str, Any]:
        """Generate gap statistics"""
        if not self.gap_log:
            return {"status": "healthy", "gaps": 0}

        # Count gap occurrences
        gap_counts = {}
        for log_entry in self.gap_log:
            for category, fields in log_entry["gaps"].items():
                for field in fields:
                    key = f"{category}.{field}"
                    gap_counts[key] = gap_counts.get(key, 0) + 1

        return {
            "status": "gaps_detected",
            "total_checks": len(self.gap_log),
            "gap_counts": gap_counts,
            "most_common_gap": max(gap_counts.items(), key=lambda x: x[1]) if gap_counts else None
        }
