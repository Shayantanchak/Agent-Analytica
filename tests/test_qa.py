import pandas as pd
import json
import sys
import os

# Add parent directory to path to allow importing from the root qa module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from qa.qa_engine import QAEngine

def run_test():
    print("=============================================")
    print(" 🛠️ Commencing Phase 1 QA Validation Test...")
    print("=============================================\n")

    # 1. Build a Mock Pandas DataFrame
    data = {
        'Revenue': [1000, 1100, 1200, 1300, None], # Sum = 4600
        'Profit': [200, 150, 100, 50, -50]         # Sum = 450
    }
    clean_df = pd.DataFrame(data)
    print(">> Mock Data Loaded: 5 rows (Revenue, Profit) including 1 Missing Value.")

    # 2. Build Mock KPIs
    kpis = {
        "Total Revenue": "4,600.00", # Should PASS (perfect float match)
        "Total Profit": "1,000.00",  # Should FAIL (actual is 450)
    }
    print(f">> Executing KPI Math Checks on: {kpis}")

    # 3. Build Mock Trends (Revenue Up, but Profit Down)
    trends = {
        "direction": "up",      
        "revenue_trend": "up",  
        "profit_trend": "down"  
    }

    # 4. Build a Mock Hallucinated Narrative from the AI
    # (Using the unverified number "9,999")
    insights = "The business saw a wonderful increase in revenue. The flagship store generated 9,999 new customers."
    print(">> Scanning Narrative for Trends & Hallucinated Claims...")

    # 5. Build Mock Forecast
    forecast = {
        "confidence_note": "A highly negative downturn is expected in Q4."
    }

    # Execute the Engine!
    engine = QAEngine()
    report = engine.run_qa_checks(clean_df, kpis, trends, insights, forecast)
    
    print("\n✅ QA Pipeline Executed... Printing the Structured Output Schema:\n")
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    run_test()
