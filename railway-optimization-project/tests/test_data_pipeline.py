# tests/test_data_pipeline.py
"""
Tests for data pipeline components.
"""

import unittest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.data_pipeline.collector import DataCollector
from core.data_pipeline.preprocessor import DataPreprocessor


class TestDataPipeline(unittest.TestCase):
    """Test data pipeline functionality."""

    def setUp(self):
        self.collector = DataCollector()
        self.preprocessor = DataPreprocessor()

    def test_data_validation(self):
        """Test data validation logic."""
        # Valid data
        valid_data = pd.DataFrame({
            'train_id': ['T001', 'T002'],
            'arrival_time': [datetime.now(), datetime.now() + timedelta(hours=1)],
            'departure_time': [datetime.now() + timedelta(minutes=30),
                               datetime.now() + timedelta(hours=1, minutes=30)],
            'platform': ['P1', 'P2']
        })

        is_valid, message = self.preprocessor.validate_data(valid_data)
        self.assertTrue(is_valid)

        # Invalid data (missing columns)
        invalid_data = pd.DataFrame({
            'train_id': ['T001'],
            'arrival_time': [datetime.now()]
        })

        is_valid, message = self.preprocessor.validate_data(invalid_data)
        self.assertFalse(is_valid)

    def test_timestamp_cleaning(self):
        """Test timestamp standardization."""
        data = pd.DataFrame({
            'train_id': ['T001'],
            'arrival_time': ['2024-01-01 10:00:00'],
            'departure_time': ['2024-01-01 10:30:00'],
            'platform': ['P1']
        })

        cleaned_data = self.preprocessor.clean_timestamps(data)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_data['arrival_time']))


if __name__ == '__main__':
    unittest.main()

