import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import sys
import os

# Link to surrounding modular architecture 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.validators import run_rule_based_checks
from outputs.chart_builder import build_anomaly_chart

def select_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    num_df = df.select_dtypes(include=[np.number]).copy()
    num_df = num_df.loc[:, ~num_df.columns.str.lower().isin(['id', 'index', 'row_id'])]
    return num_df.fillna(num_df.median(numeric_only=True))

def run_iqr_outliers(df: pd.DataFrame, num_df: pd.DataFrame) -> list:
    """Computes interquartile statistical spikes to find univariate outliers."""
    anomalies = []
    for col in num_df.columns:
        Q1 = num_df[col].quantile(0.25)
        Q3 = num_df[col].quantile(0.75)
        IQR = Q3 - Q1
        if IQR == 0: continue
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        for idx in outliers.index:
            val = df.at[idx, col]
            
            # Extreme variance scoring
            severity = "high" if (val < lower_bound - IQR) or (val > upper_bound + IQR) else "medium"
            anomalies.append({
                "row_id": int(idx),
                "type": "statistical_outlier_iqr",
                "column": col,
                "score": 0.8,
                "severity": severity,
                "reason": f"Value {val:,.2f} radically breaks standard IQR variance bounds."
            })
    return anomalies

def run_isolation_forest(df: pd.DataFrame, num_df: pd.DataFrame) -> list:
    """Utilizes ML (Isolation Forest) to find hidden multivariate relationship anomalies."""
    anomalies = []
    if len(num_df.columns) < 2 or len(num_df) < 20: 
        return anomalies # Data shape is too small for ML context

    try:
        clf = IsolationForest(contamination=0.05, random_state=42)
        preds = clf.fit_predict(num_df)
        scores = clf.decision_function(num_df)
        
        outlier_indices = np.where(preds == -1)[0]
        for i in outlier_indices:
            idx = df.index[i]
            anomalies.append({
                "row_id": int(idx),
                "type": "ml_anomaly_isolation_forest",
                "column": "Multivariate ML Flag",
                "score": round(float(abs(scores[i])), 3),
                "severity": "high",
                "reason": "Isolation Forest flagged this macro-pattern mathematically unusual compared to the overarching data geometry."
            })
    except Exception as e:
        print(f"ML Processing Exception: {e}")
        pass
    
    return anomalies

def merge_and_rank_anomalies(anomalies: list) -> list:
    severity_map = {"high": 3, "medium": 2, "low": 1}
    anomalies.sort(key=lambda x: (severity_map.get(x["severity"], 0), x["score"]), reverse=True)
    
    # Prune identical duplicate flags
    seen = set()
    unique = []
    for a in anomalies:
        identifier = (a["row_id"], a["type"], a["column"])
        if identifier not in seen:
            seen.add(identifier)
            unique.append(a)
    return unique

def summarize_anomalies(anomalies: list) -> dict:
    return {
        "total_anomalies": len(anomalies),
        "high_severity": sum(1 for a in anomalies if a["severity"] == "high"),
        "medium_severity": sum(1 for a in anomalies if a["severity"] == "medium")
    }

def detect_anomalies(df: pd.DataFrame, domain_mode: str = "general") -> dict:
    anomalies = []
    if df is None or df.empty:
         return {"summary": summarize_anomalies([]), "flags": [], "charts": {}}

    # Module 1: Deterministic
    anomalies.extend(run_rule_based_checks(df, domain_mode))
    
    # Module 2 & 3: Statistical & ML
    numeric_df = select_numeric_features(df)
    if not numeric_df.empty:
        anomalies.extend(run_iqr_outliers(df, numeric_df))
        if len(numeric_df.columns) >= 2:
            anomalies.extend(run_isolation_forest(df, numeric_df))
            
    anomalies = merge_and_rank_anomalies(anomalies)
    
    # Module 4: Artifact Generation
    charts = {}
    if anomalies and not numeric_df.empty:
        # Default chart creation leveraging the primary numeric feature
        target_col = numeric_df.columns[0]
        if 'revenue' in [c.lower() for c in numeric_df.columns]:
             target_col = [c for c in numeric_df.columns if 'revenue' in c.lower()][0]
        charts["anomaly_scatter"] = build_anomaly_chart(df, target_col, anomalies)

    return {
        "summary": summarize_anomalies(anomalies),
        "flags": anomalies,
        "charts": charts
    }
