# Agent Analytica 2.0

An AI-powered multi-agent data analytics platform designed for automated data profiling, diagnostic analytics, forecasting, anomaly detection, explainable insights, and automated report generation.

---

## System Overview

Agent Analytica 2.0 transforms raw datasets into decision-ready business intelligence, executive summaries, structured documents, and slide decks. The platform separates statistical computations from natural language generation to guarantee numerical precision, transparency, and auditability.

Key highlights of the platform architecture include:
* Multi-format ingestion supporting CSV, Excel, and Google Sheets.
* Automated dataset profiling with data quality scoring.
* Interactive data cleaning with user approval workflows.
* Multi-level anomaly detection combining statistical and machine learning methods.
* Time-series forecasting with automated backtesting and model selection.
* QA-validated explainable AI for root-cause and what-if analysis.
* Automated report generation in Word (.docx) and PowerPoint (.pptx) formats.
* Multi-mode presentation tailoring output for students, professionals, and executives.

---

## System Architecture

```
                                  USER INTERFACE
                               (React / Streamlit)
                                        |
                                        v
                                 FASTAPI BACKEND
                                        |
                                        v
                                  AGENT ROUTER
                                        |
      +---------------------------------+---------------------------------+
      |                                 |                                 |
      v                                 v                                 v
 DATA AGENT                     ANALYTICS AGENT                       RAG AGENT
      |                                 |                                 |
      |                 +---------------+---------------+                 |
      |                 |               |               |                 |
      |                 v               v               v                 |
      |            KPI Engine    Anomaly Detection  Forecasting Engine    |
      |                 |               |               |                 |
      +-----------------+---------------+---------------+-----------------+
                                        |
                                        v
                               ROOT CAUSE ENGINE
                                        |
                                        v
                                QA VALIDATION LAYER
                                        |
                                        v
                                EXPLAINABLE INSIGHTS
                                        |
                                        v
                               RECOMMENDATION ENGINE
                                        |
         +------------------------------+------------------------------+
         |                              |                              |
         v                              v                              v
  Interactive UI                 Word Report (.docx)          PowerPoint (.pptx)
         |
         v
External Integrations (Excel Export / Google Sheets API / Power BI Bridge)
```

---

## Core Capabilities Matrix

| Capability | Category | Status | Description |
| :--- | :--- | :--- | :--- |
| Data Ingestion | Data Engine | Production | Ingests CSV, Excel, and Google Sheets files. |
| Automated Profiling | Data Engine | Production | Calculates completeness, duplicate count, schema types, and data quality score. |
| Automated Cleaning | Data Engine | Production | Detects missing values and outliers with explicit user approval logic. |
| KPI Engine | Analytics Engine | Production | Dynamically computes domain-specific metrics for Sales, HR, and Finance. |
| Visualization System | Analytics Engine | Production | Automatically selects optimal Plotly chart types based on data attributes. |
| Multi-Level Anomaly Detection | Analytics Engine | Production | Combines IQR, Z-Score, and Isolation Forest algorithms. |
| Time-Series Forecasting | Analytics Engine | Production | Evaluates Baseline, ARIMA, and Prophet models using historical backtesting. |
| Explainable Insights | Insight Layer | Production | Decomposes numerical trends into exact contribution percentages. |
| QA Validation Layer | Insight Layer | Production | Verifies all LLM-generated claims against raw statistical outputs. |
| Natural-Language Routing | Agent Layer | Production | Decouples user intent routing from underlying deterministic calculations. |
| Root-Cause Analysis | Decision Support | Production | Traces revenue and metric drops down to contributing sub-factors. |
| What-If Scenario Engine | Decision Support | Production | Simulates custom parameter shifts and estimates impact on outcomes. |
| Recommendation Engine | Decision Support | Production | Generates prioritized business recommendations with confidence scores. |
| Multi-Mode Presentation | UI Layer | Production | Renders insights in Student, Professional, or Executive detail levels. |
| Report & Deck Generators | Export Engine | Production | Exports structured Word documents and widescreen PowerPoint presentations. |

---

## Audit Checklist (Baseline Evaluation)

Before implementing version 2.0 enhancements, the existing codebase is audited against the target functional matrix:

* [x] Data Ingestion Engine
* [x] Data Cleaning Module
* [x] Data Profiling Module
* [x] KPI Analysis Engine
* [x] Anomaly Detection Module
* [ ] Time-Series Forecasting Engine
* [x] Explainable Insights Layer
* [x] QA Validation Layer
* [ ] Actionable Recommendation Engine
* [x] Word Report Generation
* [x] PowerPoint Generation
* [ ] Excel Export Integration
* [x] Google Sheets Connector
* [ ] Power BI Bridge
* [x] LLM Router Integration
* [x] Streamlit Dashboard UI
* [ ] PostgreSQL Database Integration
* [ ] User Authentication Module
* [ ] Cloud API Deployment

---

## 12-Week Master Implementation Roadmap

### Phase 0: Baseline Audit and Refactoring
* **Duration:** Days 1-3
* Audit existing codebase and dependencies.
* Standardize data structures and establish test harnesses for existing components.
* Output: Stable baseline build.

### Phase 1: Data Intelligence Layer
* **Duration:** Weeks 1-2
* **Multi-Format Ingestion:** Implement unified ingestion for CSV, Excel (.xlsx), and Google Sheets using Pandas, Polars, openpyxl, and Google Sheets API.
* **Automated Profiling:** Calculate dataset metrics including row counts, column types, missing percentage, duplicate counts, date indicators, target candidates, and an overall Data Quality Score (0 to 100).
* **Automated Cleaning Workflow:** Detect missing values, invalid dates, type mismatches, and extreme values. Present recommended actions (such as median imputation or record dropping) for explicit user approval before mutating dataset state.
* **Domain-Aware KPI Engine:** Pre-configure calculations for Sales (Revenue, Profit, Margin, AOV, Growth), HR (Headcount, Attrition, Average Salary, Retention), and Finance (Revenue, Expenses, Profit, ROI, Cash Flow).

### Phase 2: Analytics & Dynamic Visualization Engine
* **Duration:** Week 3
* **Descriptive Analytics:** Automatically compute distributions, temporal trends, correlations, top/bottom performers, and cross-category comparisons.
* **Dynamic Visualization:** Map dataset characteristics directly to visualization types using Plotly:
  * Temporal trends -> Line chart
  * Categorical comparisons -> Bar chart
  * Feature distributions -> Histogram
  * Variable correlations -> Heatmap
  * Proportional compositions -> Donut/Pie chart (restricted to <= 6 slices)

### Phase 3: Multi-Level Anomaly Detection
* **Duration:** Week 4
* Implement a hybrid anomaly detection pipeline combining three complementary methodologies:
  1. **Level 1 (Statistical):** Interquartile Range (IQR) boundary checks.
  2. **Level 2 (Parametric):** Z-score deviation analysis.
  3. **Level 3 (Machine Learning):** Isolation Forest model.
* Compute a unified Anomaly Score (0 to 100), severity tier (Low, Medium, High), and human-readable explanation of why the record was flagged.
* Evaluate performance using Precision, Recall, and F1-score on benchmark datasets.

### Phase 4: Time-Series Forecasting Engine
* **Duration:** Week 5
* Implement multi-model time-series forecasting:
  * Baseline (Naïve / Moving Average)
  * ARIMA (Autoregressive Integrated Moving Average)
  * Prophet (Additive Trend and Seasonality)
* Automatically evaluate models using historical backtesting and select the optimal model based on Mean Absolute Percentage Error (MAPE), MAE, and RMSE.
* Output forecasted values alongside confidence intervals and performance metrics.

### Phase 5: Explainable AI and QA Validation Layer
* **Duration:** Week 6
* **Explainable Insights:** Break down macro changes (such as a 12.4% revenue drop) into exact contributing sub-factors (for example: South Region -6.1%, Product A -3.8%, Customer Segment B -2.5%).
* **QA Validation Layer:** Intercept LLM output before presentation. Perform numeric cross-referencing, calculation checks, contradiction detection, and claim verification against raw statistical results. Assign a overall verification Confidence Score (0 to 100%).

### Phase 6: LLM & Agent Router Architecture
* **Duration:** Week 7
* Implement a decoupled LLM Agent Router.
* The LLM determines user intent, identifies necessary data parameters, and delegates calculation tasks strictly to deterministic Python tools.
* The LLM receives calculated outputs and generates clear explanations without performing arithmetic inline.

### Phase 7: Actionable Recommendation Engine
* **Duration:** Weeks 7-8
* Combine rule-based heuristics with LLM synthesis to generate actionable business recommendations.
* Each recommendation includes a clear rationale, priority level (Low, Medium, High), expected impact, and confidence score.

### Phase 8: Root-Cause and What-If Analysis
* **Duration:** Week 8
* **Root-Cause Analysis:** Trace metric shifts down multi-dimensional trees to identify primary drivers.
* **What-If Analysis:** Allow users to simulate parameter adjustments (such as a 10% increase in sales volume) and estimate the resulting impact on revenue and profit margins.

### Phase 9: User Interface & Multi-Mode Experience
* **Duration:** Week 9
* **Interface Layout:** Redesign the dashboard layout with an Overview panel, Data Management tab, Analytical Insights tab, Forecasting tab, Anomalies view, and Export tab.
* **AI Copilot Sidebar:** Provide an interactive assistant supporting guided prompts (e.g., "Find anomalies", "Forecast next quarter", "Explain revenue drop").
* **Multi-Mode Presentation:**
  * **Student Mode:** Educational output explaining statistical concepts (such as correlation coefficients and p-values).
  * **Professional Mode:** Standard technical metrics and charts for analytical users.
  * **Executive Mode:** High-level narrative summaries focusing on business impact and strategic actions.

### Phase 10: Automated Reports and Presentation Deck Generation
* **Duration:** Week 10
* **Analytical Word Document (.docx):** Generate formal reports containing Executive Summary, Dataset Overview, Quality Scores, KPIs, Trends, Anomalies, Forecasts, Root Causes, Recommendations, and Methodology.
* **PowerPoint Presentation (.pptx):** Generate clean 16:9 widescreen slide decks converting analytical findings into formatted charts, bullet points, and action items using `python-pptx` and `Plotly`.

### Phase 11: Enterprise Integrations
* **Duration:** Weeks 10-11
* **Excel Export:** Export processed datasets, KPIs, anomaly logs, forecasts, and recommendations into formatted `.xlsx` workbooks.
* **Google Sheets API:** Connect directly to Google Sheets for automated reading and writing of analytical outputs.
* **Power BI Bridge:** Export structured analytical outputs as clean datasets formatted for Power BI dashboard consumption.

### Phase 12: Backend Architecture, Database & Deployment
* **Duration:** Weeks 11-12
* **Database Layer:** Deploy PostgreSQL to manage users, uploaded datasets, analysis runs, KPIs, generated insights, recommendations, audit logs, and report history.
* **Backend API (FastAPI):** Expose structured REST endpoints:
  * `POST /upload` - Ingest raw datasets.
  * `POST /analyze` - Trigger full multi-agent analytical pipeline.
  * `GET /analysis/{id}` - Retrieve analysis results.
  * `GET /insights/{id}` - Fetch generated explanations.
  * `GET /forecast/{id}` - Retrieve time-series forecasts.
  * `GET /report/{id}` - Download generated Word report.
  * `GET /ppt/{id}` - Download generated PowerPoint deck.
* **Deployment Stack:** Deploy frontend to Vercel/Streamlit Community Cloud, backend API to Render/Railway, and database to Managed PostgreSQL. Dockerize all services for cloud hosting (AWS / GCP / Azure).

---

## Benchmark Evaluation Framework

To validate system performance, accuracy, and reliability, Agent Analytica 2.0 uses a test suite of 100 to 150 diverse datasets:

| Industry Domain | Dataset Allocation |
| :--- | :--- |
| Sales & Retail | 15 |
| Finance & Banking | 25 |
| Marketing Analytics | 10 |
| Human Resources | 10 |
| E-Commerce | 10 |
| Healthcare | 10 |
| Manufacturing | 10 |
| Supply Chain & Logistics | 10 |
| General Business | 20 |
| **Total Datasets** | **120** |

In addition, 500+ structured test queries with ground-truth mathematical answers, expected evidence, and calculation checks are executed across the dataset pool to benchmark QA validation performance.

---

## Out of Scope (Future Improvements)

To maintain focus and deliver a robust production baseline, the following items are intentionally excluded from the initial version 2.0 release:

* Microservices architecture and Kubernetes orchestration.
* Fine-tuning or pre-training custom LLM weights.
* Deep learning time-series models (LSTM/TFT) prior to baseline stability.
* Complex reinforcement learning algorithms for recommendations.
* Real-time streaming data infrastructure (Kafka/Flink).
* Multi-region distributed cloud infrastructure.

---

## Local Development Setup

### Prerequisites
* Python 3.10 or higher
* Node.js (if running React frontend)
* PostgreSQL database instance

### Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/agent-analytica.git
   cd "agent-analytica"
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/agent_analytica
   LLM_API_KEY=your_api_key_here
   GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
   ```

5. **Launch the application:**
   ```bash
   python run_app.py
   ```
