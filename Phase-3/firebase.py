import firebase_admin
from firebase_admin import credentials, auth, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


import os

# Dynamically construct the file path to the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
file_path = os.path.join(current_dir, "ht02.json")  # Path to 'ht.json'

# Verify the file exists before initializing Firebase
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file 'ht.json' was not found at {file_path}")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(file_path)  # Ensure the correct path to your credentials
firebase_admin.initialize_app(cred)

# Get Firestore database reference
db = firestore.client()


def signup_user(email: str, password: str, username: str, age: int, gender: str, blood_type: str):
    """
    Create a user in Firebase Authentication and store additional details in Firestore.
    """
    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(email=email, password=password)
        print("User created in Firebase Authentication:", user.uid)
        
        # Store additional user data in Firestore
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),  # Store hashed password
            'age': age,
            'gender': gender,
            'blood_type': blood_type,
            'created_at': datetime.now()  # Optional: store account creation timestamp
        }
        
        # Save user data in Firestore
        db.collection('users').document(user.uid).set(user_data)
        print("User data saved in Firestore.")

        return True, "User registered successfully!", user.uid
    except Exception as e:
        print(f"Error during signup_user: {e}")
        return False, str(e), None

def login_user(email: str, password: str):
    """
    Authenticate user using Firebase Authentication and verify password against Firestore.
    """
    try:
        user = auth.get_user_by_email(email)
        
        # Fetch user details from Firestore to verify password
        user_ref = db.collection('users').document(user.uid)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            # Verify the hashed password
            if check_password_hash(user_data['password'], password):
                return True, f"Welcome {user_data['username']}!", user.uid
            else:
                return False, "Incorrect password.", None
        else:
            return False, "User details not found in Firestore.", None
    except Exception as e:
        return False, "Authentication failed. Please check your credentials.", None



def update_daily_data(uid: str, health_data: dict):
    """
    Update the `daily-data` sub-field with the provided health data for today's date.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD

    # Reference to the user's document in Firestore
    user_ref = db.collection('users').document(uid)

    try:
        # Update the specific date in the `daily-data` field with new health data
        user_ref.update({
            f'daily_data.{current_date}': health_data
        })
        print(f"Updated daily data for {current_date} under user {uid}.")
        return True
    except Exception as e:
        print(f"Failed to update daily data: {e}")
        return False

def check_existing_data(uid: str) -> bool:
    """
    Check if health data for the current date already exists.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    user_ref = db.collection('users').document(uid)

    try:
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return current_date in user_data.get('daily_data', {})
        return False
    except Exception as e:
        print(f"Error checking existing data: {e}")
        return False
    

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
