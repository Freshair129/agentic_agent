## 2. 5+2+2 Dimensional Model (`TransitionNode.py`)

The Matrix state is calculated using three distinct layers of abstraction:

### A. 5 Core Affective Axes
- **Axes**: Stress, Warmth, Drive, Clarity, Joy.
- **Math**: $V_{new} = (I_{raw} \times L) + (V_{prev} \times I)$
    - $I_{raw}$: Raw influence (Positive factors - Negative factors).
    - $L$: Learning Rate (0.3).
    - $I$: State Inertia (0.7).
- **Result**: Smooth transitions that simulate emotional momentum.

### 2.1 Node Spec: `TransitionNode`
- **Primary Method**:
    - `calculate_transition(current_axes, current_momentum, signals)`: Pure logic provider.
- **Axis Logic (Verified)**:
    - **Stability**: `0.5 + (GABA - Adrenaline)`.
    - **Orientation**: `0.5 + (Oxytocin - Cortisol)`.
    - **Momentum Decay**: `1.0 - 0.15` (85% persistence per step).
- **Categorization**: Uses `eval()` on `emotion_categories` config to determine human labels like "Calm" or "Panicked".

### B. 2 Meta-Directional Axes
- **Stability**: Calculated as $0.5 + (GABA - Adrenaline)$. Reaches $1.0$ under calm states and $0.0$ under panic.
- **Orientation**: Calculated as $0.5 + (Oxytocin - Cortisol)$. Represents the biological bias toward social connection vs. self-preservation.

### C. 2 Categorical Axes (Pointers)
- **Primary/Secondary**: Identifies the top two dominant affective axes to simplify state-labeling for the LLM.

## 3. Emotion Labeling & Momentum
- **Momentum Intensity**: A scalar tracking how "energized" the emotional state is, decaying over time.
- **Reflex Directives**: Urgency signals ($0.8$ or $0.2$) triggered when Stress exceeds a high-arousal threshold ($0.85$).

## 4. Code Mapping
- `matrix_psych_module.py`: The functional integrator that connects the Matrix system to its nodes.
- `transition_node.py`: The pure logic provider for the 9-dimensional state space.

## 5. Component Inventory (Absolute Coefficients)
These internal components drive the 5+2+2 dynamical system in `transition_node.py`:

| Component | Key | Value | Description |
| :--- | :--- | :--- | :--- |
| **State Inertia** | `inertia` | 0.7 | Resistance to state change (momentum). |
| **Learning Rate** | `learning_rate` | 0.3 | Sensitivity to incoming signals. |
| **Momentum Decay** | `decay` | 0.15 | Rate at which emotional intensity fades. |
| **Reflex Threshold** | `high_stress` | 0.85 | Threshold for triggering concise urgency. |
| **Meta-Offset** | `offset` | 0.5 | Neutral baseline for binary orientations. |
