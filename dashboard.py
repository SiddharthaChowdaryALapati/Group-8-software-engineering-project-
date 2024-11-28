import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from firebase import get_first_user_uid, db  # Import Firestore functions
from datetime import datetime as dt
import joblib
import requests
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from the .env file
load_dotenv()

# Get API key and Search Engine ID from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Email address to send emails from
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Email password or app-specific password

# Load the trained machine learning model
model = joblib.load('hypertension_risk_model.pkl')

# Sample data to simulate the doctors, categories, and bed availability
doctors_data = [
    {"name": "Dr. John Doe", "specialty": "Cardiologist", "availability": ["Monday", "Wednesday", "Friday"]},
    {"name": "Dr. Jane Smith", "specialty": "Dermatologist", "availability": ["Tuesday", "Thursday"]},
    {"name": "Dr. Emily Davis", "specialty": "Pediatrician", "availability": ["Monday", "Thursday"]},
    {"name": "Dr. Mark Lee", "specialty": "Orthopedic", "availability": ["Wednesday", "Friday"]},
]

beds_data = {
    "ICU": 2,
    "General": 5,
    "Private": 3
}

appointments = []

# Convert sample data to DataFrame
doctors_df = pd.DataFrame(doctors_data)

# Fetch user profile from Firestore
def fetch_user_profile(uid):
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()
    return user_doc.to_dict() if user_doc.exists else {}

# Fetch user daily health data from Firestore
def fetch_user_daily_data(user_data):
    daily_data = user_data.get('daily_data', {})
    if daily_data:
        df = pd.DataFrame.from_dict(daily_data, orient='index')
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df
    return pd.DataFrame()  # Empty DataFrame if no data

# Update user profile data in Firestore
def update_user_data(uid, updated_data):
    db.collection('users').document(uid).update(updated_data)

# Provide recommendations based on hypertension risk level
def get_recommendations(risk_level):
    recommendations = {
        0: {
            "Proteins": ["Lean chicken, Fish, Eggs, Greek yogurt, Tofu, Lentils"],
            "Food Items": ["Leafy greens, Berries, Whole grains, Almonds, Olive oil"],
            "Exercise": ["30 mins of moderate exercise daily"],
            "Mental Wellness": ["Practice mindfulness meditation for 10 minutes a day"],
            "Hydration": ["Drink 8-10 glasses of water daily"],
            "Sleep Hygiene": ["Aim for 7-8 hours of sleep per night"]
        },
        1: {
            "Proteins": ["Skinless poultry, Low-fat dairy, Beans, Soy milk"],
            "Food Items": ["High-fiber vegetables, Low-sodium foods, Potassium-rich foods"],
            "Exercise": ["20-30 mins of light to moderate exercise, 3-5 days a week"],
            "Mental Wellness": ["Engage in relaxation techniques and reduce stress"],
            "Hydration": ["Increase water intake, limit caffeine and alcohol"],
            "Sleep Hygiene": ["Prioritize 7-8 hours of sleep, reduce caffeine intake"]
        }
    }
    return recommendations[risk_level]

# Predict hypertension risk and get recommendations
def predict_hypertension_risk(bmi, heart_rate, systolic_bp, diastolic_bp, age):
    input_data = [[bmi, heart_rate, systolic_bp, diastolic_bp, age]]
    risk_prediction = model.predict(input_data)[0]
    recommendations = get_recommendations(risk_prediction)
    return risk_prediction, recommendations

# Google Search interaction
def google_search(query):
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": 3  # Get top 3 results
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()

        results = []
        if "items" in search_results:
            for item in search_results["items"]:
                results.append({"title": item["title"], "link": item["link"], "snippet": item["snippet"]})
        return results
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Chatbot interface in the dashboard
def display_chatbot():
    st.markdown("<h3>\U0001F4AC Health Chatbot</h3>", unsafe_allow_html=True)
    question = st.text_input("Ask me anything about your health metrics or get advice:")

    if st.button("Send Question"):
        if question:
            search_results = google_search(question)
            if isinstance(search_results, str):
                st.error(search_results)  # Display error message if request fails
            elif len(search_results) == 0:
                st.warning("No results found.")
            else:
                st.subheader("Top Results:")
                for result in search_results:
                    st.write(f"**{result['title']}**")
                    st.write(f"{result['snippet']}")
                    st.write(f"[Link]({result['link']})")
                    st.write("---")
        else:
            st.warning("Please enter a question for the chatbot.")

# Send email with health data report
def send_health_report(email, subject, body):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

        # Send the email
        server.send_message(msg)
        server.quit()
        st.success(f"Health report sent successfully to {email}!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Doctor appointment system
def doctor_appointment_system():
    st.title("Hospital Appointment and Bed Availability System")

    # Section for scheduling an appointment
    st.header("Schedule a Doctor's Appointment")
    specialty = st.selectbox("Select Specialty", doctors_df["specialty"].unique())
    available_doctors = doctors_df[doctors_df["specialty"] == specialty]
    doctor = st.selectbox("Select Doctor", available_doctors["name"])
    appointment_date = st.date_input("Select Appointment Date", min_value=datetime.date.today())
    appointment_time = st.time_input("Select Appointment Time")
    appointment_day = appointment_date.strftime("%A")

    # Check doctor's availability
    selected_doctor = available_doctors[available_doctors["name"] == doctor].iloc[0]
    if appointment_day in selected_doctor["availability"]:
        if st.button("Schedule Appointment"):
            uid = st.session_state.get('uid') or get_first_user_uid()
            user_data = fetch_user_profile(uid)
            appointment = {
                "doctor": doctor,
                "specialty": specialty,
                "date": str(appointment_date),
                "time": str(appointment_time)
            }
            user_appointments = user_data.get("appointments", [])
            user_appointments.append(appointment)
            db.collection('users').document(uid).update({"appointments": user_appointments})
            st.success(f"Appointment scheduled with {doctor} ({specialty}) on {appointment_date} at {appointment_time}.")
            # Send email with appointment details
            email = user_data.get('email', '')
            if email:
                subject = "Doctor's Appointment Confirmation"
                body = f"Your appointment with {doctor} ({specialty}) is scheduled for {appointment_date} at {appointment_time}."
                send_health_report(email, subject, body)
    else:
        st.error(f"{doctor} is not available on {appointment_day}. Please select a different date.")

    # Display scheduled appointments
    st.header("Scheduled Appointments")
    uid = st.session_state.get('uid') or get_first_user_uid()
    user_data = fetch_user_profile(uid)
    if "appointments" in user_data and len(user_data["appointments"]) > 0:
        appointments_df = pd.DataFrame(user_data["appointments"])
        st.table(appointments_df)
    else:
        st.info("No appointments scheduled.")

    # Section for checking bed availability
    st.header("Check Bed Availability")
    bed_category = st.selectbox("Select Bed Category", list(beds_data.keys()), key="bed_category")
    if st.button("Check Bed Availability"):
        available_beds = beds_data[bed_category]
        if available_beds > 0:
            st.success(f"{available_beds} {bed_category} bed(s) available.")
        else:
            st.error(f"No {bed_category} beds available.")

    # Section for bed booking
    st.header("Book a Bed")
    patient_name_bed = st.text_input("Enter Patient Name for Bed Booking", key="bed_booking")
    bed_category_booking = st.selectbox("Select Bed Category for Booking", list(beds_data.keys()), key="bed_booking_category")
    if st.button("Book Bed"):
        if beds_data[bed_category_booking] > 0:
            beds_data[bed_category_booking] -= 1
            st.success(f"Bed booked successfully for {patient_name_bed} in {bed_category_booking} category.")
            # Send email with bed booking details
            email = user_data.get('email', '')
            if email:
                subject = "Bed Booking Confirmation"
                body = f"Your bed booking for {bed_category_booking} category is confirmed. Patient: {patient_name_bed}"
                send_health_report(email, subject, body)
        else:
            st.error(f"No {bed_category_booking} beds available for booking.")

    if st.button("Back to Dashboard"):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()

# Main health analytics dashboard
def dashboard(uid):
    st.title("Health Analytics Dashboard")

    # Add a button to book a doctor's appointment
    if st.button("Book Doctor's Appointment"):
        st.session_state['page'] = 'appointment'
        st.experimental_rerun()

    # Fetch user profile and daily health data
    user_data = fetch_user_profile(uid)
    df = fetch_user_daily_data(user_data)

    if df.empty:
        st.warning("No daily health data available.")
        return

    # Calculate BMI
    df['BMI'] = df.apply(lambda row: row['weight'] / ((row['height'] / 100) ** 2) if row['height'] > 0 else 0, axis=1)

    # Sidebar for updating user profile
    st.sidebar.markdown("<div class='sidebar-card'><h3>\U0001F464 Patient Information</h3></div>", unsafe_allow_html=True)
    with st.sidebar.form("patient_info_form"):
        username = st.text_input("Name", user_data.get('username', ''))
        age = st.number_input("Age", 0, 120, user_data.get('age', 35))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], \
                              ["Male", "Female", "Other"].index(user_data.get('gender', 'Male')))
        blood_type = st.selectbox("Blood Type", \
                                  ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                  ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(user_data.get('blood_type', 'O+')))
        email = st.text_input("Email Address", user_data.get('email', ''))
        if st.form_submit_button("Update Patient Information"):
            updated_data = {"username": username, "age": age, "gender": gender, "blood_type": blood_type, "email": email}
            update_user_data(uid, updated_data)
            st.success("Patient information updated successfully!")

    # Display key health metrics in wider cards
    st.markdown("<div class='neumorphic-card'><h3>\U0001F4CA Key Health Metrics</h3></div>", unsafe_allow_html=True)
    metric_columns = st.columns([1, 1, 1, 1], gap="large")
    metrics = [
        {"label": "⚖️ BMI", "value": f"{df['BMI'].iloc[-1]:.1f}", "color": "#FFCDD2"},
        {"label": "🩺 Blood Pressure", "value": f"{df['blood_pressure'].iloc[-1]}", "color": "#C8E6C9"},
        {"label": "💓 Heart Rate", "value": f"{df['heart_rate'].iloc[-1]:.0f} bpm", "color": "#BBDEFB"},
        {"label": "🫁 Oxygen Level", "value": f"{df['oxygen'].iloc[-1]:.0f}%", "color": "#FFF9C4"}
    ]

    for col, metric in zip(metric_columns, metrics):
        col.markdown(
            f"""
            <div style="background-color: {metric['color']}; padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 20px; font-weight: bold;">{metric['label']}</div>
                <div style="font-size: 28px; font-weight: bold;">{metric['value']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tabbed data visualizations with wider layout
    tab1, tab2, tab3 = st.tabs(["\U0001F4C8 Vitals", "\U0001F3CC‍ Activity & Sleep", "\U0001F52C Lab Results"])
    with tab1:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            systolic = [int(bp.split('/')[0]) if isinstance(bp, str) and '/' in bp else 0 for bp in df['blood_pressure'].fillna('0/0')]
            diastolic = [int(bp.split('/')[1]) if isinstance(bp, str) and '/' in bp else 0 for bp in df['blood_pressure'].fillna('0/0')]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=systolic, name="Systolic"))
            fig.add_trace(go.Scatter(x=df.index, y=diastolic, name="Diastolic"))
            fig.update_layout(title="Blood Pressure Trend", height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(df, x=df.index, y='heart_rate', title="Heart Rate Trend")
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            fig = px.bar(df, x=df.index, y='activity', title="Activity Level")
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(df, x=df.index, y='sleep', title="Sleep Duration")
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            fig = px.line(df, x=df.index, y='glucose', title="Glucose Levels")
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(df, x=df.index, y='body_temp', title="Body Temperature")
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig, use_container_width=True)

    # Hypertension prediction and recommendations
    st.markdown("<h3>\U0001F9E0 Hypertension Risk Prediction & Recommendations</h3>", unsafe_allow_html=True)
    latest_data = df.iloc[-1]
    if isinstance(latest_data['blood_pressure'], str) and '/' in latest_data['blood_pressure']:
        systolic, diastolic = map(int, latest_data['blood_pressure'].split('/'))
    else:
        systolic, diastolic = 0, 0

    risk_level, recommendations = predict_hypertension_risk(
        latest_data['BMI'], latest_data['heart_rate'], systolic, diastolic, user_data.get('age', 35)
    )
    risk_text = "High" if risk_level == 1 else "Low"
    st.markdown(f"### Predicted Hypertension Risk Level: **{risk_text}**")

    for category, items in recommendations.items():
        with st.expander(f"{category} Recommendations"):
            for item in items:
                st.write(f"- {item}")

    # Display chatbot
    st.markdown("<div style='padding: 20px; border-radius: 15px; background-color: #F1F8E9; margin-top: 20px;'>", unsafe_allow_html=True)
    display_chatbot()
    st.markdown("</div>", unsafe_allow_html=True)

    # Email health report
    recipient_email = user_data.get('email', '')
    if recipient_email:
        health_summary = f"Health Report for {user_data.get('username', 'User')}\n\n"
        health_summary += f"BMI: {df['BMI'].iloc[-1]:.1f}\n"
        health_summary += f"Blood Pressure: {df['blood_pressure'].iloc[-1]}\n"
        health_summary += f"Heart Rate: {df['heart_rate'].iloc[-1]:.0f} bpm\n"
        health_summary += f"Oxygen Level: {df['oxygen'].iloc[-1]:.0f}%\n"
        health_summary += f"Hypertension Risk Level: {risk_text}\n"

        for category, items in recommendations.items():
            health_summary += f"\n{category} Recommendations:\n"
            for item in items:
                health_summary += f"- {item}\n"

        send_health_report(recipient_email, "Daily Health Report", health_summary)

# Start dashboard function
def start_dashboard():
    uid = st.session_state.get('uid') or get_first_user_uid()
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'

    if uid:
        if st.session_state['page'] == 'dashboard':
            dashboard(uid)
        elif st.session_state['page'] == 'appointment':
            doctor_appointment_system()
    else:
        st.warning("No user found or user is not logged in.")

if __name__ == "__main__":
    start_dashboard()
