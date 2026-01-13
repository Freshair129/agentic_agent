    def _load_core_identity_card(self, context: Dict[str, Any]) -> str:
        """
        Load Core Identity Card (Tier 1 Context) with dynamic bio-state injection.
        
        Args:
            context: Full context dict with bio-state, episode_id, etc.
        
        Returns:
            Formatted core identity markdown
        """
        # Load template
        template_path = self.base_path / "cim" / "system_contexts" / "core_identity.md"
        
        if not template_path.exists():
            # Fallback to minimal identity
            return """# EVA Core Identity
You are the Reasoning Cortex (System 2) of a bio-digital organism.
Your decisions affect physiological state. Hormone vectors are REAL."""
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Extract bio-state
        physio = context.get('physio_baseline', {})
        hormones = physio.get('hormones', {})
        vitals = physio.get('vitals', {})
        matrix = context.get('eva_matrix', {})
        
        # Format dynamic bio-state summary
        bio_state_summary = f"""### Live Physiological State
**Hormones (μg/dL)**:
- Cortisol: {hormones.get('cortisol', 0):.2f} | Dopamine: {hormones.get('dopamine', 0):.2f}
- Oxytocin: {hormones.get('oxytocin', 0):.2f} | Serotonin: {hormones.get('serotonin', 0):.2f}
- Adrenaline: {hormones.get('adrenaline', 0):.2f}

**Vitals**:
- Heart Rate: {vitals.get('heart_rate', 0):.0f} BPM | Respiration: {vitals.get('respiration_rate', 0):.1f} RPM
- Status: {physio.get('status', 'connected')}

**Matrix (9D State)**:
- Stress: {matrix.get('stress', 0):.0f}/1000 | Warmth: {matrix.get('warmth', 0):.0f}/1000
- Drive: {matrix.get('drive', 0):.0f}/1000 | Clarity: {matrix.get('clarity', 0):.0f}/1000
- Joy: {matrix.get('joy', 0):.0f}/1000
"""
        
        # Replace placeholders
        identity_card = template.replace("{{DYNAMIC_BIO_STATE}}", bio_state_summary)
        identity_card = identity_card.replace("{{EPISODE_ID}}", self._get_current_episode_id())
        identity_card = identity_card.replace("{{TURN_INDEX}}", str(context.get('turn_index', 0)))
        identity_card = identity_card.replace("{{SESSION_ID}}", context.get('session_id', 'unknown'))
        
        # Speaker info (from User Registry)
        identity_card = identity_card.replace("{{ACTIVE_USERNAME}}", context.get('active_username', 'User'))
        identity_card = identity_card.replace("{{USER_ID}}", context.get('active_user_id', 'unknown'))
        
        return identity_card
