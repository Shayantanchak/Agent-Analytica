import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_anomaly_chart(df: pd.DataFrame, target_column: str, anomalies: list) -> go.Figure:
    """
    Renders a premium AI-themed scatter plot showcasing data points with outliers flagged in crimson.
    """
    fig = go.Figure()
    
    indices = df.index
    values = df[target_column]
    
    # 1. Base Density Plotting
    fig.add_trace(go.Scatter(
        x=indices, 
        y=values, 
        mode='markers',
        name='Nominal Data',
        marker=dict(color='#3B82F6', size=8, opacity=0.5)
    ))

    # 2. Extract specific anomalous vertices
    outlier_indices = []
    for a in anomalies:
        if a["column"] == target_column or a["type"] == "ml_anomaly_isolation_forest":
            outlier_indices.append(a["row_id"])
            
    # Highlight with intense colors
    if outlier_indices:
        # Cross reference index exists in df
        valid_indices = [i for i in outlier_indices if i in df.index]
        outlier_vals = [df.at[i, target_column] for i in valid_indices]
        fig.add_trace(go.Scatter(
            x=valid_indices,
            y=outlier_vals,
            mode='markers',
            name='Critical Anomaly',
            marker=dict(color='#EF4444', size=12, symbol='x', line=dict(width=2, color='white'))
        ))

    fig.update_layout(
        title=f"Anomaly Vector Matrix: {target_column}",
        paper_bgcolor="rgba(15,23,42,0.9)",
        plot_bgcolor="rgba(15,23,42,0.5)",
        font=dict(color="white"),
        xaxis=dict(title="Row ID Stream", gridcolor="#334155"),
        yaxis=dict(title=target_column, gridcolor="#334155"),
        hovermode="closest",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
