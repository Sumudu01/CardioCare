import joblib
import numpy as np
import os
import sys

# Add the parent directory to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class PredictionService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.scaler = joblib.load(Config.SCALER_PATH)
            print("Model and scaler loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def predict(self, input_data):
        """
        Predict heart attack risk based on input features
        input_data: dict with feature values
        """
        try:
            print(f"Input data received: {input_data}")

            # Expected features in order
            features = [
                'age', 'hypertension', 'diabetes', 'cholesterol_level', 'obesity',
                'waist_circumference', 'sleep_hours', 'fasting_blood_sugar', 'triglycerides',
                'previous_heart_disease', 'medication_usage', 'region_Urban', 'income_level_middle',
                'smoking_status_Never', 'smoking_status_Past', 'smoking_status_Unknown',
                'physical_activity_Low', 'stress_level_Moderate', 'stress_level_moderate',
                'EKG_results_Normal', 'gender_Male'
            ]

            # Extract values in correct order
            feature_values = [input_data.get(feature, 0) for feature in features]
            print(f"Feature values: {feature_values}")

            # Convert to numpy array and scale
            X = np.array(feature_values).reshape(1, -1)
            print(f"Input array shape: {X.shape}")

            X_scaled = self.scaler.transform(X)
            print(f"Scaled array: {X_scaled}")

            # Make prediction
            prediction = self.model.predict(X_scaled)[0]
            probability = self.model.predict_proba(X_scaled)[0][1]  # Probability of positive class

            print(f"Raw prediction: {prediction}, Probability: {probability}")

            result = {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if prediction == 1 else 'Low',
                'message': 'Heart attack risk detected' if prediction == 1 else 'No heart attack risk detected'
            }

            print(f"Final result: {result}")
            return result

        except Exception as e:
            print(f"Error in prediction: {e}")
            import traceback
            traceback.print_exc()
            raise