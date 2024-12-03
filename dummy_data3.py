import random
import pandas as pd
from datetime import datetime, timedelta
from firebase_admin import firestore, credentials, initialize_app
import streamlit as st  # Assuming Streamlit is used to manage session state

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("ht.json")  # Replace with the path to your Firebase credentials file
# initialize_app(cred)

# Get Firestore database reference
db = firestore.client()

def generate_dummy_data(uid, start_date: str = "2024-10-01", num_days: int = 30):
    """
    Generate and insert dummy health data for a specified number of days for the logged-in user.
    
    Parameters:
    - uid: The UID of the currently logged-in user.
    - start_date: Starting date in the format 'YYYY-MM-DD' (default: "2024-10-01").
    - num_days: Number of days of data to generate (default: 30).
    """
    if not uid:
        print("Unable to proceed without a valid user UID.")
        return

    # Parse start_date to datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    user_ref = db.collection('users').document(uid)
    
    for i in range(num_days):
        # Generate random data for each day
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        
        health_data = {
            'weight': round(random.uniform(50, 100), 1),  # kg
            'height': round(random.uniform(150, 200), 1),  # cm
            'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 90)}",  # systolic/diastolic
            'heart_rate': random.randint(60, 100),  # BPM
            'body_temp': round(random.uniform(36.0, 37.5), 1),  # °C
            'glucose': round(random.uniform(70, 120), 1),  # mg/dL
            'oxygen': random.randint(95, 100),  # %
            'sleep': round(random.uniform(5, 9), 1),  # hours
            'activity': random.choice(["Sedentary", "Light", "Moderate", "Intense"])
        }

        # Update Firestore with the new data entry for the specific date
        try:
            user_ref.update({
                f'daily_data.{formatted_date}': health_data
            })
            print(f"Inserted dummy data for {formatted_date} under user {uid}.")
        except Exception as e:
            print(f"Failed to insert data for {formatted_date}: {e}")

def fetch_data_and_export_to_csv(uid, filename="exported_health_data.csv"):
    """
    Fetch daily health data for the given user UID from Firestore and export to CSV.
    
    Parameters:
    - uid: The UID of the logged-in user whose data is being fetched.
    - filename: The name of the CSV file to export (default: "exported_health_data.csv").
    """
    if not uid:
        print("UID not provided. Please log in to fetch user data.")
        return

    try:
        user_ref = db.collection('users').document(uid)
        daily_data = user_ref.get().to_dict().get("daily_data", {})

        # Format daily_data into a list of records for DataFrame
        data = []
        for date, health_data in daily_data.items():
            health_data['Date'] = date  # Add the date as a field
            data.append(health_data)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df.sort_values(by='Date', inplace=True)  # Sort by date

        # Export to CSV
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        
    except Exception as e:
        print(f"Error fetching data or exporting to CSV: {e}")

# Example usage in Streamlit or other session-based applications
def fetch_data_main():
    # Assume the user is logged in and their UID is stored in the session
    print("started: UID:", st.session_state.get("uid"))
    uid = st.session_state.get("uid")  # Retrieve UID of the logged-in user from session state
    
    if uid:
        # Generate dummy data for the logged-in user
        # generate_dummy_data(uid)
        
        # Fetch and export the data for the logged-in user
        fetch_data_and_export_to_csv(uid)
    else:
        st.warning("User is not logged in. Please log in to generate and fetch data.")

# Run the main function if needed
fetch_data_main()
