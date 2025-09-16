# core/data_pipeline/preprocessor.py
"""
Data preprocessing and validation module.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class DataPreprocessor:
    """Cleans and validates railway data."""

    def __init__(self):
        self.required_columns = ['train_id', 'arrival_time', 'departure_time', 'platform']

    def validate_data(self, df):
        """Validate data integrity and completeness."""
        if df.empty:
            return False, "Empty dataset"

        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"

        return True, "Data valid"

    def clean_timestamps(self, df):
        """Standardize timestamp formats."""
        for col in ['arrival_time', 'departure_time']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df

    def handle_missing_values(self, df):
        """Handle missing values in train data."""
        # Forward fill platform assignments
        df['platform'] = df['platform'].fillna(method='ffill')

        # Remove rows with missing critical data
        df = df.dropna(subset=['train_id', 'arrival_time'])

        return df


