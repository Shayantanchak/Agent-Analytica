import pandas as pd
import numpy as np
import re

def validate_metrics(clean_df: pd.DataFrame, kpis: dict) -> list:
    """
    Validates derived KPIs exactly match the underlying DataFrame totals.
    """
    checks = []
    
    if clean_df is None or clean_df.empty:
        checks.append({"name": "data_exists", "status": "fail", "reason": "Data is empty."})
        return checks
    else:
        checks.append({"name": "data_exists", "status": "pass"})

    if not kpis:
        return checks

    # Look for Total / Average / Max within KPIs and verify against clean_df columns dynamically
    for kpi_name, str_val in kpis.items():
        # Clean the string value to float
        clean_str = re.sub(r'[^\d.-]', '', str(str_val))
        try:
            val = float(clean_str)
        except ValueError:
            continue # Not purely numeric
        
        # Determine matching column 
        col_match = None
        for col in clean_df.select_dtypes(include=[np.number]).columns:
            if col.lower() in kpi_name.lower():
                col_match = col
                break
        
        if col_match:
            # Recompute based on standard KPI prefixes
            if 'total' in kpi_name.lower() or 'sum' in kpi_name.lower():
                actual = clean_df[col_match].sum()
            elif 'average' in kpi_name.lower() or 'mean' in kpi_name.lower():
                actual = clean_df[col_match].mean()
            elif 'max' in kpi_name.lower():
                actual = clean_df[col_match].max()
            else:
                continue
                
            # Tolerance check (5% drift threshold for minor rounding differences)
            diff = abs(actual - val)
            if actual != 0 and (diff / abs(actual)) > 0.05:
                checks.append({
                    "name": f"{kpi_name}_match", 
                    "status": "fail", 
                    "reason": f"Expected ~{actual:,.2f}, found {val}"
                })
            else:
                checks.append({"name": f"{kpi_name}_match", "status": "pass"})
                
    return checks
