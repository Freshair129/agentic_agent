"""
VitalsEngine
Version: v1.0

Role:
- Calculate Heart Rate (BPM) and Respiration Rate (RPM)
- Implement Respiratory Sinus Arrhythmia (RSA) coupling
- Simulate breathing phase (sinusoidal)
"""

import math
import random

class VitalsEngine:
    def __init__(self, config: dict = None):
        self.cfg = config or {}
        
        # Internal states
        self.bpm = 70.0
        self.rpm = 14.0
        self.breath_phase = 0.0 # 0.0 to 2*PI
        
        # Coherence tracking (for Vagus Feedback)
        self.vagus_tone = 0.5
        
        # Baselines
        self.base_hr = 65.0
        self.base_rr = 12.0

    def step(self, ans_state: dict, adrenaline_level: float, dt: float) -> dict:
        """
        Calculate vitals based on Autonomic state and Hormones.
        """
        symp = ans_state.get("sympathetic", 0.5)
        para = ans_state.get("parasympathetic", 0.5)
        
        # 1. Calculate Target Rates
        # Adrenaline provides a direct multiplier boost to HR/RR
        # We assume 100 pg/mL is a "baseline" for adrenaline in this context
        adr_boost = max(0, (adrenaline_level / 150.0)) 
        
        # Heart Rate Model
        # Range: ~50 (Deep Calm) to ~180 (Panic/Exertion)
        target_bpm = self.base_hr + (symp * 80) - (para * 20) + (adr_boost * 40)
        
        # Respiration Model
        # Range: ~8 to ~40 RPM
        target_rpm = self.base_rr + (symp * 20) - (para * 4) + (adr_boost * 10)
        
        # 2. Smooth Transition (Metabolic Inertia)
        alpha = 0.05 # Adjust for responsiveness
        self.bpm = (alpha * target_bpm) + ((1 - alpha) * self.bpm)
        self.rpm = (alpha * target_rpm) + ((1 - alpha) * self.rpm)
        
        # 3. Breathing Cycle (Phase)
        # 1 RPM = 1 cycle per 60s = speed of 2*PI / 60 radians per sec
        phase_speed = (self.rpm * 2 * math.pi) / 60.0
        self.breath_phase = (self.breath_phase + phase_speed * dt) % (2 * math.pi)
        
        # 4. RSA (Respiratory Sinus Arrhythmia)
        # Heart Rate increases slightly during inhalation (first half of phase)
        # and decreases during exhalation.
        rsa_amplitude = 5.0 * (1.0 - symp) + 2.0 # More RSA when calm (para dominance)
        rsa_offset = math.sin(self.breath_phase) * rsa_amplitude
        
        # Final display values
        display_bpm = self.bpm + rsa_offset
        display_rpm = self.rpm
        
        # 5. Calculate Vagus Tone (Feedback Signal)
        # Vagus tone is high when breathing is slow AND BPM is relatively low/stable
        # This is a simplified proxy for HRV-based vagal modulation
        raw_vagus = (1.0 - (self.rpm / 40.0)) * (1.0 + (para * 0.5))
        self.vagus_tone = max(0, min(1.0, raw_vagus))
        
        return {
            "bpm": round(display_bpm, 1),
            "rpm": round(display_rpm, 1),
            "vagus_tone": self.vagus_tone,
            "breath_phase": self.breath_phase,
            "hrv_index": rsa_amplitude / 10.0 # Proxy for variability
        }
