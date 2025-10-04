import streamlit as st
import requests
import json

# Configure page
st.set_page_config(
    page_title="CardioCare - Heart Attack Prediction",
    page_icon="❤️",
    layout="wide"
)

# Backend API URL
API_URL = "http://localhost:5000/api"

def main():
    st.title("❤️ CardioCare - Heart Attack Prediction System")
    st.markdown("---")

    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Home", "Prediction", "Results", "History"]
    )

    if page == "Home":
        show_home()
    elif page == "Prediction":
        show_prediction()
    elif page == "Results":
        show_results()
    elif page == "History":
        show_history()

def show_home():
    st.header("Welcome to CardioCare")
    st.markdown("""
    CardioCare is an AI-powered heart attack prediction system that uses machine learning
    to assess your risk of heart attack based on various health parameters.

    ### Features:
    - **Advanced ML Model**: Uses Random Forest algorithm trained on comprehensive health data
    - **Real-time Prediction**: Get instant risk assessment
    - **User-friendly Interface**: Easy-to-use web interface
    - **Comprehensive Analysis**: Considers multiple health factors

    ### How it works:
    1. Fill in your health information in the Prediction section
    2. Our AI model analyzes your data
    3. Receive your heart attack risk assessment

    **⚠️ Disclaimer**: This tool is for educational purposes only and should not replace professional medical advice.
    """)

def show_prediction():
    st.header("Heart Attack Risk Prediction")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Personal Information")
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            region = st.selectbox("Region", ["Urban", "Rural"])

        with col2:
            st.subheader("Health Conditions")
            hypertension = st.checkbox("Hypertension")
            diabetes = st.checkbox("Diabetes")
            previous_heart_disease = st.checkbox("Previous Heart Disease")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Measurements")
            cholesterol_level = st.number_input("Cholesterol Level (mg/dL)", min_value=100, max_value=600, value=200)
            waist_circumference = st.number_input("Waist Circumference (cm)", min_value=50, max_value=200, value=80)
            triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=1000, value=150)

        with col4:
            st.subheader("Lifestyle Factors")
            obesity = st.checkbox("Obesity")
            smoking_status = st.selectbox("Smoking Status", ["Never", "Past", "Current", "Unknown"])
            physical_activity = st.selectbox("Physical Activity Level", ["High", "Moderate", "Low"])
            stress_level = st.selectbox("Stress Level", ["Low", "Moderate", "High"])

        col5, col6 = st.columns(2)

        with col5:
            sleep_hours = st.slider("Sleep Hours per Night", 0.0, 12.0, 7.0)
            fasting_blood_sugar = st.number_input("Fasting Blood Sugar (mg/dL)", min_value=50, max_value=500, value=90)
            medication_usage = st.checkbox("Currently Taking Heart-related Medication")

        with col6:
            income_level = st.selectbox("Income Level", ["Low", "Middle", "High"])
            ekg_results = st.selectbox("EKG Results", ["Normal", "Abnormal"])

        submitted = st.form_submit_button("Predict Heart Attack Risk")

        if submitted:
            # Prepare data for API
            data = {
                "age": age,
                "hypertension": 1 if hypertension else 0,
                "diabetes": 1 if diabetes else 0,
                "cholesterol_level": cholesterol_level,
                "obesity": 1 if obesity else 0,
                "waist_circumference": waist_circumference,
                "sleep_hours": sleep_hours,
                "fasting_blood_sugar": fasting_blood_sugar,
                "triglycerides": triglycerides,
                "previous_heart_disease": 1 if previous_heart_disease else 0,
                "medication_usage": 1 if medication_usage else 0,
                "region_Urban": 1 if region == "Urban" else 0,
                "income_level_middle": 1 if income_level == "Middle" else 0,
                "smoking_status_Never": 1 if smoking_status == "Never" else 0,
                "smoking_status_Past": 1 if smoking_status == "Past" else 0,
                "smoking_status_Unknown": 1 if smoking_status == "Unknown" else 0,
                "physical_activity_Low": 1 if physical_activity == "Low" else 0,
                "stress_level_Moderate": 1 if stress_level == "Moderate" else 0,
                "stress_level_moderate": 1 if stress_level == "Moderate" else 0,  # Duplicate for compatibility
                "EKG_results_Normal": 1 if ekg_results == "Normal" else 0,
                "gender_Male": 1 if gender == "Male" else 0
            }

            # Store data in session state for results page
            st.session_state.prediction_data = data
            st.session_state.prediction_submitted = True

            # Show loading spinner
            with st.spinner("Analyzing your health data..."):
                # Make API call
                try:
                    st.write(f"Connecting to API: {API_URL}/predict")
                    response = requests.post(f"{API_URL}/predict", json=data, timeout=10)

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.prediction_result = result

                        # Display immediate result
                        st.success("✅ Prediction completed successfully!")

                        # Show quick result summary
                        if result['prediction'] == 1:
                            st.error(f"⚠️ **HIGH RISK**: {result['message']}")
                        else:
                            st.success(f"✅ **LOW RISK**: {result['message']}")

                        st.info(f"**Risk Probability**: {result['probability']:.1%}")
                        st.info("📊 **Detailed results available on the Results page**")

                    else:
                        st.error(f"❌ API Error ({response.status_code})")
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', 'Unknown error')
                            st.write(f"Error message: {error_msg}")
                            if 'details' in error_data:
                                st.write(f"Error details: {error_data['details']}")
                        except:
                            st.write("Raw response:", response.text)
                        st.write(f"Response headers: {dict(response.headers)}")

                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. Please check if the backend server is running.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Connection failed. Please ensure the backend server is running on http://localhost:5000")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    st.write("Full error details:", e)

def show_results():
    st.header("Prediction Results")

    if 'prediction_result' not in st.session_state:
        st.info("Please complete a prediction first in the Prediction section.")
        return

    result = st.session_state.prediction_result

    # Display results
    if result['prediction'] == 1:
        st.error("⚠️ HIGH RISK: Heart attack risk detected!")
        st.markdown(f"**Probability**: {result['probability']:.2%}")
    else:
        st.success("✅ LOW RISK: No heart attack risk detected.")
        st.markdown(f"**Probability**: {result['probability']:.2%}")

    st.markdown("---")

    # Display input summary
    if 'prediction_data' in st.session_state:
        st.subheader("Input Summary")
        data = st.session_state.prediction_data

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Age**: {data['age']}")
            st.markdown(f"**Gender**: {'Male' if data['gender_Male'] else 'Female'}")
            st.markdown(f"**Hypertension**: {'Yes' if data['hypertension'] else 'No'}")
            st.markdown(f"**Diabetes**: {'Yes' if data['diabetes'] else 'No'}")
            st.markdown(f"**Cholesterol**: {data['cholesterol_level']} mg/dL")

        with col2:
            st.markdown(f"**Smoking Status**: {['Never', 'Past', 'Current', 'Unknown'][data['smoking_status_Past']*1 + data['smoking_status_Unknown']*3 + (1 if not data['smoking_status_Never'] and not data['smoking_status_Past'] and not data['smoking_status_Unknown'] else 0)]}")
            st.markdown(f"**Physical Activity**: {['High', 'Moderate', 'Low'][data['physical_activity_Low']*2 + (1 if not data['physical_activity_Low'] else 0)]}")
            st.markdown(f"**Stress Level**: {['Low', 'Moderate', 'High'][data['stress_level_Moderate']*1 + (2 if not data['stress_level_Moderate'] else 0)]}")
            st.markdown(f"**Sleep Hours**: {data['sleep_hours']}")

def show_history():
    st.header("Prediction History")
    st.info("History feature coming soon...")

if __name__ == "__main__":
    main()