import pandas as pd
import os

class ExcelConnector:
    """
    Phase 7: Excel Integration
    Exports data, metrics, and models cleanly into native Excel formatting.
    """
    def __init__(self, output_dir="storage/exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export_pipeline_results(self, filename: str, pipeline_results: dict):
        """
        Takes the Orchestrator output and maps it to a multi-sheet Excel Workbook.
        """
        filepath = os.path.join(self.output_dir, f"{filename}.xlsx")
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 1. Base Data
            df = pipeline_results.get("dataset_cleaned")
            if df is not None and not df.empty:
                df.to_excel(writer, sheet_name="Clean Data", index=False)
                
            # 2. Anomalies
            anomalies = pipeline_results.get("insights", {}).get("anomalies", {}).get("flags", [])
            if anomalies:
                pd.DataFrame(anomalies).to_excel(writer, sheet_name="Detected Anomalies", index=False)
                
            # 3. Forecast
            forecast = pipeline_results.get("insights", {}).get("forecast", {}).get("forecast", [])
            if forecast:
                pd.DataFrame(forecast).to_excel(writer, sheet_name="Future Forecast", index=False)
                
            # 4. Actions
            actions = pipeline_results.get("actionable_intelligence", {}).get("recommendations", {}).get("actionable_steps", [])
            if actions:
                pd.DataFrame(actions).to_excel(writer, sheet_name="Strategy Plan", index=False)
                
        return {"status": "success", "filepath": filepath}
