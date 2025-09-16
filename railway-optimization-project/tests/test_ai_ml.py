# tests/test_ai_ml.py
"""
Tests for AI/ML components.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ai_ml.prediction import DelayPredictor


class TestAIML(unittest.TestCase):
    """Test AI/ML functionality."""

    def setUp(self):
        self.predictor = DelayPredictor()

    def test_delay_prediction_training(self):
        """Test delay predictor training."""
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 100

        data = pd.DataFrame({
            'train_id': [f'T{i:03d}' for i in range(n_samples)],
            'arrival_time': [
                datetime.now() + timedelta(hours=i / 10) for i in range(n_samples)
            ],
            'delay_minutes': np.random.exponential(5, n_samples)  # Exponential delays
        })

        # Train model
        score = self.predictor.train(data)

        # Check training success
        self.assertIsNotNone(score)
        self.assertTrue(self.predictor.is_trained)

    def test_delay_prediction(self):
        """Test delay prediction after training."""
        # Create training data
        np.random.seed(42)
        n_samples = 50

        data = pd.DataFrame({
            'train_id': [f'T{i:03d}' for i in range(n_samples)],
            'arrival_time': [
                datetime.now() + timedelta(hours=i / 10) for i in range(n_samples)
            ],
            'delay_minutes': np.random.exponential(3, n_samples)
        })

        # Train and predict
        self.predictor.train(data)

        test_data = {
            'train_id': 'T999',
            'arrival_time': datetime.now() + timedelta(hours=2)
        }

        prediction = self.predictor.predict_delay(test_data)

        # Check prediction is reasonable
        self.assertIsInstance(prediction, (int, float))
        self.assertGreaterEqual(prediction, 0)


if __name__ == '__main__':
    unittest.main()

