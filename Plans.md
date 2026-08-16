# Agent Analytica 2.0 - Master Implementation & Execution Plans

An AI-powered multi-agent data analytics platform featuring automated dataset profiling, diagnostic analytics, multi-model forecasting, hybrid anomaly detection, explainable AI, zero-trust QA validation, and decoupled AWS production deployment.

---

## Architecture Principles & Design Decisions

* **Decoupled AWS Production Architecture (Option 1):**
  * **Frontend Tier:** Single-Page React Application built with Vite, styled with dark glassmorphism and Outfit typography. Hosted on **AWS Amplify** with global CDN edge delivery.
  * **Backend Tier:** Production FastAPI REST API containerized with Docker and deployed on **AWS App Runner** / **AWS ECS Fargate** with auto-scaling.
  * **Database Tier:** Managed **AWS RDS PostgreSQL** storing dataset metadata, analysis runs, KPIs, recommendations, and audit logs.
* **Zero-Emoji Professional Standard:** Interface outputs, logs, documentation, generated Word documents (.docx), and PowerPoint slide decks (.pptx) strictly adhere to clean ASCII / markdown formatting without emojis.
* **Humanized Workflow:** Data cleaning actions present recommended steps (such as median imputation) for user approval rather than mutating data silently.

---

## 12-Week Master Roadmap Overview

```
Phase 0 : Baseline Audit & Test Harnesses                [COMPLETED]
Phase 1 : Data Intelligence Layer                        [COMPLETED]
Phase 2 : Analytics & Dynamic Visualization Engine      [COMPLETED]
Phase 3 : Multi-Level Anomaly Detection Engine           [COMPLETED]
Phase 4 : Time-Series Forecasting & Backtesting          [COMPLETED]
Phase 5 : Explainable AI & Zero-Trust QA Validation      [COMPLETED]
Phase 6 : LLM & Agent Router Architecture                [COMPLETED]
Phase 7 : Actionable Recommendation Engine              [COMPLETED]
Phase 8 : Root Cause & What-If Scenario Engines          [COMPLETED]
Phase 9 : UI Redesign & Multi-Mode Dashboard             [COMPLETED]
Phase 10: Automated Reports (.docx) & Decks (.pptx)       [COMPLETED]
Phase 11: Enterprise Integrations (Excel & Power BI)    [COMPLETED]
Phase 12: Production Backend, Database & Docker Setup    [COMPLETED]
```

---

## Phase 3 to Phase 6 Execution Sprint Roadmap

### Phase 3: Multi-Level Anomaly Detection Engine
* **Objective:** Combine statistical, parametric, and machine learning anomaly detection methodologies.
* **Specifications:**
  1. Level 1 (Statistical IQR): Compute Interquartile Range bounds per numeric column to flag univariate spikes (`lower_bound = Q1 - 1.5*IQR`, `upper_bound = Q3 + 1.5*IQR`).
  2. Level 2 (Parametric Z-Score): Identify records exceeding 3 standard deviations from the population mean.
  3. Level 3 (Machine Learning Isolation Forest): Train `sklearn.ensemble.IsolationForest` to identify multivariate pattern anomalies.
* **Outputs:** Unified Anomaly Score (0 to 100), severity tier (`High`, `Medium`, `Low`), and reasoning logs.

### Phase 4: Time-Series Forecasting & Backtesting Engine
* **Objective:** Multi-model time-series forecasting with historical backtesting and model selection.
* **Specifications:**
  1. Time Column Auto-Detection: Automatically infer date/time dimensions across irregular dataset columns.
  2. Multi-Model Suite: Evaluate Linear Trend Regression, Moving Average Baseline, and Exponential Smoothing (`statsmodels.tsa.holtwinters`).
  3. Historical Backtesting (80/20 Split): Evaluate models on an 80% train / 20% test split to compute MAPE, MAE, and RMSE metrics.
  4. Automated Selection: Select the model with the lowest test MAPE score.
* **Outputs:** Forecast values, backtesting accuracy metrics, and 95% confidence intervals.

### Phase 5: Explainable AI & Zero-Trust QA Validation Layer
* **Objective:** Provide numerical lineage tracing and intercept LLM outputs to prevent hallucinations.
* **Specifications:**
  1. Metric Shift Decomposition (`analysis/trends.py`): Calculate exact subgroup percentage contributions for macro metric shifts.
  2. QA Validation Engine (`qa/qa_engine.py`):
     * Numeric Cross-Referencing: Verify narrative figures against deterministic KPI engine outputs.
     * Hallucination Risk Check: Flag unverified numeric claims larger than structural threshold numbers.
     * Contradiction Check: Identify revenue vs profit trend divergence flags.
* **Outputs:** QA Confidence Score (0 to 100%), metric match logs, and contradiction alerts.

### Phase 6: LLM & Agent Router Architecture
* **Objective:** Decouple natural language routing from deterministic Python calculation tools.
* **Specifications:**
  1. Agent Orchestrator (`agents/orchestrator.py`): Coordinate execution sequence across Profiler, Cleaner, Anomaly Engine, Forecasting Engine, Analysis Agent, QA Layer, and Recommendation Engine.
  2. Decoupled Prompt Design: Embed calculated statistical outputs directly into prompt context windows to prevent inline math generation by the LLM.
* **Outputs:** Unified pipeline state artifact containing cleaned datasets, metrics, insights, and actionable recommendations.

---

## AWS Deployment Architecture (Option 1)

### Infrastructure Configuration (`aws/`)
* **`aws/app_runner.json`**: AWS App Runner service configuration for containerized FastAPI deployment.
* **`aws/amplify.yml`**: AWS Amplify build pipeline specification for the React frontend.
* **`aws/cloudformation.template.yaml`**: Infrastructure-as-Code template for AWS RDS PostgreSQL, VPC, and Security Groups.
* **`aws/deploy_aws.ps1`**: PowerShell deployment automation script.

---

## Verification & Testing Harnesses

All modules are validated with 34 unit tests under `tests/`:
```bash
python -m unittest discover -s tests
```

Master 12-phase deep verification audit:
```bash
python scratch/test_master_verification_all_phases.py
```
