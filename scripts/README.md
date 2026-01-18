# EVA Utility Scripts

**Directory**: `scripts/`  
**Purpose**: System-level utility, verification, and audit tools.  
**Version**: v9.6.2

---

## 📋 Overview

The **Scripts** directory contains standalone Python utilities used for system maintenance, version auditing, and integrity verification. These scripts are run externally (not part of the main organism loop) during development and deployment.

---

## 📂 Notable Scripts

### 1. [Check Doc Alignment](check_doc_alignment.py)

Audits the entire codebase to ensure that documentation (READMEs, ADRs) aligns with the current system versions in the Registry.

### 2. [Check Versions](check_versions.py)

Specifically validates version strings in file headers against `registry/eva_master_registry.yaml`.

### 3. [Verify Physio Loop](verify_physio_loop.py)

Runs a headless simulation of `PhysioCore` to ensure hormone decay and basal secretion are stable.

### 4. [Verify Matrix Coupling](verify_matrix_coupling.py)

Tests the interaction between `PhysioCore` pulses and `EVAMatrix` emotional shifts via the Resonance Bus.

---

## 🚀 Usage

Most scripts are designed to be run from the root directory:

```bash
python scripts/check_doc_alignment.py
```

---

*Verified Integrity.*
