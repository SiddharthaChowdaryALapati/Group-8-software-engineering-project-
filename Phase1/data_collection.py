import sqlite3
import streamlit as st
import pandas as pd
import json
import os

# Determine the path of the current script and place the database in the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'users.db')

# Database setup for health data
def initialize_health_data_table():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS health_data (
                user_id INTEGER,
                weight REAL, height REAL, blood_pressure TEXT, heart_rate REAL,
                body_temp REAL, bmi REAL, glucose_level REAL, cholesterol TEXT,
                oxygen_saturation REAL, activity_level TEXT, dietary_intake TEXT,
                sleep_patterns TEXT, medications TEXT, symptoms TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

# Function to collect health data from users
def collect_health_data(user_id):
    st.title("Health Data Collection")
    
    # Health data inputs
    weight = st.number_input("Weight (kg)", min_value=0.0)
    height = st.number_input("Height (cm)", min_value=0.0)
    blood_pressure = st.text_input("Blood Pressure (Systolic/Diastolic)")
    heart_rate = st.number_input("Heart Rate (BPM)", min_value=0)
    body_temp = st.number_input("Body Temperature (Celsius)", min_value=0.0)
    bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0)
    glucose = st.number_input("Blood Glucose Level", min_value=0.0)
    cholesterol = st.text_input("Cholesterol Levels (Total, HDL, LDL, Triglycerides)")
    oxygen = st.number_input("Oxygen Saturation (%)", min_value=0)
    activity = st.text_area("Activity Level")
    dietary = st.text_area("Dietary Intake (Calories, Macronutrients)")
    sleep = st.text_input("Sleep Patterns (Hours)")
    medications = st.text_area("Medications (Name, Dosage, Frequency)")
    symptoms = st.text_area("Symptoms or Concerns")

    if st.button("Save Data"):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO health_data (
                user_id, weight, height, blood_pressure, heart_rate, body_temp, bmi, glucose_level,
                cholesterol, oxygen_saturation, activity_level, dietary_intake, sleep_patterns,
                medications, symptoms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (user_id, weight, height, blood_pressure, heart_rate, body_temp, bmi, glucose, 
                       cholesterol, oxygen, activity, dietary, sleep, medications, symptoms))
            conn.commit()
            st.success("Health data saved successfully!")

# Function to export health data as CSV or JSON
def export_data(user_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM health_data WHERE user_id=?', (user_id,))
        data = c.fetchall()
        df = pd.DataFrame(data, columns=['UserID', 'Weight', 'Height', 'Blood Pressure', 'Heart Rate', 
                                         'Body Temp', 'BMI', 'Glucose', 'Cholesterol', 
                                         'Oxygen', 'Activity', 'Dietary', 'Sleep', 'Medications', 'Symptoms'])
        
        st.download_button(label="Download as CSV", data=df.to_csv(index=False), file_name="health_data.csv", mime='text/csv')
        st.download_button(label="Download as JSON", data=json.dumps(df.to_dict(orient='records')), file_name="health_data.json", mime='application/json')

# Initialize the health data table when the module is imported
initialize_health_data_table()
