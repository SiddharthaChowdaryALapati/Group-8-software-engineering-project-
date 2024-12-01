import streamlit as st
from firebase import update_daily_data # Import the function from firebase


def weekly_data():
    # st.title("Health Data Collection")
    # Check if data for the current day already exists
    
        

    # Create form for data collection
    with st.form("health_data_form"):
        st.subheader("Basic Health Metrics")

        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0)
            height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0)
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (BPM)", min_value=0, max_value=250)
        
        with col2:
            body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=36.6)
            glucose = st.number_input("Blood Glucose Level (mg/dL)", min_value=0.0)
            oxygen = st.number_input("Oxygen Saturation (%)", min_value=0, max_value=100, value=98)
            
        st.subheader("Lifestyle Factors")
        sleep = st.number_input("Hours of Sleep", min_value=0.0, max_value=24.0)
        activity = st.selectbox("Physical Activity Level", ["Sedentary", "Light", "Moderate", "Intense"])
        
        # Submit form
        if st.form_submit_button("Submit Data"):
            # Collect data into a dictionary
            health_data = {
                'weight': weight,
                'height': height,
                'blood_pressure': blood_pressure,
                'heart_rate': heart_rate,
                'body_temp': body_temp,
                'glucose': glucose,
                'oxygen': oxygen,
                'sleep': sleep,
                'activity': activity
            }

            # Update Firestore with the new data entry
            update_success = update_daily_data(st.session_state['uid'], health_data)

            if update_success:
                st.success("Data submitted and saved successfully!")
            else:
                st.error("Failed to save data. Please try again.")
