# CardioCare - Heart Attack Prediction System

## Overview

CardioCare is a comprehensive heart attack prediction software solution that leverages data mining and machine learning techniques to analyze health data and predict the risk of heart attacks. The system uses real-world datasets to train predictive models, providing valuable insights for early detection and prevention.

## Features

- **Machine Learning Models**: Utilizes various data mining and machine learning algorithms trained on real-world health datasets
- **Web Interface**: User-friendly Streamlit-based frontend for easy interaction
- **RESTful API**: Flask-powered backend for robust data processing and model serving
- **Data Persistence**: MongoDB integration for efficient data storage and retrieval
- **Predictive Analytics**: Real-time heart attack risk assessment based on user input

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: Streamlit (Python data app framework)
- **Database**: MongoDB (NoSQL database)
- **Machine Learning**: Scikit-learn, Pandas, NumPy (Python libraries)
- **Data Mining**: Various algorithms for pattern discovery and predictive modeling

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CardioCare
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   - Install and start MongoDB on your system
   - Update database connection settings in the configuration files

4. **Configure environment variables**:
   - Create a `.env` file with necessary environment variables (API keys, database URLs, etc.)

## Usage

### Running the Application

1. **Start the Flask backend**:
   ```bash
   python app.py
   ```

2. **Launch the Streamlit frontend**:
   ```bash
   streamlit run frontend.py
   ```

3. **Access the application**:
   - Open your browser and navigate to the Streamlit app URL (usually `http://localhost:8501`)

### API Endpoints

- `POST /predict`: Submit health data for heart attack risk prediction
- `GET /models`: Retrieve information about available ML models
- `POST /data`: Store new health data in the database

## Dataset

The machine learning models are trained using publicly available real-world datasets such as:
- UCI Heart Disease Dataset
- Framingham Heart Study data
- Other relevant cardiovascular health datasets

## Model Training

To train new models or retrain existing ones:

1. Prepare your dataset in CSV format
2. Run the training script:
   ```bash
   python train_model.py
   ```
3. Models will be saved and integrated into the prediction pipeline

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## Contact

For questions or support, please contact the development team at [email/contact information].