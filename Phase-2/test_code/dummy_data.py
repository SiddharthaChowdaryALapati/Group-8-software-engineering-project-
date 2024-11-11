import random
from datetime import datetime, timedelta
from firebase_admin import firestore, credentials, initialize_app

# Initialize Firebase Admin SDK
cred = credentials.Certificate("ht.json")  # Replace with the path to your Firebase credentials file
initialize_app(cred)

# Get Firestore database reference
db = firestore.client()

def get_first_user_uid():
    """Fetch the UID of the first user in Firestore."""
    try:
        users = db.collection('users').limit(1).get()
        if users:
            return users[0].id  # Get the document ID of the first user
        else:
            print("No users found in Firestore.")
            return None
    except Exception as e:
        print(f"Error fetching user UID: {e}")
        return None

def generate_dummy_data(start_date: str = "2024-10-01", num_days: int = 30):
    """
    Generate and insert dummy health data for analysis for a specified number of days.
    
    Parameters:
    - start_date: Starting date in the format 'YYYY-MM-DD' (default: "2024-10-01").
    - num_days: Number of days of data to generate (default: 30).
    """
    uid = get_first_user_uid()  # Automatically get the first user UID

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

# Example usage
if __name__ == "__main__":
    generate_dummy_data()  # Call with default start_date and num_days
