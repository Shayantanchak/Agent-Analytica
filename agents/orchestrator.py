from agents.profiler_agent import ProfilerAgent
from agents.cleaning_agent import CleaningAgent
from agents.analysis_agent import AnalysisAgent
from analysis.anomaly_engine import detect_anomalies
from analysis.forecasting import generate_forecast
from agents.narrative_agent import NarrativeAgent
from agents.recommendation_agent import RecommendationAgent
from agents.qa_agent import QAAgent
import pandas as pd

class Orchestrator:
    """
    Phase 6: The AI Orchestrator
    Manages the complete end-to-end data lifecycle connecting all agents and engines.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        
    def run_pipeline(self, df: pd.DataFrame, query: str = None) -> dict:
        """
        Executes the entire agentic pipeline automatically.
        """
        # Phase 0.1: Profiling
        profiler = ProfilerAgent()
        profile_res = profiler.execute(df.copy())
        
        # Phase 0.2: Cleaning & Normalization
        cleaner = CleaningAgent()
        df_cleaned, cleaning_log = cleaner.execute(df.copy())
        
        # Phase 2: Anomaly Engine
        anomalies = detect_anomalies(df_cleaned)
        
        # Phase 3.1: Statistical Forecasting Model
        forecast = generate_forecast(df_cleaned)
        
        # Phase 3.2: LLM Analysis & Insight Narrative
        analysis = AnalysisAgent(api_key=self.api_key).execute(df_cleaned, query)
        
        # Phase 1: Zero-Trust QA Validation (Run post-analysis to validate generated claims against ground truth)
        qa = QAAgent().execute(analysis, df_cleaned)
        
        # Phase 4: Explainable Insights (Lineage Tracer)
        narrative = NarrativeAgent(api_key=self.api_key).generate_explanation(analysis, anomalies, forecast)
        
        # Phase 5: Recommendation Engine (Actionable Next Steps)
        recs = RecommendationAgent(api_key=self.api_key).execute(anomalies, forecast)
        
        # Unified State Artifact
        pipeline_results = {
            "dataset_cleaned": df_cleaned,
            "metrics": {
                "profile": profile_res,
                "analysis": analysis,
                "qa_layer": qa
            },
            "insights": {
                "anomalies": anomalies,
                "forecast": forecast,
            },
            "actionable_intelligence": {
                "explainability": narrative,
                "recommendations": recs
            }
        }
        
        return pipeline_results
