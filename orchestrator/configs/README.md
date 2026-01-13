# Orchestrator Configuration Management

This directory contains the central configuration for the EVA Orchestrator system.

## 🟢 Single Source of Truth (SSOT)
The file **`orchestrator_configs.yaml`** is the **Single Source of Truth** for the entire orchestration layer. 

### Mandatory Sync Protocol
1. **Always edit `orchestrator_configs.yaml` first.** This file controls the runtime behavior of the Orchestrator, CIN, and PMT.
2. **Synchronize with Sub-configs**: After making changes to the SSOT, ensure that the corresponding values in the following files are updated to maintain consistency:
   - `orchestrator/cin/configs/CIN_configs.yaml`
   - `orchestrator/pmt/configs/PMT_configs.yaml` (or relevant files in `pmt/configs/`)

### File Roles
- `orchestrator_configs.yaml`: Unified runtime configuration (High Precedence).
- `CIN_configs.yaml`: Legacy/Module-specific fallback for Context Injection.
- `PMT_configs.yaml`: Legacy/Module-specific fallback for Prompt Rule Layer.

> [!WARNING]
> Inconsistencies between the SSOT and sub-configs may lead to unpredictable behavior during fallback scenarios or module-level testing.

---

# การจัดการคอนฟิกของ Orchestrator

ไดเรกทอรีนี้เก็บไฟล์คอนฟิกหลักสำหรับระบบ EVA Orchestrator

## 🟢 Single Source of Truth (SSOT)
ไฟล์ **`orchestrator_configs.yaml`** คือ **แหล่งข้อมูลความจริงหนึ่งเดียว (SSOT)** สำหรับเลเยอร์การจัดการทั้งหมด

### โปรโตคอลการซิงค์ที่ต้องปฏิบัติ (Mandatory Sync)
1. **แก้ไขที่ `orchestrator_configs.yaml` เสมอ:** ไฟล์นี้ควบคุมพฤติกรรมการทำงานจริงของ Orchestrator, CIN และ PMT
2. **การซิงโครไนซ์กับคอนฟิกย่อย:** หลังจากแก้ไข SSOT แล้ว ต้องตรวจสอบและอัปเดตค่าในไฟล์ย่อยต่อไปนี้ให้สอดคล้องกันเสมอ:
   - `orchestrator/cin/configs/CIN_configs.yaml`
   - `orchestrator/pmt/configs/PMT_configs.yaml`

### บทบาทของไฟล์
- `orchestrator_configs.yaml`: คอนฟิกรวมสำหรับการรันไทม์ (มีลำดับความสำคัญสูงสุด)
- `CIN_configs.yaml`: คอนฟิกสำรอง (Fallback) สำหรับระบบ Context Injection
- `PMT_configs.yaml`: คอนฟิกสำรอง (Fallback) สำหรับระบบ Prompt Rule Layer

> [!WARNING]
> ความไม่สอดคล้องกันระหว่าง SSOT และคอนฟิกย่อยอาจทำให้เกิดพฤติกรรมที่ไม่คาดคิดในช่วงที่ระบบต้องใช้ค่าสำรองหรือระหว่างการทดสอบแยกโมดูล
