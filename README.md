# 🛡️ Shift-Left Security Demo: End-to-End DevSecOps Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Hardened-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Security](https://img.shields.io/badge/Security-Shift_Left-success)

## 🎯 Project Overview

This repository demonstrates a **Mid-level DevSecOps engineering approach** to securing a software development lifecycle (SDLC). It features a vulnerable-by-design Python (FastAPI) application and implements a strict, multi-layered security pipeline. 

The goal is to showcase the **"Shift-Left"** methodology: catching vulnerabilities, leaked secrets, and misconfigurations as early as the developer's local machine, all the way through automated CI/CD quality gates, and enforcing Policy-as-Code.

---

## 🏗️ Architecture & Security Gates

The project is structured into four distinct security phases:

### 1. The Vulnerable Application (Target)
A deliberately flawed REST API built with Python and FastAPI. It contains typical OWASP Top 10 vulnerabilities to trigger our security scanners:
* **SQL Injection (SQLi):** Raw SQL queries without parameterization.
* **Cross-Site Scripting (XSS):** Unsanitized user inputs reflected in responses.
* **Hardcoded Secrets:** Intentional exposure of dummy API keys in the source code.

### 2. Local Guard (True Shift-Left)
Security starts before the `git commit`. The repository utilizes `pre-commit` hooks to provide immediate feedback to developers:
* `check-yaml` & `end-of-file-fixer`: Standard code quality checks.
* **Local Gitleaks:** Prevents committing hardcoded secrets to the local git tree.
* **Local Semgrep:** Runs lightweight Static Application Security Testing (SAST) directly on the developer's machine.

### 3. CI/CD Pipeline (GitHub Actions)
The `.github/workflows/security.yml` defines a strict pipeline with multiple Quality Gates. If any gate fails, the build is broken.
* **Secrets Detection:** `Gitleaks` scans the entire commit history for exposed credentials.
* **SCA (Software Composition Analysis):** `pip-audit` analyzes `requirements.txt` for known vulnerable Python dependencies.
* **SAST (Static Analysis):** `Semgrep` scans the source code using specific `p/python` and `p/fastapi` rule sets to catch SQLi and XSS.
* **IaC Scanning:** `Checkov` evaluates the `Dockerfile` for infrastructure-as-code misconfigurations.
* **Container Scanning:** `Trivy` scans the built Docker image for OS-level vulnerabilities (CVEs).

### 4. Container Hardening & Policy-as-Code (The Cherry on Top)
To demonstrate remediation skills, the project documents the evolution of the application's infrastructure:

#### 📉 Before: The "Bad" Dockerfile
* Used a heavy, bloated base image (`python:3.11`).
* Ran the application as the `root` user.
* Contained hundreds of unnecessary OS-level vulnerabilities.

#### 📈 After: The Hardened Dockerfile
* Migrated to a minimal base image (e.g., `alpine` or `distroless`).
* Implemented the Principle of Least Privilege by creating a dedicated `appuser`.
* Removed unnecessary build tools from the final image using multi-stage builds.

> **Trivy Scan Comparison**
> 
> | Scan Stage | CRITICAL | HIGH | MEDIUM | LOW |
> | :--- | :---: | :---: | :---: | :---: |
> | **Initial (Root/Heavy)** | 🔴 24 | 🟠 89 | 🟡 140 | 🔵 30 |
> | **Hardened (Appuser/Alpine)**| 🟢 0 | 🟢 0 | 🟢 2 | 🔵 1 |

#### 🛑 Policy-as-Code (Open Policy Agent)
The pipeline integrates **OPA (Open Policy Agent)**. A custom `policy.rego` file evaluates the Trivy JSON output. **The build is automatically blocked and failed if any `CRITICAL` vulnerabilities are detected**, enforcing a strict security baseline.

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.11+
* Docker
* `pre-commit` installed locally

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/NikodemHeitzman/shift-left-security-demo.git](https://github.com/NikodemHeitzman/shift-left-security-demo.git)
   cd shift-left-security-demo
