# **🎯 Mission: EVA v9.4.3 Refactor & Standard Alignment**

Project Version: v9.4.3 (Resonance Refactored)  
Primary Architecture: System \> Module \> Node \> Component  
Design Philosophy: SOLID-based Structure + GSD-driven Implementation
Codified Standards: [.agent/rules/resonancestandard.md](file:///e:/The%20Human%20Algorithm/T2/agent/.agent/rules/resonancestandard.md) | [.agent/workflows/autonomous-refactor.md](file:///e:/The%20Human%20Algorithm/T2/agent/.agent/workflows/autonomous-refactor.md)

## **🚦 System Status & Progress Tracking**

*ส่วนนี้ใช้สำหรับให้ Orchestrator อัปเดตสถานะภาพรวม เพื่อให้ Agent ชุดต่อไปรู้จุดพักงาน*

* **Current Active Phase:** Task 0 (Planning)  
* **Overall Completion:** 0%  
* **System Integrity:** 🟢 Stable (Wait for refactor)  
* **Last Updated:** \[ระบุวันเวลาเมื่อเริ่มงาน\]

## **🤖 Agent Roles & Chain of Command**

### **1\. Main Agent (Orchestrator) \- "The Architect"**

* **Duty:** อ่านแผนที่ใหญ่, แตก Task, **อนุมัติผลงานของ Worker**, และเขียน Handover Memo  
* **Constraint:** ห้ามเขียน Logic เองเด็ดขาด หน้าที่คือ "ตรวจ" และ "สั่ง" เท่านั้น

### **2\. Sub-agent (Worker) \- "The Technician"**

* **Duty:** รับคำสั่งรายย่อยจาก Orchestrator, แก้ไขโค้ดทีละส่วน, รัน Test  
* **Constraint:** ต้องเสนอการแก้ไข (Batch Edit) และรอให้ Orchestrator (หรือ User) ติ๊ก \[x\] ก่อนไปต่อ

## **🚀 Execution & Autonomy Protocol (Full Auto Mode)**

เพื่อให้พี่สั่งงานแล้ว "ไปข้างนอกได้" โดย AI ไม่มึน:

1. **Cycle: Plan \-\> Code \-\> Verify \-\> Summarize:**  
   * **Plan:** Orchestrator ระบุไฟล์ที่ต้องแก้ใน Task นั้นๆ  
   * **Code:** Worker ทำการ Batch Edit ทุกไฟล์ที่เกี่ยวข้องในเทิร์นเดียว  
   * **Verify:** Agent ต้องรัน Terminal เพื่อเช็ค Syntax และรัน Test Script เสมอ  
   * **Summarize:** เมื่อ Test ผ่าน Orchestrator ต้องอัปเดต Checklist \[x\] ในไฟล์นี้ทันที  
2. **Self-Healing:** หากรัน Test แล้วพบบั๊ก Agent ต้องพยายามแก้เองอย่างน้อย 3 ครั้งก่อนจะหยุดรอ User  
3. **No-Prompt Acceptance:** ในโหมด "Always Process" ให้ Agent ใช้ความเงียบในการทำงานจนจบ Task ใหญ่ แล้วค่อยแจ้งสรุปทีเดียว

## **📋 Strategic Roadmap (The Master Plan)**

### **🔴 Phase 1: Structural Foundations (SOLID)**

*เป้าหมาย: วางโครงกระดูกใหม่ ห้ามข้ามขั้นตอนนี้*

* \[ \]### **Task 1: Interface & Contract Definition (SOLID Layer)**

* [x] **1.1 สร้าง Directory:** สร้าง agent/contracts/systems/ และ agent/contracts/modules/  
* [x] **1.2 นิยาม I-Prefix ABCs:** สร้าง Interface IMSPassport.py, IMemoryRetrieval.py, IMemoryStorage.py  
* \[ \]### **Task 1: Interface & Contract Definition (SOLID Layer)**

* [x] **1.1 สร้าง Directory:** สร้าง agent/contracts/systems/ และ agent/contracts/modules/  
* [x] **1.2 นิยาม I-Prefix ABCs:** สร้าง Interface IMSPassport.py, IMemoryRetrieval.py, IMemoryStorage.py  
* \[ \] **1.3 Documentation Sync:** อัปเดต docs/protocols/ARCHITECTURAL\_STANDARDS.md ให้ตรงกับ Interface ใหม่  
  * Status: \[TODO\]

### **🔵 Phase 2: Engine Deconstruction (Decoupling)**

* [x] **Task 2: MSP Engine Refactoring (Module Delegation)**
  * [x] Implement `IMemoryRetrieval` and `IMemoryStorage` in Modules.
  * [x] Delegate logic from `MSP` facade to Modules.
  * [x] Migrate query logic to submodule specific nodes.
  * [x] Transformation of MSP into a pure high-level facade.
* [x] **Task 3: Resonance Bus & State Decoupling**
* [x] **Task 2: MSP Engine Refactoring (Module Delegation)**
  * [x] Implement `IMemoryRetrieval` and `IMemoryStorage` in Modules.
  * [x] Delegate logic from `MSP` facade to Modules.
  * [x] Migrate query logic to submodule specific nodes.
  * [x] Transformation of MSP into a pure high-level facade.
* [x] **Task 3: Resonance Bus & State Decoupling**
  * [x] Refactor `resonance_bus.py` to implement `IResonanceBus` interface.
  * [x] Update Matrix & Physio Subscriber patterns.
  * [x] Transform MSP Engine into a passive listener for automatic state latching.

### **🟡 Phase 3: Communication & Integrity**

* [x] **Task 3.3: Final Integrity Check & Version Stamp v9.4.3**

## **📝 Handover Memos (The "Eternal Memory" Store)**

*Agent: เมื่อต้อง Reset Session ให้เขียนสรุป Technical Delta ที่นี่*

* **Status:** รอนุมัติเริ่ม Task 1.1  
* **Next Direct Command:** "Orchestrator: Initialize Task 1.1 and create directory structure."  
* **Context Hash:** N/A

## **🚨 Final Directives for AI**

* **SSOT Rule:** ยึดไฟล์นี้เป็นคำสั่งสูงสุด หากโค้ดขัดแย้งกับแผน ให้ยึดแผนเป็นหลัก  
* **Batch Rule:** พยายามแก้ไขหลายไฟล์พร้อมกันเพื่อลดจำนวนการกด Accept  
* **Safety Rule:** ห้ามแตะ PhysioCore (STRUCTURAL LOCK)
