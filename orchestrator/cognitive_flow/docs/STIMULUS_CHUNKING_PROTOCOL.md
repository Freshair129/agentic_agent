# Stimulus Chunking Protocol v2.0 (Multi-Stage Injection)

**Component ID:** `PROTO-CHUNK-2.0` | **Status:** Canonical / v9.6.2
**Parent Standard:** [Cognitive Flow 2.0](Cognitive_Flow_2_0.md)

> [!IMPORTANT]
> **Why Chunking?**
> Humans do not process a long sentence as a single emotional blob. We process it sequentially.
>
> * "I love you..." -> (Dopamine Spike)
> * "...but I'm leaving." -> (Cortisol Shock)
> Flattening this into one vector ({0.5 Valence}) destroys the context. Chunking preserves the **Emotional Journey**.

## 1. The Protocol (v9.6.2 Update)

In **Cognitive Flow 2.0**, the **LLM** (System 2) is responsible for generating these chunks during the **Bio-Digital Sync** (The Gap).

1. **Reflex/Perception:** SLM provides raw intent/sentiment.
2. **Reasoning (LLM):** The LLM analyzes the user's input complexity.
3. **Generation:** The LLM constructs a `list[Stimulus]` payload for the `sync_bio_state` tool.
4. **Embodiment:** The `PhysioCore` digests this list sequentially.

### Structure (Schema)

Each chunk in the list passed to `sync_bio_state` must adhere to:

```json
{
  "sequence_id": 1,       // Order of digestion
  "valence": 0.1,         // 0.0 (Negative) to 1.0 (Positive)
  "arousal": 0.9,         // 0.0 (Calm) to 1.0 (Excited)
  "intensity": 0.8,       // Magnitude of impact
  "stress": 0.7,          // 0.0 (Safe) to 1.0 (Threat)
  "salience_anchor": "...but I'm leaving", // The specific text trigger
  "tags": ["breakup", "betrayal"]          // Memory search tags
}
```

## 2. Digestive Logic (The Loop)

Located in `eva/physio_core/physio_core.py`: `step()`

The `PhysioCore` iterates through the list sequentially, treating each chunk as a separate "Second of Experience". This digestion occurs on top of the **Continuous Background Metabolism**, which handles hormone decay and vitals fluctuations.

```python
# Sequential Digestion Logic
# Located in physio_core.py

if isinstance(llm_stimuli, list):
    for chunk in llm_stimuli:
         # Recursive call for single chunk
         # Each chunk is processed as a full biological tick (dt=1s)
         self._run_tick(chunk, dt=1.0)
```

## 3. Impact on Response

By the time the `sync_bio_state` function returns, the system state reflects the **Final Emotional Destination**, but the Internal History (Matrix State) captures the **Entire Trajectory**, allowing the LLM to "feel" the rollercoaster it just experienced.

---

## 5. Stimulus Chunking Protocol (ภาษาไทย)

**Component ID:** `PROTO-CHUNK-9.6` | **สถานะ:** ใช้งานจริง (Cognitive Flow 2.0)

**LLM** เป็นผู้รับผิดชอบในการหั่นข้อความดิบออกเป็น **รายการของ Stimulus Chunks** และส่งผ่าน Function Call `sync_bio_state` เพื่อให้ `PhysioCore` ทยอยกินทีละคำ

หลักการนี้ทำให้ร่างกายเกิด "การเดินทางของอารมณ์" (Emotional Journey) ที่สมจริง ไม่ใช่แค่รับค่าเฉลี่ยทางอารมณ์เพียงค่าเดียว
