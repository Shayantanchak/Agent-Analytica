import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    cleaned_df = df.copy()
    change_log = []
    
    # 0. Format Normalization (Column Names)
    import re
    old_cols = cleaned_df.columns.tolist()
    cleaned_df.columns = [re.sub(r'\W+', '_', str(c).strip().lower()).strip('_') for c in cleaned_df.columns]
    changed_cols = sum([1 for o, n in zip(old_cols, cleaned_df.columns) if o != n])
    if changed_cols > 0:
        change_log.append(f"Standardized {changed_cols} column names to snake_case.")
        
    # 1. Remove duplicates
    initial_rows = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates()
    dropped_dups = initial_rows - len(cleaned_df)
    if dropped_dups > 0:
        change_log.append(f"Removed {dropped_dups} duplicate rows.")
        
    # 2. Trim string spaces
    str_cols = cleaned_df.select_dtypes(include=['object', 'string']).columns
    for col in str_cols:
        # Check if the column contains only strings to avoid applying strip to numeric/floats
        if cleaned_df[col].apply(type).eq(str).any():
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    if len(str_cols) > 0:
        change_log.append(f"Trimmed leading/trailing spaces across {len(str_cols)} text columns.")
        
    # 3. Impute missing values
    numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing = cleaned_df[col].isna().sum()
        if missing > 0:
            median_val = cleaned_df[col].median()
            # If median is nan, use 0
            if pd.isna(median_val): median_val = 0
            cleaned_df[col] = cleaned_df[col].fillna(median_val)
            change_log.append(f"Imputed {missing} missing values in '{col}' with median ({median_val}).")
            
    cat_cols = cleaned_df.select_dtypes(exclude=[np.number]).columns
    for col in cat_cols:
        missing = cleaned_df[col].isna().sum()
        if missing > 0:
            mode_series = cleaned_df[col].mode()
            mode_val = mode_series[0] if not mode_series.empty else "Unknown"
            cleaned_df[col] = cleaned_df[col].fillna(mode_val)
            change_log.append(f"Imputed {missing} missing values in '{col}' with mode ('{mode_val}').")
            
    # 4. Outlier Capping (Using IQR bounds)
    outlier_capped_count = 0
    for col in numeric_cols:
        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_to_cap = ((cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound))
        if outliers_to_cap.sum() > 0:
            cleaned_df.loc[cleaned_df[col] < lower_bound, col] = lower_bound
            cleaned_df.loc[cleaned_df[col] > upper_bound, col] = upper_bound
            outlier_capped_count += outliers_to_cap.sum()
            
    if outlier_capped_count > 0:
        change_log.append(f"Capped {outlier_capped_count} extreme outlier values across numeric columns using IQR bounds.")
            
    # 5. Infer more datetime columns if they look like dates (simplistic for MVP)
    date_cols = [c for c in cleaned_df.columns if 'date' in c.lower()]
    for col in date_cols:
        if cleaned_df[col].dtype == 'object':
            try:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
                change_log.append(f"Parsed column '{col}' to datetime format.")
            except Exception:
                pass

    if not change_log:
        change_log.append("No cleaning actions were necessary; dataset is already clean.")
        
    return cleaned_df, change_log
