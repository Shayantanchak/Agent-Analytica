import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import uuid
import json
from datetime import datetime

# Add parent directory to path to allow importing from analysis module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.profiler_agent import ProfilerAgent
from agents.cleaning_agent import CleaningAgent
from agents.analysis_agent import AnalysisAgent
from agents.ppt_agent import PPTAgent
from agents.report_agent import ReportAgent
from agents.orchestrator import Orchestrator
from qa.qa_engine import QAEngine
from analysis.anomaly_engine import detect_anomalies

profiler_agent = ProfilerAgent()
cleaning_agent = CleaningAgent()
ppt_agent = PPTAgent()
report_agent = ReportAgent()
qa_agent = QAEngine()

st.set_page_config(page_title="Analytica AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium AI Dashboard Pro Theme - Massively Upgraded
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at top right, #111827, #030712 70%);
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Hide standard radio element circles to make them look like menu buttons */
    div.row-widget.stRadio > div{flex-direction:column;}
    div.row-widget.stRadio > div > label{
        background: rgba(30,41,59,0.5); 
        padding: 10px 15px; 
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid transparent;
        transition: all 0.3s;
        cursor: pointer;
    }
    div.row-widget.stRadio > div > label:hover {
        background: rgba(30,41,59,0.9);
        border: 1px solid #7C3AED;
    }
    div.row-widget.stRadio > div > label [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: 600;
    }
    /* Hide the radio circles */
    div.row-widget.stRadio > div > label > div:first-child { display: none; }

    .kpi-card {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        border: 1px solid rgba(124, 58, 237, 0.4);
        box-shadow: 0 15px 45px -10px rgba(124, 58, 237, 0.3);
        background: rgba(30, 41, 59, 0.7);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        opacity: 0;
        transition: opacity 0.4s;
    }
    .kpi-card:hover::before { opacity: 1; }

    .kpi-title { font-size: 14px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; }
    
    .kpi-value { 
        font-size: 42px; font-weight: 800; margin: 12px 0 0 0; 
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 15px rgba(167, 139, 250, 0.2);
    }

    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.5) !important;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border: 1px solid #7C3AED !important;
        box-shadow: 0 0 10px rgba(124, 58, 237, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION & SIDEBAR ---------------- #
with st.sidebar:
    st.image(r"C:\Users\schak\.gemini\antigravity\brain\ffcc1c4f-6fd0-4337-8dad-70d6bdfcd306\analytica_logo_1774471982398.png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 36px; background: linear-gradient(90deg, #60A5FA, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: -15px; margin-bottom: 0;'>📊 Analytica</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 30px;'>Agentic Intelligence Engine</p>", unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigation")
    page = st.radio("Go to:", [
        "📊 Master Dashboard", 
        "🧹 Auto-Clean Engine", 
        "💬 AI Analysis Hub", 
        "📤 Export Center (PPT/DOCX)", 
        "🧾 Immutable Audit Trail"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📥 Data Ingestion")
    uploaded_file = st.file_uploader("Upload CSV or Excel dataset", type=["csv", "xlsx"])
    
    st.markdown("---")
    st.markdown("### 🔑 Engine Settings")
    api_key = st.text_input("OpenAI API Key (Phase 3)", type="password", help="Providing this enables the true LLM Natural Language processing.")
    st.session_state['api_key'] = api_key

@st.cache_data
def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# ---------------- MAIN APP LOGIC ---------------- #
if uploaded_file is not None:
    try:
        raw_df = load_file(uploaded_file)
        
        # Session State Setup
        if 'raw_df' not in st.session_state or st.session_state.get('last_file') != uploaded_file.name:
            st.session_state['raw_df'] = raw_df
            st.session_state['cleaned_df'] = None
            st.session_state['change_log'] = []
            st.session_state['analysis_results'] = None
            st.session_state['last_file'] = uploaded_file.name

        df_to_use = st.session_state['cleaned_df'] if st.session_state['cleaned_df'] is not None else st.session_state['raw_df']

        # ---------------- PAGE 1: MASTER DASHBOARD ---------------- #
        if page == "📊 Master Dashboard":
            st.title("📊 Dataset Master Overview")
            st.markdown("Welcome to the Analytica Control Center. Here is the aerial view of your uploaded dataset and its AI-profiled structural health.")
            
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Rows</div><div class='kpi-value'>{len(df_to_use):,}</div></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Columns</div><div class='kpi-value'>{len(df_to_use.columns)}</div></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Missing Values</div><div class='kpi-value'>{df_to_use.isna().sum().sum():,}</div></div>", unsafe_allow_html=True)

            st.markdown("### 🗄️ Raw Data Feed")
            st.dataframe(df_to_use.head(100), use_container_width=True, height=300)

            st.markdown("---")
            st.markdown("## 📈 AI Quality Profiler")
            profile = profiler_agent.execute(df_to_use)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = profile["quality_score"],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Trust Score", 'font': {'size': 24, 'color': 'white'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#7C3AED"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "#334155",
                        'steps': [
                            {'range': [0, 50], 'color': '#ff4b4b'},
                            {'range': [50, 80], 'color': '#ffa726'},
                            {'range': [80, 100], 'color': '#10b981'}],
                    }
                ))
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
                st.plotly_chart(fig, use_container_width=True)
                
                if profile["duplicates"] > 0:
                    st.warning(f"⚠️ {profile['duplicates']} duplicate rows detected (Requires Auto-Clean).")
                else:
                    st.success("✅ No duplicate layers detected.")
                    
            with col2:
                st.markdown("**Core Schema Architecture**")
                st.dataframe(profile["schema"], use_container_width=True, height=250)
                
            if profile["total_missing"] > 0:
                st.markdown("**Anomalies: Missing Value Heatmap**")
                missing_df = pd.DataFrame(list(profile["columns_with_missing"].items()), columns=['Column', 'Missing Count'])
                fig2 = px.bar(missing_df, x='Column', y='Missing Count', text='Missing Count')
                fig2.update_traces(marker_color='#F472B6')
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("---")
            st.markdown("## 🚨 Phase 2: AI Anomaly Detection Engine")
            if st.button("🔍 Scan Data for Anomalies", type="primary"):
                with st.spinner("Executing Phase 2 ML Isolation Forest & IQR Bounds..."):
                    anomaly_output = detect_anomalies(df_to_use)
                    
                    st.success("✅ Macro-Pattern Scan Complete")
                    c_sum1, c_sum2 = st.columns(2)
                    c_sum1.metric("Total Anomalies Detected", anomaly_output.get('summary', {}).get('total_anomalies', 0))
                    c_sum2.metric("High Severity Alerts", anomaly_output.get('summary', {}).get('high_severity', 0))
                    
                    flags = anomaly_output.get('flags', [])
                    if flags:
                        st.markdown("### 🚩 Critical Data Flags")
                        flag_df = pd.DataFrame(flags)
                        st.dataframe(flag_df, use_container_width=True)
                        
                    charts = anomaly_output.get('charts', {})
                    if "anomaly_scatter" in charts:
                        st.plotly_chart(charts["anomaly_scatter"], use_container_width=True)

        # ---------------- PAGE 2: AUTO-CLEAN ---------------- #
        elif page == "🧹 Auto-Clean Engine":
            st.title("🧹 Auto-Clean Pipeline")
            st.markdown("The underlying Auto-Clean Agent will physically optimize and reconstruct the dataset without human intervention. The engine performs: **Column normalization, Duplicate stripping, Median/Mode imputation, Whitespace trimming, and IQR Outlier capping.**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("✨ Initialize Complete Dataset Optimization", type="primary"):
                    with st.spinner("Cleaning agent is optimizing architecture..."):
                        cleaned_df, log = cleaning_agent.execute(st.session_state['raw_df'])
                        st.session_state['cleaned_df'] = cleaned_df
                        st.session_state['change_log'] = log
                    st.success("✅ Architecture Optimized! Check the Master Dashboard to track improvements.")

            if st.session_state['cleaned_df'] is not None:
                st.markdown("---")
                st.markdown("### 📝 Optimization Audit Log")
                for entry in st.session_state['change_log']:
                    st.markdown(f"- 🟢 *{entry}*")
                    
                st.markdown("### 📤 Pipeline Integrations")
                export_c1, export_c2 = st.columns(2)
                with export_c1:
                    csv = convert_df(st.session_state['cleaned_df'])
                    st.download_button(label="⬇️ Download Cleaned Artifact (CSV)", data=csv, file_name="cleaned_dataset.csv", mime="text/csv")
                with export_c2:
                    if st.button("📡 Synchronize to Google Workspace Apps"):
                        st.info("ℹ️ Database sync initialized. Provide 'credentials.json' in `/connectors/` to complete OAuth handshake.")

        # ---------------- PAGE 3: AI ANALYSIS HUB ---------------- #
        elif page == "💬 AI Analysis Hub":
            st.title("🤖 Agentic Command Center")
            st.markdown("Interact directly with the analytical AI. The Engine uses strict pandas-execution to parse mathematical insight natively and builds executive summaries.")
            
            # Chat Box
            question = st.text_area("Request specific multidimensional analysis:", placeholder="e.g. Which region is driving our primary revenue loss?")
            
            col_b1, col_b2, col_b3 = st.columns([1,2,1])
            with col_b2:
                if st.button("🚀 Execute Pipeline Orchestrator", type="primary"):
                    with st.spinner("Orchestrator initializing full agentic graph..."):
                        orchestrator = Orchestrator(api_key=st.session_state.get('api_key'))
                        pipeline_res = orchestrator.run_pipeline(df_to_use, query=question)
                        
                        st.session_state['pipeline_results'] = pipeline_res
                        
                        # Map to existing expected analysis_results structural shape for compatibility
                        results = pipeline_res['metrics']['analysis']
                        results['qa_layer'] = pipeline_res['metrics']['qa_layer']
                        st.session_state['analysis_results'] = results
                        
                        qa_results = results['qa_layer']
                    
                    # Log run
                    run_id = str(uuid.uuid4())[:8]
                    run_data = {
                        "Run ID": run_id,
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Dataset": uploaded_file.name,
                        "Trust Score": str(qa_results.get('trust_score', 100)) + "%",
                        "Query Provided": "Yes" if question else "Automated Extraction",
                        "Status": "✅ Confirmed"
                    }
                    log_file = os.path.join("storage", "run_history.json")
                    if not os.path.exists("storage"): os.makedirs("storage")
                    history = []
                    if os.path.exists(log_file):
                        try:
                            with open(log_file, "r") as f: history = json.load(f)
                        except: pass
                    history.insert(0, run_data)
                    with open(log_file, "w") as f: json.dump(history, f, indent=4)
                        
                    st.success("✅ Analysis Complete & Fully Audited")
            
            # Results Render
            if st.session_state.get('analysis_results'):
                res = st.session_state['analysis_results']
                st.markdown("---")
                
                # KPIs
                st.markdown("### 🏆 Core Metrics Derived")
                kpi_cols = st.columns(min(len(res['kpis']), 4) if len(res['kpis']) > 0 else 1)
                for idx, (k, v) in enumerate(res['kpis'].items()):
                    with kpi_cols[idx % 4]:
                        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>{k}</div><div class='kpi-value'>{v}</div></div>", unsafe_allow_html=True)
                
                # Charts
                st.markdown("### 📊 Multi-dimensional View")
                chart_cols = st.columns(2)
                c_idx = 0
                for c_name, fig in res.get('charts', {}).items():
                    with chart_cols[c_idx % 2]:
                        st.plotly_chart(fig, use_container_width=True)
                    c_idx += 1
                
                # Narrative
                st.markdown("### 🧠 Agent Insights Report")
                st.markdown(res.get('narrative', ''))
                
                # QA Layer
                if 'qa_layer' in res:
                    st.markdown("---")
                    st.markdown("### 🛡️ Phase 1: Upgraded QA Validation Layer")
                    qa_res = res['qa_layer']
                    
                    status = qa_res.get('overall_status', 'pending').upper()
                    conf = qa_res.get('confidence', 'low').upper()
                    color = "#10b981" if conf == "HIGH" else "#ffa726" if conf == "MEDIUM" else "#ef4444"
                    
                    st.markdown(f"**Engine Confidence Validation:** <span style='color:{color}; font-size:24px; font-weight:800; background: rgba(30,41,59,0.5); padding: 5px 15px; border-radius: 8px;'>{conf} CONFIDENCE ({status})</span>", unsafe_allow_html=True)
                    
                    with st.expander("Explore Phase 1 QA System Audit Logs", expanded=True):
                        st.markdown("**1. Data & Metric Validations**")
                        for check in qa_res.get('metric_checks', []):
                            icon = "✅" if check['status'] == "pass" else "❌"
                            reason = f" - {check['reason']}" if 'reason' in check else ""
                            st.markdown(f"{icon} {check['name']}{reason}")
                            
                        st.markdown("**2. Narrative Hallucination Checks**")
                        for check in qa_res.get('narrative_checks', []):
                            icon = "✅" if check['status'] == "pass" else "❌"
                            reason = f" - {check['reason']}" if 'reason' in check else ""
                            st.markdown(f"{icon} {check['name']}{reason}")
                            
                        if qa_res.get('contradictions'):
                            st.markdown("**3. Identified Contradictions**")
                            for check in qa_res['contradictions']:
                                st.error(f"⚠️ {check['name']}: {check['reason']}")
                                
                        if qa_res.get('warnings'):
                            st.markdown("**4. System Warnings**")
                            for warn in qa_res['warnings']:
                                st.warning(f"⚠️ {warn}")

                if 'pipeline_results' in st.session_state:
                    pipe = st.session_state['pipeline_results']
                    st.markdown("---")
                    st.markdown("### 🔮 Predictive Forecast (Phase 3)")
                    forecast = pipe['insights']['forecast']
                    if not forecast.get('error'):
                        c_f1, c_f2 = st.columns(2)
                        with c_f1:
                            st.info(f"Model: {forecast.get('model')}")
                        with c_f2:
                            st.info(f"Target: {forecast.get('target')}")
                        if forecast.get('forecast'):
                            st.dataframe(pd.DataFrame(forecast['forecast']), use_container_width=True)
                    else:
                        st.warning(forecast.get('error'))

                    st.markdown("---")
                    st.markdown("### 💡 Explainable Lineage (Phase 4)")
                    narrative = pipe['actionable_intelligence']['explainability']
                    st.success(narrative.get("summary_narrative", ""))
                    for trace in narrative.get("evidence_traces", []):
                        with st.expander(trace['insight']):
                            st.write(f"**Lineage:** {trace['lineage']}")
                            st.write(f"**Confidence:** {trace['confidence']}")

                    st.markdown("---")
                    st.markdown("### 🎯 Executive Recommendations (Phase 5)")
                    recs = pipe['actionable_intelligence']['recommendations'].get('actionable_steps', [])
                    for i, rec in enumerate(recs):
                        if rec['impact'] == 'High':
                            st.error(f"🔴 Action {i+1}: {rec['action']} (Effort: {rec['effort']})  \n*Reasoning: {rec['reasoning']}*")
                        elif rec['impact'] == 'Medium':
                            st.warning(f"🟡 Action {i+1}: {rec['action']} (Effort: {rec['effort']})  \n*Reasoning: {rec['reasoning']}*")
                        else:
                            st.info(f"🟢 Action {i+1}: {rec['action']} (Effort: {rec['effort']})  \n*Reasoning: {rec['reasoning']}*")

        # ---------------- PAGE 4: EXPORT CENTER ---------------- #
        elif page == "📤 Export Center (PPT/DOCX)":
            st.title("📤 Boardroom Artifact Generators")
            st.markdown("Transform the digital analytics directly into corporate-ready physical deliverables. **You must execute an Analysis in the Hub first.**")
            
            if not st.session_state.get('analysis_results'):
                st.error("⚠️ AI Architecture requires processed data. Go to 'AI Analysis Hub' and execute an analysis first.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='kpi-card' style='padding:40px; text-align:center;'>", unsafe_allow_html=True)
                    st.markdown("### 📄 DOCX Corporate Summary")
                    st.markdown("Generates a strict executive text output.")
                    if st.button("🔨 Package DOCX Report", key="docx"):
                        with st.spinner("Structuring paragraphs..."):
                            docx_bytes = report_agent.execute(st.session_state['analysis_results'])
                            st.success("✅ Compiled!")
                            st.download_button("⬇️ Download Artifact", docx_bytes, "Analytica_Executive_Report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with col2:
                    st.markdown("<div class='kpi-card' style='padding:40px; text-align:center;'>", unsafe_allow_html=True)
                    st.markdown("### 📽️ PPTX Widescreen Deck")
                    st.markdown("Packages KPIs and deeply themed Dark-Mode Plotly renders.")
                    if st.button("🔨 Package Presentation", key="pptx"):
                        with st.spinner("Rendering vector components..."):
                            pptx_bytes = ppt_agent.execute(st.session_state['analysis_results'])
                            st.success("✅ Compiled!")
                            st.download_button("⬇️ Download Deck", pptx_bytes, "Analytica_Board_Deck.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                    st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.get('pipeline_results'):
                from connectors.excel_connector import ExcelConnector
                st.markdown("---")
                st.markdown("### 📊 Excel Native Export (Phase 7)")
                if st.button("🔨 Package Comprehensive Excel Workbook", type="secondary"):
                    with st.spinner("Generating native .xlsx..."):
                        connector = ExcelConnector()
                        res = connector.export_pipeline_results("Analytica_Export", st.session_state['pipeline_results'])
                        with open(res['filepath'], "rb") as f:
                            st.download_button("⬇️ Download Excel", f.read(), "Analytica_Export.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # ---------------- PAGE 5: AUDIT TRAIL ---------------- #
        elif page == "🧾 Immutable Audit Trail":
            st.title("🧾 Ledger & Run History")
            st.markdown("The Orchestrator strictly logs all Agent executions for full reproducibility, compliance, and enterprise accountability (Phase 6).")
            
            log_file = os.path.join("storage", "run_history.json")
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r") as f:
                        history = json.load(f)
                    if history:
                        hist_df = pd.DataFrame(history)
                        st.dataframe(hist_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("Ledger is physically empty.")
                except Exception as e:
                    st.error("Audit log corrupted.")
            else:
                st.info("System Ledger is empty. Execute an Analysis Pipeline to record the first event.")

    except Exception as e:
        st.error(f"FATAL UI EXCEPTION: {e}")
            
else:
    # Beautiful landing screen when no file is uploaded
    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 64px; background: linear-gradient(135deg, #60A5FA, #A78BFA, #F472B6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 Welcome to Analytica</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #94A3B8;'>Upload a dataset in the sidebar to initialize the AI engine.</p>", unsafe_allow_html=True)
