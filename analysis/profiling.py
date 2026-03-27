import pandas as pd
import numpy as np

def generate_profile(df: pd.DataFrame) -> dict:
    profile = {}
    profile["total_rows"] = len(df)
    profile["total_cols"] = len(df.columns)
    profile["duplicates"] = df.duplicated().sum()
    
    # Missing values
    missing_counts = df.isna().sum()
    profile["total_missing"] = missing_counts.sum()
    profile["columns_with_missing"] = missing_counts[missing_counts > 0].to_dict()
    
    # Schema and Outliers
    schema = []
    total_outliers = 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        unique_count = df[col].nunique(dropna=True)
        
        # Outlier tracking
        outlier_count = 0
        if col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outlier_count = int(((df[col] < lower_bound) | (df[col] > upper_bound)).sum())
            total_outliers += outlier_count
            
        schema.append({
            "column": col,
            "type": col_type,
            "unique_values": unique_count,
            "missing_values": missing_counts[col],
            "outliers": outlier_count
        })
    profile["schema"] = pd.DataFrame(schema)
    profile["total_outliers"] = total_outliers
    
    # Data Quality Score (0-100)
    # Deduct points for duplicates, missing values, and outliers
    dup_percent = profile["duplicates"] / profile["total_rows"] if profile["total_rows"] > 0 else 0
    missing_percent = profile["total_missing"] / (profile["total_rows"] * profile["total_cols"]) if profile["total_rows"] > 0 else 0
    outlier_percent = profile["total_outliers"] / (profile["total_rows"] * len(numeric_cols)) if profile["total_rows"] > 0 and len(numeric_cols) > 0 else 0
    
    score = 100 - (dup_percent * 100) - (missing_percent * 100) - (outlier_percent * 20)
    profile["quality_score"] = max(0, round(score, 2))
    
    return profile
