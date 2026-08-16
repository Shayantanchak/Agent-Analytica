# Agent Analytica 2.0 - Phase 3 to Phase 6 Implementation Plan

A structured 1-week execution roadmap covering advanced analytical intelligence, multi-model forecasting, hybrid anomaly detection, explainable AI, zero-trust QA validation, and decoupled LLM agent routing.

---

## Executive Overview

This plan details the technical roadmap for building the analytical intelligence layer of **Agent Analytica 2.0** over a 7-day sprint. The primary goal is to separate statistical computation from natural language generation, guaranteeing zero hallucination risk, exact mathematical precision, and auditable reasoning lineage.

---

## 1-Week Timeline Schedule

```
Day 1 - Day 2: Phase 3 (Multi-Level Anomaly Detection Engine)
Day 3 - Day 4: Phase 4 (Time-Series Forecasting & Backtesting)
Day 5 - Day 6: Phase 5 (Explainable AI & Zero-Trust QA Validation)
Day 7        : Phase 6 (LLM & Agent Router Architecture)
```

---

## Phase Specifications

### Phase 3: Multi-Level Anomaly Detection Engine
* **Target Duration:** Days 1-2
* **Objective:** Implement a 3-tier hybrid anomaly detection engine combining statistical, parametric, and machine learning methodologies.
* **Component Specs:**
  1. **Level 1 (Statistical IQR):** Compute Interquartile Range (IQR) bounds per numeric column to catch univariate spikes (`lower_bound = Q1 - 1.5*IQR`, `upper_bound = Q3 + 1.5*IQR`).
  2. **Level 2 (Parametric Z-Score):** Flag records exceeding 3 standard deviations from the population mean.
  3. **Level 3 (Machine Learning Isolation Forest):** Train `sklearn.ensemble.IsolationForest` on numeric features to detect multivariate relationship anomalies.
* **Outputs:** Unified Anomaly Score (0 to 100), severity assignment (`High`, `Medium`, `Low`), and readable explanation logs for each flagged row.

### Phase 4: Time-Series Forecasting Engine & Backtesting
* **Target Duration:** Days 3-4
* **Objective:** Build a multi-model time-series forecasting engine with historical backtesting and automated model selection.
* **Component Specs:**
  1. **Time Column Auto-Detection:** Infer date/time columns across irregular formats.
  2. **Multi-Model Suite:**
     * Linear Trend Regression
     * Moving Average Baseline
     * Exponential Smoothing (`statsmodels.tsa.holtwinters`)
  3. **Historical Backtesting (80/20 Split):** Train models on 80% historical data and evaluate on 20% test set using Mean Absolute Percentage Error (MAPE), MAE, and RMSE metrics.
  4. **Automated Selection:** Automatically select the model with the lowest test MAPE score.
* **Outputs:** Selected model name, backtesting error metrics, projected future values, and 95% confidence intervals.

### Phase 5: Explainable AI & Zero-Trust QA Validation Layer
* **Target Duration:** Days 5-6
* **Objective:** Provide exact numerical lineage tracing for trend shifts and intercept LLM outputs to prevent hallucinations.
* **Component Specs:**
  1. **Metric Shift Decomposition (`analysis/trends.py`):** Calculate exact subgroup contribution percentages (for example: Total revenue drop -12.4% -> South Region -6.1%, Product A -3.8%, Customer Segment B -2.5%).
  2. **QA Validation Layer (`qa/qa_engine.py`):**
     * Numeric Cross-Referencing: Match LLM narrative figures against strict KPI engine outputs.
     * Hallucination Risk Check: Flag unverified numeric claims larger than structural threshold numbers.
     * Contradiction Check: Identify revenue vs profit trend divergence flags.
* **Outputs:** QA Confidence Score (0 to 100%), metric match logs, and contradiction alerts.

### Phase 6: LLM & Agent Router Architecture
* **Target Duration:** Day 7
* **Objective:** Implement a decoupled agent orchestrator pipeline that separates natural language intent understanding from numeric calculation.
* **Component Specs:**
  1. **Agent Orchestrator (`agents/orchestrator.py`):** Coordinate execution sequence: Ingestion -> Profiler -> Cleaner -> Anomaly Engine -> Forecasting Engine -> Analysis Agent -> QA Layer -> Recommendations.
  2. **Decoupled Prompt Design:** Embed deterministic statistical outputs directly into the prompt context window to prevent inline math generation by the LLM.
* **Outputs:** Unified state dictionary containing cleaned datasets, profiling metrics, QA reports, trend forecasts, and actionable recommendations.

---

## Verification & Testing Harnesses

Each phase includes automated unit tests under `tests/`:
* `tests/test_anomaly.py` (Phase 3 verification)
* `tests/test_forecasting.py` (Phase 4 verification)
* `tests/test_trends.py` (Phase 5 verification)
* `tests/test_orchestrator.py` (Phase 6 verification)

### Test Execution Command
```bash
python -m unittest discover -s tests
```

---

## Git Commit & Delivery Workflow

Upon completing each phase:
```bash
git add .
git commit -m "Complete Phase X implementation"
git push origin main
```
