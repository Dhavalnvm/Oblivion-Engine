# core/ai_ml/prediction.py
"""
Machine learning prediction models.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import logging


class DelayPredictor:
    """Predicts train delays using machine learning."""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self.logger = logging.getLogger(__name__)

    def train(self, historical_data):
        """Train the delay prediction model."""
        try:
            # Feature engineering
            features = self._extract_features(historical_data)
            targets = historical_data['delay_minutes']

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, targets, test_size=0.2, random_state=42
            )

            # Train model
            self.model.fit(X_train, y_train)
            self.is_trained = True

            # Evaluate
            score = self.model.score(X_test, y_test)
            self.logger.info(f"Model trained with R² score: {score:.3f}")

            return score
        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            return None

    def predict_delay(self, train_data):
        """Predict delay for a train."""
        if not self.is_trained:
            return 0

        try:
            features = self._extract_features(pd.DataFrame([train_data]))
            prediction = self.model.predict(features)[0]
            return max(0, prediction)  # No negative delays
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            return 0

    def _extract_features(self, data):
        """Extract features for ML model."""
        features = pd.DataFrame()

        # Time-based features
        data['hour'] = pd.to_datetime(data['arrival_time']).dt.hour
        data['day_of_week'] = pd.to_datetime(data['arrival_time']).dt.dayofweek

        features['hour'] = data['hour']
        features['day_of_week'] = data['day_of_week']
        features['is_weekend'] = (data['day_of_week'] >= 5).astype(int)

        # Add more features as needed
        return features.fillna(0)


