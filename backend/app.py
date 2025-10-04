import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from config import Config
from routes.prediction_routes import prediction_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    print("Registering prediction blueprint...")
    app.register_blueprint(prediction_bp, url_prefix='/api')
    print("Blueprint registered successfully")

    @app.route('/')
    def index():
        return {'message': 'CardioCare API is running'}

    # List all routes for debugging
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    print("App initialization complete!")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)