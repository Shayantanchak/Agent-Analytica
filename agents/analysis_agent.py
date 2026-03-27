import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

class AnalysisAgent:
    """
    Phase 3: Natural Language Analysis & KPI Generation
    Connects to the OpenAI API explicitly to generate deep, contextual business insights 
    based on the structural metrics of the loaded dataframe.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    def execute(self, df: pd.DataFrame, query: str = None) -> dict:
        results = {
            "kpis": {},
            "charts": {},
            "narrative": ""
        }
        
        num_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(num_cols) == 0:
            results["narrative"] = "❌ No numeric columns detected to run KPI analysis."
            return results

        # --- 1. QUANTITATIVE ENGINE (PANDAS BASELINE) ---
        primary_metric = num_cols[-1]
        if 'revenue' in [c.lower() for c in num_cols]:
            primary_metric = [c for c in num_cols if 'revenue' in c.lower()][0]
            
        total_val = df[primary_metric].sum()
        avg_val = df[primary_metric].mean()
        max_val = df[primary_metric].max()
        
        results["kpis"][f"Total {primary_metric.title()}"] = f"{total_val:,.2f}"
        results["kpis"][f"Average {primary_metric.title()}"] = f"{avg_val:,.2f}"
        results["kpis"][f"Max {primary_metric.title()}"] = f"{max_val:,.2f}"
        
        cat_cols = df.select_dtypes(include=['object', 'category', 'string']).columns
        agg_df = None
        top_cat_data = ""
        
        if len(cat_cols) > 0:
            primary_cat = cat_cols[-1]
            if 'category' in [c.lower() for c in cat_cols]:
                primary_cat = [c for c in cat_cols if 'category' in c.lower()][0]

            agg_df = df.groupby(primary_cat)[primary_metric].sum().reset_index()
            agg_df = agg_df.sort_values(by=primary_metric, ascending=False).head(10)
            
            fig = px.bar(agg_df, x=primary_cat, y=primary_metric, 
                         title=f"Top 10 {primary_cat.title()} by {primary_metric.title()}",
                         color=primary_metric, color_continuous_scale="Blues")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
            results["charts"]["main_bar"] = fig
            
            if len(agg_df) > 1:
                fig2 = px.pie(agg_df.head(5), names=primary_cat, values=primary_metric, 
                              title=f"Top {primary_cat.title()} Share")
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
                results["charts"]["distribution_pie"] = fig2
                
            top_cat_data = f"Top Performing {primary_cat.title()}: {agg_df.iloc[0][primary_cat]} with {agg_df.iloc[0][primary_metric]:,.2f}."

        # --- 2. QUALITATIVE AGENT (OPENAI GPT-4 SYSTEM PROMPTS) ---
        user_query = query if query and query.strip() != "" else "Please summarize the core business insights and highlight any potential risks or anomalies based on these metrics."
        
        # Check if a legitimate API Key string is provided
        if self.api_key and len(self.api_key.strip()) > 10 and self.api_key.lower() != "test":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                
                # --- The Prompt Engineering Core ---
                # We package the mathematical outputs directly into the prompt context to prevent hallucination!
                system_prompt = f"""You are Analytica, an elite Senior Data Analyst AI designed to assist executives.
Your job is to read raw mathematical data outputs and user queries, and write a brilliant, boardroom-ready Executive Summary.

### Data Context Extracted from Engine:
- Total Dataset Rows Evaluated: {len(df)}
- Primary Tracked Metric: {primary_metric.title()}
- Total Aggregation for Primary Metric: {total_val:,.2f}
- Average Aggregation: {avg_val:,.2f}
- Maximum Single Value Detected: {max_val:,.2f}
- {top_cat_data}

### Strict Instructions:
1. Answer the user's specific business query based STRICTLY on the Data Context provided above.
2. If the user asks a question the data context cannot answer (e.g. historical dates not provided), explicitly state that you lack that context.
3. Write your output clearly using markdown bullet points. Format all numbers with commas. 
4. DO NOT hallucinate numbers! Only use data explicitly provided in the Context window.
5. Provide actionable, strategic recommendations at the end based on your findings.
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # Using 3.5 turbo to guarantee speed and low latency for MVP tests
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.3, # Extremely low temperature enforces strict analytical consistency
                    max_tokens=600
                )
                
                ai_text = response.choices[0].message.content
                results["narrative"] = f"### 🧠 Native Agentic Summary\n\n> *Query: {user_query}*\n\n{ai_text}"
                
            except Exception as e:
                # Failsafe if the API Key is invalid or rate limited
                results["narrative"] = f"❌ **OpenAI API Exception Intercepted:**\n\n`{str(e)}`\n\n*Please ensure your API key starts with 'sk-' and has valid billing limits assigned.*"
        else:
            # Fallback algorithmic heuristic if no valid key is provided (Simulation Mode)
            narrative = f"### 🧠 Simulated Insights Summary\n\n"
            narrative += f"- **Primary Tracking Metric:** The dataset's primary numeric metric appears to be `{primary_metric.title()}`, with a total sum of **{total_val:,.2f}**.\n"
            if agg_df is not None and not agg_df.empty:
                top_cat = agg_df.iloc[0][primary_cat]
                top_val = agg_df.iloc[0][primary_metric]
                percent = (top_val / total_val) * 100 if total_val > 0 else 0
                narrative += f"- **Top Performer:** The highest performing category in `{primary_cat.title()}` is **{top_cat}**, contributing **{top_val:,.2f}** ({percent:.1f}% of the total tracked).\n"
            
            narrative += f"\n> *⚠️ Displaying fallback heuristics. An authentic OpenAI API Key (sk-...) was not detected in the Settings panel.*"
            results["narrative"] = narrative

        return results
