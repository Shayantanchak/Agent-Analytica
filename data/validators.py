import pandas as pd
import numpy as np

def run_rule_based_checks(df: pd.DataFrame, domain_mode: str) -> list:
    """
    Executes domain-agnostic deterministic sanity checks to find impossible or completely broken data vectors.
    """
    anomalies = []
    
    # Metric limits: Detect conceptually impossible negative business values
    positive_keywords = ['revenue', 'price', 'amount', 'quantity', 'loan', 'sales', 'profit']
    
    for col in df.select_dtypes(include=[np.number]).columns:
        if any(keyword in col.lower() for keyword in positive_keywords):
            # Check for negative bounds, unless profit is acceptable. Assuming 'profit' can be negative but others shouldn't.
            if 'profit' in col.lower():
                continue 
                
            neg_mask = df[col] < 0
            if neg_mask.any():
                for idx in df[neg_mask].index:
                    anomalies.append({
                        "row_id": int(idx),
                        "type": "impossible_value",
                        "column": col,
                        "score": 1.0,
                        "severity": "high",
                        "reason": f"{col} has a negative value ({df.at[idx, col]}), which violates deterministic bounds."
                    })
                    
    # Primary Key Violations: Exact row duplicates
    duplicates = df[df.duplicated(keep=False)]
    if not duplicates.empty:
        for idx in duplicates.index:
            anomalies.append({
                "row_id": int(idx),
                "type": "duplicate_record",
                "column": "Multiple",
                "score": 0.5, 
                "severity": "medium",
                "reason": "Row is a carbon copy of an existing database record."
            })
            
    return anomalies
