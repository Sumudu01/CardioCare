import streamlit as st
import requests
import json
import os
import uuid
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="CardioCare - Heart Attack Prediction",
    page_icon="",
    layout="wide"
)

# Backend API URL
API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:5000/api"))

# Local history storage
HISTORY_PATH = os.path.join(os.path.dirname(__file__), "history.json")

def _load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_history(history_items):
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history_items, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _append_history(entry):
    history_items = _load_history()
    history_items.append(entry)
    _save_history(history_items)

def _delete_history(entry_id):
    history_items = _load_history()
    new_items = [h for h in history_items if h.get("id") != entry_id]
    _save_history(new_items)

def main():
    st.title("CardioCare - Heart Attack Prediction System")
    st.markdown("---")

    # The built-in Pages menu (top-left) controls navigation. This main page
    # serves as the Home page.
    show_home()

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

    **Disclaimer**: This tool is for educational purposes only and should not replace professional medical advice.
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
                    response = requests.post(f"{API_URL}/predict", json=data, timeout=10)

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.prediction_result = result

                        # Display immediate result
                        st.success("Prediction completed successfully.")

                        # Show quick result summary
                        if result['prediction'] == 1:
                            st.error(f"**HIGH RISK**: {result['message']}")
                        else:
                            st.success(f"**LOW RISK**: {result['message']}")

                        st.info(f"**Risk Probability**: {result['probability']:.1%}")
                        st.info("Detailed results are available on the Results page.")

                        # Persist history (local file) with timestamp and unique id
                        try:
                            history_entry = {
                                "id": str(uuid.uuid4()),
                                "timestamp": datetime.now().isoformat(timespec="seconds"),
                                "input": data,
                                "result": result
                            }
                            _append_history(history_entry)
                        except Exception:
                            pass

                    else:
                        st.error(f"API error ({response.status_code}). Please try again.")
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', '')
                            if error_msg:
                                st.caption(f"Details: {error_msg}")
                        except Exception:
                            pass

                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please confirm the backend is running.")
                except requests.exceptions.ConnectionError:
                    st.error("Connection failed. Ensure the backend is running on http://localhost:5000.")
                except Exception as e:
                    st.error("Unexpected error occurred.")
                    st.caption(str(e))

def show_results():
    st.header("Prediction Results")

    if 'prediction_result' not in st.session_state:
        st.info("Please complete a prediction first in the Prediction section.")
        return

    result = st.session_state.prediction_result

    # Display results
    risk_container = st.container()
    with risk_container:
        if result['prediction'] == 1:
            st.error("HIGH RISK: Heart attack risk detected.")
        else:
            st.success("LOW RISK: No heart attack risk detected.")
        st.markdown(f"**Estimated Probability**: {result['probability']:.2%}")

    st.markdown("---")

    # Display input summary
    if 'prediction_data' in st.session_state:
        st.subheader("Input Summary")
        data = st.session_state.prediction_data

        # Derive user-friendly labels using the submitted flags only (no backend changes)
        gender_label = 'Male' if data.get('gender_Male') else 'Female'
        smoking_label = (
            'Never' if data.get('smoking_status_Never') else
            'Past' if data.get('smoking_status_Past') else
            'Unknown' if data.get('smoking_status_Unknown') else
            'Current'
        )
        physical_activity_label = 'Low' if data.get('physical_activity_Low') else 'High/Moderate'
        stress_label = 'Moderate' if data.get('stress_level_Moderate') else 'Low/High'

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Age**: {data['age']}")
            st.markdown(f"**Gender**: {gender_label}")
            st.markdown(f"**Hypertension**: {'Yes' if data['hypertension'] else 'No'}")
            st.markdown(f"**Diabetes**: {'Yes' if data['diabetes'] else 'No'}")
            st.markdown(f"**Cholesterol**: {data['cholesterol_level']} mg/dL")

        with col2:
            st.markdown(f"**Smoking Status**: {smoking_label}")
            st.markdown(f"**Physical Activity**: {physical_activity_label}")
            st.markdown(f"**Stress Level**: {stress_label}")
            st.markdown(f"**Sleep Hours**: {data['sleep_hours']}")

def show_history():
    st.header("Prediction History")

    history_items = _load_history()

    if not history_items:
        st.info("No predictions saved yet.")
        return

    # Sort by timestamp desc
    def _parse_ts(ts):
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime.min
    history_items_sorted = sorted(history_items, key=lambda h: _parse_ts(h.get("timestamp", "")), reverse=True)

    # Build a concise label for each item
    labels = []
    for item in history_items_sorted:
        ts = item.get("timestamp", "")
        res = item.get("result", {})
        pred = res.get("prediction")
        prob = res.get("probability")
        status = "HIGH" if pred == 1 else "LOW"
        labels.append(f"{ts} — {status} risk ({prob:.1%})")

    selected = st.radio("Saved predictions", options=range(len(history_items_sorted)), format_func=lambda i: labels[i])

    selected_item = history_items_sorted[selected]
    st.markdown("---")
    st.subheader("Details")

    colA, colB = st.columns(2)
    with colA:
        st.markdown(f"**Timestamp**: {selected_item.get('timestamp','')}")
        st.markdown(f"**Risk Level**: {'HIGH' if selected_item['result'].get('prediction') == 1 else 'LOW'}")
        st.markdown(f"**Probability**: {selected_item['result'].get('probability', 0):.2%}")
        st.markdown(f"**Message**: {selected_item['result'].get('message','')}")
    with colB:
        st.markdown("**Input Summary**")
        data = selected_item.get("input", {})
        gender_label = 'Male' if data.get('gender_Male') else 'Female'
        smoking_label = (
            'Never' if data.get('smoking_status_Never') else
            'Past' if data.get('smoking_status_Past') else
            'Unknown' if data.get('smoking_status_Unknown') else
            'Current'
        )
        physical_activity_label = 'Low' if data.get('physical_activity_Low') else 'High/Moderate'
        stress_label = 'Moderate' if data.get('stress_level_Moderate') else 'Low/High'

        st.markdown(f"- Age: {data.get('age')}")
        st.markdown(f"- Gender: {gender_label}")
        st.markdown(f"- Hypertension: {'Yes' if data.get('hypertension') else 'No'}")
        st.markdown(f"- Diabetes: {'Yes' if data.get('diabetes') else 'No'}")
        st.markdown(f"- Cholesterol: {data.get('cholesterol_level')} mg/dL")
        st.markdown(f"- Smoking Status: {smoking_label}")
        st.markdown(f"- Physical Activity: {physical_activity_label}")
        st.markdown(f"- Stress Level: {stress_label}")
        st.markdown(f"- Sleep Hours: {data.get('sleep_hours')}")

    st.markdown("---")
    cols = st.columns(2)
    with cols[0]:
        if st.button("Delete this record", type="secondary"):
            _delete_history(selected_item.get("id"))
            st.success("Record deleted.")
            st.rerun()

if __name__ == "__main__":
    main()