import pandas as pd
import sys
import os

# Add parent directory to path to allow importing from analysis module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analysis.cleaning import clean_data

class CleaningAgent:
    """
    Phase 2 Agent responsible for executing automated data cleaning pipelines.
    Handles missing values, duplicate removal, format normalization, and outlier capping.
    """
    def __init__(self):
        pass

    def execute(self, df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
        """
        Executes the automated cleaning engine and returns the cleaned dataframe 
        along with a transparent change log.
        """
        return clean_data(df)
