import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True

    # MongoDB settings
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/cardio_care'

    # Model path
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'ml_model.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'scaler.pkl')