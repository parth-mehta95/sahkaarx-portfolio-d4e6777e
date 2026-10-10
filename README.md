# AI-Enhanced Python Package & Git Conflict Resolution Portfolio

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Packaging](https://img.shields.io/badge/Packaging-PEP%20517%20%7C%20PEP%20621-brightgreen.svg)](https://packaging.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Pytest-Passing-success.svg)](https://pytest.org/)
[![Git Flow](https://img.shields.io/badge/Branching-Git--Flow-orange.svg)](https://git-scm.com/)

A production-grade Python package repository initialized with modern standards (**PEP 517 / PEP 621**, `pyproject.toml`, `setup.py`), clean `src/` layout, unit testing suite (`pytest`), and a comprehensive merge conflict simulation and resolution workflow across competing feature branches.

---

## 📌 Repository Information
- **GitHub Repository URL:** [https://github.com/parth-mehta95/sahkaarx-portfolio-d4e6777e](https://github.com/parth-mehta95/sahkaarx-portfolio-d4e6777e)
- **Primary Branch:** `main`
- **Feature Branches:**
  - `feature/streaming-response` (Token-level streaming generator with latency tracking)
  - `feature/batch-optimization` (Buffered batch evaluation with SHA-256 LRU cache)

---

## 📁 Repository & Package Layout

```
.
├── .gitignore                                   # Standard Python & OS ignore rules
├── LICENSE                                      # MIT Open Source License
├── README.md                                    # Root repository documentation
├── pyproject.toml                               # PEP 517 / PEP 621 build configuration
├── setup.py                                     # Backward-compatible & editable installation setup
├── setup.cfg                                    # Package metadata and tool configurations
├── requirements.txt                             # Runtime dependencies
├── requirements-dev.txt                         # Development & testing dependencies
├── docs/
│   └── git_conflict_resolution_walkthrough.md   # Step-by-step Git branching & conflict guide
├── scripts/
│   ├── simulate_conflict_and_merge.ps1          # One-click conflict & merge automation (PowerShell)
│   └── simulate_conflict_and_merge.sh           # One-click conflict & merge automation (Bash)
├── src/
│   └── ai_enhanced_pkg/
│       ├── __init__.py                          # Public package exports & version declaration
│       ├── core.py                              # AIEngineConfig dataclass & AIEnhancedClient
│       ├── exceptions.py                        # Custom error classes (PromptValidationError, etc.)
│       ├── prompt_engine.py                     # Unified streaming & batch execution engine
│       └── utils.py                             # Token estimators, sanitizers & cache hashing
├── tests/
│   ├── __init__.py                              # Test package marker
│   ├── conftest.py                              # Shared pytest fixtures
│   ├── test_core.py                             # Unit tests for config & client metrics
│   ├── test_prompt_engine.py                    # Unit tests for templates, caching, stream, batch
│   └── test_utils.py                            # Unit tests for token counters & hashing
└── practice/
    └── week-01-initialize-python-package-repository-with-confli/
        └── README.md                            # Week 01 task brief and checklist
```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/parth-mehta95/sahkaarx-portfolio-d4e6777e.git
cd sahkaarx-portfolio-d4e6777e
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Package in Editable Mode
```bash
# Production dependencies + local package
pip install -e .

# Development dependencies (testing, linting)
pip install -r requirements-dev.txt
```

---

## 🧪 Running Unit Tests
```bash
pytest -v
```

All test cases validate:
1. `AIEngineConfig` parameter validation and constraint checks.
2. `PromptTemplate` placeholder parsing, sanitization, and variable enforcement.
3. `PromptEngine` single-prompt execution and deterministic caching.
4. `stream_prompt()` generator functionality (from `feature/streaming-response`).
5. `execute_batch()` throughput & cache hit optimization (from `feature/batch-optimization`).

---

## 🔀 Git Conflict Simulation & Resolution Workflow

### Scenario Overview
Two developers developed competing features on separate branches targeting the same function in `src/ai_enhanced_pkg/prompt_engine.py`:
- **Branch A (`feature/streaming-response`)**: Implemented chunk-based streaming generation.
- **Branch B (`feature/batch-optimization`)**: Implemented high-throughput batch evaluation with caching.

### Step 1: Branch Creation & Competing Edits
```bash
# Branch A
git checkout -b feature/streaming-response
# (implements streaming generator in prompt_engine.py)
git add src/ai_enhanced_pkg/prompt_engine.py README.md
git commit -m "feat(stream): implement streaming token generator in prompt_engine"

# Branch B
git checkout main
git checkout -b feature/batch-optimization
# (implements batch optimization on identical lines in prompt_engine.py)
git add src/ai_enhanced_pkg/prompt_engine.py README.md
git commit -m "feat(batch): implement batch optimization and LRU cache in prompt_engine"
```

### Step 2: Merge Branch A to `main`
```bash
git checkout main
git merge feature/streaming-response -m "Merge branch 'feature/streaming-response' into main"
```

### Step 3: Trigger Conflict by Merging Branch B
```bash
git merge feature/batch-optimization
# Output: CONFLICT (content): Merge conflict in src/ai_enhanced_pkg/prompt_engine.py
```

### Step 4: Resolution & Verification
The conflict was resolved by **harmonizing both innovations**: combining real-time streaming with batch caching in `src/ai_enhanced_pkg/prompt_engine.py`.

```bash
# Stage resolved files
git add src/ai_enhanced_pkg/prompt_engine.py README.md

# Commit resolution
git commit -m "Merge branch 'feature/batch-optimization' into main (resolved conflicts: unified streaming and batch caching)"

# Verify tests pass on merged codebase
pytest tests/ -v
```

### Step 5: Push All Branches
```bash
git push -u origin main
git push -u origin feature/streaming-response
git push -u origin feature/batch-optimization
```

---

## 💻 Automated Conflict Simulation Script
To execute the conflict simulation and resolution automatically in a single command:
- **Windows (PowerShell):**
  ```powershell
  .\scripts\simulate_conflict_and_merge.ps1
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  bash scripts/simulate_conflict_and_merge.sh
  ```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
