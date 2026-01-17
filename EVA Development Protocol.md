# **📜 EVA v9.5 Development Protocol (The GSD Standard)**

**Codename:** Resonance GSD  
**Source of Truth:** [https://github.com/Cars-10/get-shit-done-gemini](https://github.com/Cars-10/get-shit-done-gemini)  
**Status:** Mandatory for Active Development  

---

## **🔥 1. The GSD Core Philosophy**

**"Existence is not Implementation."**  
Just because a file exists doesn't mean it works. Just because it imports doesn't mean it flows.

1. **Context is Currency:** ห้าม Context Dump. โหลดเฉพาะที่ใช้. ล้างเมื่อจบ Phase.
2. **Verify First:** สร้าง Test/Verification Script *ก่อน* หรือ *พร้อม* การเขียนโค้ดเสมอ
3. **No Enterprise Bloat:** **BAN** `AbstractFactory`, `ProxyPattern`, หรือ Interface ที่ไม่ได้ใช้จริง (YAGNI).
4. **Functional Reality:** โฟกัสที่ "การทำงานได้จริง" (Wiring) มากกว่า "โครงสร้างที่สวยงาม" (Structure).

---

## **2. The Workflow (XML Plan Protocol)**

เราเลิกใช้ `Implementation Plan` แบบความเรียงยาวๆ เปลี่ยนมาใช้ **Executable XML Plan** แทน:

### **Phase 1: <plan>**

สร้างไฟล์ `PLAN.md` (หรือใส่ใน Artifact) ด้วยโครงสร้างนี้:

```xml
<plan>
    <goal>
        Integrated WebUI with WebSocket Streaming
    </goal>
    <context>
        <file>agent/api/main.py</file>
        <file>agent/orchestrator.py</file>
    </context>
    <tasks>
        <task id="1">
            <description>Create verification script for WebSocket connection</description>
            <validation>Run scripts/verify_ws.py -> Expect "Connected"</validation>
        </task>
        <task id="2">
            <description>Implement WebSocket endpoint in API</description>
            <validation>Manual Test via Postman/Browser</validation>
        </task>
    </tasks>
</plan>
```

### **Phase 2: <execute>**

ทำงานทีละ `<task>` แบบ Atomic:

1. **เขียน Verification Script** (ถ้ายังไม่มี)
2. **เขียน Implement Code**
3. **รัน Verification**

### **Phase 3: <verify>**

ถ้าผ่าน -> Commit/Tick Checkbox -> Next Task.
ถ้าไม่ผ่าน -> Debug -> Retry.

---

## **3. Code Standards (Real GSD)**

| Pattern | Status | Reason |
| :--- | :--- | :--- |
| **Fat Interface files** | 🚫 **BANNED** | ไม่จำเป็นต้องสร้าง `IContract.py` แยก ถ้ามีแค่ 1 Implementation |
| **ABC (Abstract Base Classes)** | ⚠️ **CAUTION** | ใช้เฉพาะเมื่อมี >= 2 Implementations ที่ต้องสลับกันจริงๆ (Polymorphism) |
| **Type Hinting** | ✅ **MANDATORY** | ใช้ Type Hinting (`Callable`, `Protocol`) แทน Interface Class |
| **Functional Composition** | ✅ **PREFERRED** | ใช้ Function/Closure แทน Class ที่มีแค่ method เดียว |

---

---

## **4. GSD x Hierarchy Matrix (The Reconciliation)**

ความกังวลว่า "GSD จะขัดกับ System/Module/Node ไหม?" คำตอบคือ **"ไม่ขัด ถ้าใช้ถูกที่"**
เราจะใช้ GSD เพื่อตัด "ไขมัน" (Unnecessary Abstraction) แต่ยังคง "กระดูก" (Structural Integrity) ไว้:

| Hierarchy Level | GSD Rule | Example |
| :--- | :--- | :--- |
| **System** (Organs) | **Strict Structure** | ไฟล์ `_engine.py` ต้องมี Schema ชัดเจน แต่ไม่จำเป็นต้องมี `ISystem` Interface ถ้ามีแค่ 1 Implementation |
| **Module** (Integrator) | **Functional Wiring** | เน้นการเชื่อมต่อ (Logistics) ห้ามมี Complex Logic ฝังอยู่ |
| **Node** (Logic) | **Pure GSD** | เขียน Logic ดิบๆ ได้เลย ไม่ต้องสร้าง Class ถ้า Function ก็พอ (Functional Composition) |
| **Contract** | **On-Demand** | สร้าง `contracts/` เฉพาะเมื่อ Code ถูกใช้ข้าม System (Public API only) |

---

## **5. Directory & Context Rules**

* **Task-Specific Context:** ก่อนเริ่มงานใหม่ ให้ใช้ `task_boundary` เพื่อ Reset Context หรือระบุ Scope ให้ชัดเจน
* **Verification Scripts:** เก็บไว้ใน `tests/verification/` ห้ามทิ้งเรี่ยราด
* **Legacy Code:** ถ้าเจอ Code เก่าที่ "Over-engineered" ให้ Refactor ลงมาเป็น GSD Style (Simplify) เมื่อมีโอกาส

---

## **5. Definition of Done**

1. **Verified:** มีหลักฐาน (Logs/Screenshot) ว่า code ทำงานได้จริง
2. **Clean:** ไม่มี Dead Code หรือ Ghost Files ที่ไม่ได้ใช้
3. **Wired:** Component A คุยกับ B ได้จริง (ไม่ใช่แค่ Mock)

---
*Authored by: EVA Orchestrator (After GSD Alignment)*
