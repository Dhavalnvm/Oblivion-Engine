# core/ai_ml/pipelines.py
"""
ML pipeline orchestration.
"""

import logging
from datetime import datetime
import pickle
import os


class MLPipeline:
    """Manages ML model training and deployment pipeline."""

    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(model_dir, exist_ok=True)

    def run_training_pipeline(self, data, model_type="delay_predictor"):
        """Run complete training pipeline."""
        self.logger.info(f"Starting {model_type} training pipeline")

        try:
            # Data validation
            if data.empty:
                raise ValueError("No training data provided")

            # Model training
            if model_type == "delay_predictor":
                from .prediction import DelayPredictor
                model = DelayPredictor()
                score = model.train(data)

                if score and score > 0.5:  # Minimum acceptable score
                    self._save_model(model, model_type)
                    self.logger.info(f"Model saved with score: {score:.3f}")
                    return True

            return False
        except Exception as e:
            self.logger.error(f"Training pipeline failed: {e}")
            return False

    def load_model(self, model_type):
        """Load trained model."""
        model_path = os.path.join(self.model_dir, f"{model_type}.pkl")

        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            self.logger.info(f"Model {model_type} loaded successfully")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load model {model_type}: {e}")
            return None

    def _save_model(self, model, model_type):
        """Save trained model."""
        model_path = os.path.join(self.model_dir, f"{model_type}.pkl")

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        # Save metadata
        metadata = {
            'model_type': model_type,
            'created_at': datetime.now(),
            'version': '1.0'
        }

        metadata_path = os.path.join(self.model_dir, f"{model_type}_metadata.pkl")
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)


