import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

def detect_time_column(df):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col
    
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower() or 'month' in col.lower() or 'year' in col.lower():
            try:
                # Try to cast to datetime without setting entirely to NaT
                temp = pd.to_datetime(df[col], errors='coerce')
                if temp.notna().sum() > len(df) * 0.5: # If mostly parsed
                    df[col] = temp
                    return col
            except:
                pass
    return None

def generate_forecast(df: pd.DataFrame, target_col: str = None, periods: int = 5) -> dict:
    """
    Generates a forecast for a target numeric column across a detected time column.
    """
    time_col = detect_time_column(df.copy())
    if not time_col:
        return {"error": "No valid time component found to anchor forecast"}
        
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return {"error": "No numeric columns to forecast."}
        
    if not target_col or target_col not in num_df.columns:
        if 'revenue' in [c.lower() for c in num_df.columns]:
            target_col = [c for c in num_df.columns if 'revenue' in c.lower()][0]
        else:
            target_col = num_df.columns[0]
        
    # Standardize time grouping
    try:
        df[time_col] = pd.to_datetime(df[time_col])
    except:
        return {"error": "Time column format irregular."}
        
    df_ts = df.groupby(time_col)[target_col].sum().reset_index()
    df_ts = df_ts.sort_values(by=time_col).dropna()
    
    if len(df_ts) < 3:
        return {"error": "Insufficient data points for forecasting."}
    
    df_ts['time_idx'] = np.arange(len(df_ts))
    X = df_ts[['time_idx']]
    y = df_ts[target_col]
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_X = pd.DataFrame({'time_idx': np.arange(len(df_ts), len(df_ts) + periods)})
    future_y = model.predict(future_X)
    
    last_date = df_ts[time_col].iloc[-1]
    
    # Generate future dates incrementally
    time_diff = df_ts[time_col].diff().median()
    if pd.isna(time_diff):
        time_diff = pd.Timedelta(days=1)
        
    future_dates = [last_date + (time_diff * i) for i in range(1, periods + 1)]
    
    predictions = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Value': future_y
    })
    
    # Calculate simple confidence bounds using residuals
    residuals = y - model.predict(X)
    std_residual = np.std(residuals)
    predictions['Lower_Bound'] = predictions['Predicted_Value'] - (1.96 * std_residual)
    predictions['Upper_Bound'] = predictions['Predicted_Value'] + (1.96 * std_residual)
    
    return {
        "target": target_col,
        "time_col": time_col,
        "historical_count": len(df_ts),
        "forecast": predictions.to_dict(orient='records'),
        "model": "Linear Regression Trend",
        "explanation": f"Leveraged linear time progression modeling across {target_col} mapped to {time_col}."
    }
