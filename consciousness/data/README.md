# Consciousness Data (Runtime Workspace)

**Directory**: `consciousness/data/`  
**Purpose**: Transient workspace for runtime assets and processing.  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **Consciousness Data** directory is a transient "Scratchpad" for the EVA organism. It is designed to hold temporary files that the consciousness layer (LLM) or its capabilities interact with during the current runtime session.

### ⚠️ คุณสมบัติสำคัญ (Must Know)

- ✅ **Read/Write**: สามารถเขียนและอ่านไฟล์ได้โดยตรง
- ❌ **Non-Persistent**: ข้อมูลจะหายไปเมื่อสิ้นสุด Session (Session จบ = หาย)
- ❌ **Not System Memory**: ไม่ใช่ส่วนหนึ่งของสถานะระบบ (System State)
- ❌ **Not Knowledge/Recall**: ไม่ใช่พื้นที่จัดเก็บ Knowledge, Semantic, หรือ Episodic Memory
- ❌ **No Persistence Guarantee**: ไม่มีการรับประกันความคงอยู่ของข้อมูลในระยะยาว

---

## ⚙️ Use Cases

1. **Uploads**: Staging area for files uploaded by the user.
2. **Extraction**: Destination for unzipped or decrypted content.
3. **Generation**: Storage for assets created by code (e.g., generated images, PDFs, CSVs).
4. **Intermediate Output**: Logs or temp files generated during multi-step capability execution.

---

## 📂 Structure

This directory is unstructured by design to allow flexibility for various capabilities. However, developers are encouraged to use subdirectories for complex tasks (e.g., `data/unzip_temp/`).

---

## 📐 Governance

- **Volatility**: This directory is **TRANSIENT**. It is not intended for long-term storage.
- **Persistence**: Unlike the `context_container`, which is cleared every turn, the `data` folder may persist across turns within a single session but should be considered cleared upon session termination or manual garbage collection.
- **Security**: Contains raw assets; ensure sensitive data is cleared after use.

---

*The ephemeral workshop of the mind.*
