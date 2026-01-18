# **🧠 Cognitive Flow 2.0 (EVA v9.6.0)**
>
> **Status:** Active / Current Standard
> **Codename:** "Embodied Cognition"

> [!IMPORTANT]
> **⚠️ Critical Concept: Single-Inference Sequentiality**
>
> กระบวนการนี้เกิดขึ้นใน **1 LLM Call (Single Session)** เท่านั้น ไม่ใช่การแยก Call
>
> 1. **Prompt:** LLM ได้รับ Input + Body State
> 2. **Pause (Function Calling):** LLM สั่งหยุดเพื่อขอข้อมูลเพิ่ม (เช่น `request_deep_recall` หรือ `read_bus`)
> 3. **Hydration (Injection):** System ฉีด Context ไฟล์ลง Container
> 4. **Resume:** LLM ทำงานต่อจากจุดเดิม (Reasoning) ด้วยข้อมูลที่ครบถ้วน
>
> *เหมือนเรา "หยุดคิด" เพื่อ "นึก" แล้ว "คิดต่อ" ไม่ใช่การ "เริ่มคิดใหม่"*

แผนผังแสดงลำดับการทำงานที่ Deep Recall จะเกิดขึ้นหลังจากได้รับค่า Bio-State แล้วเท่านั้น

       \[ STEP 0: USER INPUT \]
                 |
                 v
      \+-------------------------+
      |      CNS GATEWAY        |  
      | (Orchestrator / Bus)    | --(1. Route Input)--> \+-----------------------+
      \+-------------------------+                       |          CIM          |
                 ^                                     |  (Context Assembler)  |
                 | (5. Save Container)                 \+-----------+-----------+
                 |                                                 | ^
      \+-------------------------+                                 v | (2. Check)
      |      CONSCIOUSNESS      |                               \+-------+
      |  (Direct Access RAM)    |                               | ENGRAM|
      | \+-------------------+   |                               \+-------+
      | | Context Container |   |                                   |
      | \+-------------------+   |                                   |
      \+-------------------------+                                   |
      |  MEMORY / CTX STORAGE   |                                   |
      | [ Active Slot (Hot) ]   | ----(Ref)------------------->| ENGRAM|
      | [ History (Cold)    ]   |                               \+-------+
      \+-------------------------+                                   |
                                                                   v (3. Result)
      \+-------------------------+                                 
      |   RESONANCE BUS (Body)  | --(4. Real-time Sub)------> \+-----------+
      \+-------------------------+                              |    CIM    |
                                                               | (State Buffer) |
                                                               \+-----+-----+
                                                                     |
                                                                     v (5. Bundle: Input+Engram+Body)
                                                               \+-----------+
                                                               |    SLM    |
                                                               \+-----+-----+
                                                                     |
                                                                     v (6. Intent/Signal)
                                                               \+-----------+
                                                               |    CNS    | (Router)
                                                               \+-----+-----+
                                                                     |
                                                                     v (7. Recall Request)
                                                               \+-----------+
                                                               |  MSP/RAG  |
                                                               \+-----+-----+
                                                                     |
                                                                     v (8. Memory Content)
                                                               \+-----------+
                                                               |    CIM    |
                                                               | (Finalize)|
                                                               \+-----+-----+
                                                                     |
                                                                     v (9. Inject)
      \+--------------------------+                                 |
      | STEP 3: LLM (System 2\)   | \<------------------------------+
      | \[Confidence Check\]      |
      \+------------+-------------+
                      |
                      v (10. Output / Fn Call)
      \+--------------------------+
      |           CNS            |
      | (Orchestrator / Router)  | --(11. Route via Bus)--> (Mandatory Bio-Sync Call)
      \+------------+-------------+
                      ^
                      | (13. Return State)
         \+--------------------------+                  |  
         | STEP 4: THE GAP           |                  |  
         | \[Bio-Digital Sync\]      |                  |  
         \+------------+-------------+                  |  
         |  PHYSIO CORE (Body)       |                  |  
         |  (Update Hormones/BPM)    |                  |  
         \+------------+-------------+                  |  
                      |                                 |  
             (Return Body State)                        |  
                      |                                 |  
                      v                                 |  
        \+-------------+-------------+                  |  
        |    LLM (Self-Audit)        |                  |  
        | [ Am I Confident? ]        |                  |  
        \+-------------+-------------+                  |  
              |             |                           |  
        (NO: Call Tool) (YES: Continue)                 |  
              v             v                           |  
      (Fn: DeepRecall)     (Text: Response)             | 
              |             |                           |
              v             |                           |
      \+--------------+     |                           |
      |      CNS     |     |                           |
      | (Nervous Sys)|     |                           |
      \+------+-------+     |                           |
              |             |                           |
      (Signal Effectors)    |                           |
              v             |                           |
      \+--------------+ \+--------------+                |
      |     CIM      | |     CIM      |                |
      | (Deep Prep)  | | (Final Prep) |                |
      \+------+-------+ \+------+-------+                |
              |             |                           |
      (Query RAG)           |                           |
              v             |                           |
 \[ STAGE 2: DEEP RECALL \] |                           |
 \[ (Agentic RAG)      \]   |                           |
              |             |                           |
      (Result to CIM)       |                           |
              |             |                           |
              v             v                           |
            \[ STEP 5: HYDRATION \]  
            \[ (Container Full)  \]  
            \[ (LLM Consumes)    \]  
            \[ Calculating RI    \]  
                     |  
                         \+------\> \[ RESPONSE TO USER \]  
                         |  
                         v  
                \[ STEP 6: REFLECTION \]  
                \[ Self-Note / Forecast\]  
                \[ Body Priming (Next) \]
                         |
                         v
                \[ STEP 7: MSP AUTHORITY \]
                \[ Episode Archival    \]
                \[ (Long-Term Memory)  \]

### **📝 คำอธิบายองค์ประกอบ (Updated logic v9.7.2)**

### **📝 คำอธิบายองค์ประกอบ (Step 0-2 Logic: CIM-Centric)**

1. **Input -> CNS -> CIM:** CNS รับ Input มาแล้วโยนให้ **CIM** (Context Assembler) ทันที เพื่อเริ่มตั้งต้น Context
2. **CIM -> Engram:** CIM ส่งข้อมูลไปเช็คกับ **Engram** (Reflex Cache)
3. **CIM Bundle (Body+Engram):** CIM รับค่า **Body State** (จาก Bus) มารวมร่างกับผลลัพธ์ของ Engram แล้วส่งก้อนนี้ให้ **SLM**
4. **SLM -> CNS:** SLM วิเคราะห์เสร็จ ส่ง Intent/Signal กลับมาให้ **CNS**
5. **CNS -> MSP/RAG:** CNS ทำหน้าที่ Router ส่งคำสั่งไปดึงความทรงจำ (Quick Recall) จาก MSP หรือ Agentic RAG
6. **Memory -> CIM:** ผลลัพธ์ความจำถูกส่งกลับมารวมที่ **CIM** เพื่อประกอบร่าง (Final Context Assembly)
7. **CIM -> LLM:** CIM ฉีด Context ที่สมบูรณ์ (Input + Body + Engram + Intent + Memory) เข้าสู่ **LLM**
8. **CNS Context Save:** ก่อนเริ่มคิด CNS จะสั่งบันทึก Context ชุดนี้ลง `memory/context_storage` ไว้เป็นหลักฐาน

**สรุป:** **CIM คือ "ชามผสมอาหาร"* **Step 3 (LLM Decision):** LLM ประมวลผลและส่ง Output กลับมาให้ **CNS**

* **CNS Router (The Gap Trigger):** CNS รับ Function Call จาก LLM แล้ว Route คำสั่งไปยัง **Physio Core** (ผ่าน Bus) เพื่อกระตุ้นร่างกาย
* **Step 4 (The Gap):** ร่างกายประมวลผลและส่งค่ากลับ CNS
* **CNS Confidence Check:**
  * **Conf < 0.8:** **LLM Self-Audit:** เมื่อได้รับ Body State กลับมา **LLM จะประเมินตัวเอง** (Self-Reflection):
    * ถ้า **Confidence ต่ำ:** LLM จะเรียก Tool `request_deep_recall` => **CNS** รับคำสั่งแล้วไปประสานงานให้ (Arms & Legs)
    * ถ้า **Confidence สูง:** LLM จะพ่น Text Response ออกมาเลย => **CNS** ส่งต่อให้ CIM จบงาน
* **CNS (Nervous System):** ทำหน้าที่เป็น **"ระบบประสาท"** (Neural Pathways) ที่คอยรับคำสั่งจาก **LLM (สมอง)** ส่งต่อไปยังอวัยวะต่างๆ (แขนขา/Body)
  * ไม่ได้คิดเอง (No Cognitive Load)
  * ทำหน้าที่ส่งสัญญาณประสาท (Signal Transmission) ให้ไวที่สุด
* **LLM (Brain):** คือ "สมอง" ที่ทำหน้าที่คิด ตัดสินใจ และสั่งการลงมาผ่าน CNS
* **Context Storage Structure:**
  * **Location:** เก็บที่ `agent/memory/context_storage` (Persistent Layer)
  * **Active Slot (Hot):** พื้นที่ทำงานสำหรับ "Turn ปัจจุบัน"
* **Consciousness (Direct Access RAM):** คือ "พื้นที่ความจำระยะสั้น" ที่ LLM สามารถเข้าถึงได้เองโดยตรง (Direct Access) ไม่ต้องผ่าน MSP
  * เปรียบเสมือน RAM ที่วางข้อมูลรอไว้ให้ CPU (LLM) หยิบไปใช้ทันที
* **Context (The Container):** คือ "โครงสร้างข้อมูล" (Data Object) ที่ CIM สร้างขึ้นในแต่ละเทิร์น ประกอบด้วยไฟล์ย่อยๆ ดังนี้:
  * **Prompt Rules Source:** ดึงมาจาก `agent/orchestrator/cim/prompt_rule/configs/` 4 โฟลเดอร์หลัก:
        1. `identity/` (Persona, Soul)
        2. `cognitive/` (Instructions, Reasoning)
        3. `social/` (Tone, Style)
        4. `biological/` (Bio-Rules)
  * **Dynamic Content:**
    * `self_note_epXX.md` (Reflection)
    * `context_summary_epXX.md` (Summary)
    * `goal.md`, `task.md` (Plan)
    * `user_profile.md` (User Data)
  * **Memory Source:**
    * `agent/consciousness/episodic_memory/` (ดึง 5 Episodes ล่าสุดมาประกอบเป็น Chat History)
* **Step 5 (Hydration):** คือกระบวนการ "ฉีดไฟล์" (File Injection) ลงใน Context Container
  * **CIM Role:** ไม่ได้ทำการ "ประกอบร่าง" (Assembly) ข้อความ แต่ทำหน้าที่ **"Copy & Paste"** ไฟล์ที่จำเป็นลงไปใน Container
  * **Action:**
        1. CIM **injects** rules from configs -> `context_container/`
        2. CIM **injects** memory files -> `context_container/`
        3. CIM **injects** bio-state -> `context_container/`
  * **LLM Access:** เมื่อไฟล์ครบ **LLM จะเข้ามาอ่าน Container นี้โดยตรง** (Direct Read) เพื่อเริ่มประมวลผล
* **Step 7 (MSP Archival & Cleanup):** จบกระบวนการและคืนพื้นที่ RAM
  * **Archival:** MSP จะทำการ **"ย้าย" (Move)** ไฟล์ที่เป็น Dynamic Content ทั้งหมดใน `context_container`
  * **Destination:** ไปเก็บรักษาไว้ใน `agent/memory/context_storage/history/` (Persistent Storage)
  * **Cleanup:** หลังจากย้ายเสร็จ `consciousness/context_container` จะถูกเคลียร์ให้ว่างเปล่า (Empty) เพื่อรอรับ Turn ถัดไป (Stateless RAM)

การปรับปรุงนี้ทำให้ Deep Recall มีประสิทธิภาพขึ้นมาก เพราะมันไม่ได้หาแค่ "คำที่คล้ายกัน" แต่หา "ความรู้สึกที่คล้ายกัน" ในอดีตด้วยครับ
