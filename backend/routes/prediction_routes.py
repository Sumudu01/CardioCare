from flask import Blueprint, request, jsonify
from services.prediction_service import PredictionService

prediction_bp = Blueprint('prediction', __name__)
prediction_service = PredictionService()

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    try:
        print("Received prediction request")
        data = request.get_json()
        print(f"Request data: {data}")

        if not data:
            print("No input data provided")
            return jsonify({'error': 'No input data provided'}), 400

        # Validate required fields (basic validation)
        required_fields = ['age', 'gender_Male']  # At minimum
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400

        print("Making prediction...")
        # Make prediction
        result = prediction_service.predict(data)
        print(f"Prediction result: {result}")

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in prediction route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500