import pandas as pd
import requests
import logging

class PowerBIConnector:
    """
    Phase 9: Power BI REST Integration
    Transmits final processed semantic models natively to Power BI Services.
    """
    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
    def push_dataset(self, dataset_id: str, table_name: str, df: pd.DataFrame):
        """
        Pushes a DataFrame as rows into an existing PowerBI Push Dataset.
        """
        if not self.access_token or self.access_token == "sim":
             logging.warning("POWERBI SYNC: Simulating API Push. No token provided.")
             return {"status": "simulated", "message": "Simulated push to PowerBI Streaming Dataset."}
             
        # Power BI Push Row Endpoint Format
        endpoint = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables/{table_name}/rows"
        
        # Convert DataFrame to PBI JSON format
        # Note: Datetime columns should be standardized to ISO format before pushing
        payload = {"rows": df.to_dict(orient="records")}
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return {"status": "success", "message": "Data stream successfully appended to PowerBI."}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"PowerBI API Fault: {str(e)}"}
