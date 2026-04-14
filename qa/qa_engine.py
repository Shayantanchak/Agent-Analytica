import pandas as pd
from .qa_models import init_qa_report
from .metric_validator import validate_metrics
from .narrative_validator import validate_narratives
from .chart_validator import validate_chart_inputs
from .contradiction_checker import detect_contradictions
from .confidence_scorer import score_confidence, derive_status

def collect_data_quality_warnings(clean_df: pd.DataFrame, forecast: dict) -> list:
    warnings = []
    if clean_df is not None and not clean_df.empty:
        null_rate = clean_df.isna().sum().sum() / (clean_df.shape[0] * clean_df.shape[1])
        if null_rate > 0.1:
            warnings.append(f"{null_rate*100:.1f}% missing values detected across dataset. Imputations heavily utilized.")
            
        if len(clean_df) < 50:
            warnings.append(f"Statistically small sample size ({len(clean_df)} rows). Confidence may be impaired in macro generation.")
            
    return warnings

class QAEngine:
    """
    The central intelligence orchestrator for Phase 1 Validation.
    Protects downstream modules by preventing unverified data or narratives from exiting the data lake.
    """
    def __init__(self):
        pass
        
    def run_qa_checks(self, clean_df: pd.DataFrame, kpis: dict, trends: dict, insights: str, forecast: dict) -> dict:
        report = init_qa_report()
        
        # Sequentially fire all the module checks securely
        report["metric_checks"] = validate_metrics(clean_df, kpis)
        report["narrative_checks"] = validate_narratives(insights, kpis, trends)
        report["chart_checks"] = validate_chart_inputs(kpis, trends, forecast)
        report["contradictions"] = detect_contradictions(kpis, trends, forecast)
        
        # Calculate heuristics
        report["warnings"] = collect_data_quality_warnings(clean_df, forecast)
        report["confidence"] = score_confidence(report)
        report["overall_status"] = derive_status(report)
        
        return report
