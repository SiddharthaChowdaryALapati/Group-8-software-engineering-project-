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
                user_id INTEGER PRIMARY KEY,
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
    
    # Check if data exists for the user
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM health_data WHERE user_id=?", (user_id,))
        data = c.fetchone()

    # Display input fields pre-filled with existing data if available
    weight = st.number_input("Weight (kg)", value=data[1] if data else 0.0)
    height = st.number_input("Height (cm)", value=data[2] if data else 0.0)
    blood_pressure = st.text_input("Blood Pressure (Systolic/Diastolic)", value=data[3] if data else "")
    heart_rate = st.number_input("Heart Rate (BPM)", value=data[4] if data else 0)
    body_temp = st.number_input("Body Temperature (Celsius)", value=data[5] if data else 0.0)
    bmi = st.number_input("Body Mass Index (BMI)", value=data[6] if data else 0.0)
    glucose = st.number_input("Blood Glucose Level", value=data[7] if data else 0.0)
    cholesterol = st.text_input("Cholesterol Levels (Total, HDL, LDL, Triglycerides)", value=data[8] if data else "")
    oxygen = st.number_input("Oxygen Saturation (%)", value=data[9] if data else 0)
    activity = st.text_area("Activity Level", value=data[10] if data else "")
    dietary = st.text_area("Dietary Intake (Calories, Macronutrients)", value=data[11] if data else "")
    sleep = st.text_input("Sleep Patterns (Hours)", value=data[12] if data else "")
    medications = st.text_area("Medications (Name, Dosage, Frequency)", value=data[13] if data else "")
    symptoms = st.text_area("Symptoms or Concerns", value=data[14] if data else "")

    # Show Update button if data exists, otherwise show Save button
    if data:
        if st.button("Update Data"):
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute('''UPDATE health_data SET weight=?, height=?, blood_pressure=?, heart_rate=?, 
                            body_temp=?, bmi=?, glucose_level=?, cholesterol=?, oxygen_saturation=?, 
                            activity_level=?, dietary_intake=?, sleep_patterns=?, medications=?, symptoms=? 
                            WHERE user_id=?''',
                          (weight, height, blood_pressure, heart_rate, body_temp, bmi, glucose, cholesterol,
                           oxygen, activity, dietary, sleep, medications, symptoms, user_id))
                conn.commit()
                st.success("Health data updated successfully!")
    else:
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
