## 2. Glandular Dynamics (`glands.py`)
- **Hill-Langmuir Response**: Maps drive level to secretion intensity using a sigmoidal Hill function ($n=3.0, k=2.5$).
- **Adaptation & Fatigue**: Glands lose efficiency under prolonged high drive and require a refill rate for their hormone inventory.
- **Basal Production**: Every gland maintains a homeostatic baseline with +/- 10% physiological jitter.
- **Vagus Inhibition**: External inhibition factor (up to 90%) can suppress secretion, simulating parasympathetic feedback.

### 2.1 Node Spec: `EndocrineGland`
- **Primary Methods**:
    - `trigger_nerve_surge(stimulus_intensity)`: Releases up to 40% of inventory instantly.
    - `process_step(stimulus, dt, inhibition)`: Calculates basal + stimulated output using Hill function.
- **State Keys**: `inventory` (pg), `adaptation` (0-1), `drive` (scalar), `last_flux_pg`.
- **Logic**: Total release is capped by `inventory` and adjusted by `adaptation` (fatigue factor).

## 3. HPA Axis Logic (`HPARegulator.py`)
- **Three-Stage Cascade**: Hypothalamus (CRH) → Pituitary (ACTH) → Adrenal (Cortisol).
- **Temporal Smoothing**: Uses Exponential Moving Average (EMA) to simulate biological latency in hormone production.
- **Negative Feedback**: High plasma Cortisol levels trigger a sigmoid-based inhibition of the HPA drive, preventing runaway stress.

### 3.1 Node Spec: `HPARegulator`
- **Primary Method**:
    - `step(stress_inputs, plasma_snapshot, dt)`: Orchestrates the 3-tier cascade.
- **Internal States**: `_crh`, `_acth` (virtual hormone vectors).
- **Core Math**:
    - `_ema(target)`: $(0.05 \times target) + (0.95 \times previous)$.
    - `inhibition`: `sigmoid((plasma_COR - threshold) * 5.0)`.

## 4. Code Mapping
- `EndocrineController.py`: The orchestrator that manages gland states and executes the 30Hz step logic.
- `HPARegulator.py`: The non-mutating regulator that calculates the targeted Adrenal drive for Cortisol.
- `glands.py`: The biological unit model representing individual endocrine organs.

## 5. Component Inventory (Absolute Coefficients)
For formal audit/verification purposes, the following coefficients are hardcoded in `constants.py` and `glands.py`:

| Component | Key | Value | Source |
| :--- | :--- | :--- | :--- |
| **Fatigue Threshold** | `FATIGUE_THRESHOLD_PCT` | 0.15 | `constants.py` |
| **Exhausted Threshold** | `EXHAUSTED_THRESHOLD_PCT` | 0.01 | `constants.py` |
| **Adaptation Range** | `ADAPTATION_MIN/MAX` | 0.1 - 1.0 | `constants.py` |
| **Drive Bounds** | `DRIVE_MIN/MAX` | 0.0 - 10.0 | `constants.py` |
| **Hill Midpoint (K)** | `HILL_K` | 2.5 | `glands.py` |
| **Hill Slope (n)** | `HILL_N` | 3.0 | `glands.py` |
| **HPA Feedback** | `FB_STRENGTH` | 0.7 | `HPARegulator.py` |
