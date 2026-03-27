# 🚀 Analytica

> AI-Powered Multi-Agent Data Analyst for Automated Insights, Reports & Presentations

---

## 🧩 Overview
Analytica is an intelligent, multi-agent data analytics system that transforms raw datasets into decision-ready insights, structured reports, and executive PowerPoint presentations.

It automates the entire analytics pipeline:
**Data ingestion → Cleaning & profiling → KPI analysis → Visualization → Insight generation → Report & PPT creation**

---

## ⚡ Key Features
- 📊 Automated Data Profiling & Cleaning
- 🧠 Multi-Agent Analysis Engine
- 📈 KPI & Trend Detection
- 🚨 Anomaly Detection (IQR Bounds)
- 🧾 Auto Report Generation (DOCX)
- 📽️ PowerPoint Deck Generation (Premium Widescreen UI)
- ✅ QA Validation Layer (Hallucination Mitigation)
- 🔁 Audit Trail & Immutable Run History
- 📡 Google Sheets Integration Ready

---

## 🏗️ Architecture
User → Orchestrator → Data Agents → Analysis Agents → QA Validation → Output Engines (Report + PPT)

### Agents Implemented:
1. **Profiler Agent:** Computes Data Quality Scores and maps schemas.
2. **Cleaning Agent:** Normalizes columns, imputes missing data, caps outliers.
3. **Analysis Agent:** Generates Plotly charts, KPIs, and LLM Narratives.
4. **QA Agent:** Defends against unverified claims via strict numeric cross-referencing.
5. **PPT & Report Agents:** Transforms dictionary outputs into `.pptx` and `.docx` artifacts.

---

## 🧪 Tech Stack
- **Python Backend:** Pandas, NumPy, Scikit-learn
- **Frontend App:** Streamlit (Custom "AI Dashboard Pro" UI Theme)
- **Visualization:** Plotly, Kaleido
- **Generators:** python-pptx, python-docx

---

## 🚀 Getting Started
1. Clone the repository natively.
2. Install the necessary dependencies: `pip install -r requirements.txt` (Ensure `kaleido`, `python-pptx`, and `python-docx` are installed for the generators to work).
3. Start the UI:
   ```bash
   streamlit run app/ui_streamlit.py
   ```
4. Access the portal at `http://localhost:8501`.

---

## 📌 Future Scope
- Power BI & Tableau API integrations
- Real-time live dashboard streams
- Multi-user collaboration with database state tracking

---

## 👨💻 Author
**Shayantan Chakrabarti**  
B.Tech ECS | AI | Data Analytics | Cybersecurity  

---

## ⭐ Star this repo if you like it!
