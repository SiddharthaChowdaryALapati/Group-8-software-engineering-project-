import firebase_admin
from firebase_admin import credentials, auth, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import streamlit as st
import requests
import json

import os

# # Dynamically construct the file path to the JSON file
# current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
# file_path = os.path.join(current_dir, "ht02.json")  # Path to 'ht.json'

# # Verify the file exists before initializing Firebase
# if not os.path.exists(file_path):
#     raise FileNotFoundError(f"The file 'ht.json' was not found at {file_path}")
presigned_url =" https://health-file.s3.us-east-2.amazonaws.com/ht04.json?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBIaCXVzLWVhc3QtMiJHMEUCIQC3S%2FAFKVgkFC34Sfic%2FvCnep%2BRGDDuIknTcJXkAczFRgIgKrHO4JgUGKMlKoBzkjn%2Fk8zncIwp0sI8pZGH%2Bga3mIkq1AMIu%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw1NDUwMDk4NTg3OTciDPuuHLdJzUF07rEnQCqoA%2FWAIVVmYy%2FcwxoC6SVWNFY0LsUkV3tgYDmf5IXXWtx9Nqvz%2Fs7kkoQ3MxNpo9lVr1Kplma3JHZEh1JTpnnTYohuh1y3L9oz9%2F5x7ahWWNhPQ%2FeWOwnAG042E1rlnyPOdPriAGBLAf3XLpVTEFUHwMDCnl4Hvmy%2B1UhnvnljjwyMliKfUxCU2Vg5FhhvAJ5Ny9GDi8At1n2Z9mNRtzHWQvxI3CZSWAsleylAyRkDUvgA83kd%2BKZeUwJTzl68YwGPi%2F%2Fsbosbx4oryyxMdlegcjoYCiK0lz6ZbYtbzZjMdda9b0xpg9mlk3EgytHqFX%2Bf8p5zauJqTBxzGP%2FkDjFTo6YtoY50zG9sVeJ73uFBrKa8drKIRr9gxXOl1I4%2BkbOlUjDmZNeRepufyQDVFJzF1JJSEtBCkvY2ACXYlLPtB9Wj44p9h%2Bi7xf%2F6Y%2F7mS%2FOZJJ0s46L61%2F8JnEW9p%2BT2JpnaOHIwtW0BbJMBzKeLgLrWnIR3U4qZTyegfysVHKFGmfSqzFs%2F6lVDphkvOS0Jn6Rt3ctbsmgJQ%2F7iuUxNyYlqFGtIlirNS3sw7%2Fq1ugY65AIozR%2Fp7sO04vrjZXtDEj3%2BOA0MukDkTkXI7G%2Fwf0Z96mIYo9oJ05%2BvJWjxYeuXjE3EAtYOzZC798aYVsZQcAgzegq%2FrSpu88b9JDEKxAuZTCeqPg9VRmBeoPWkBA54Sc2L5WeiwzOOqJ3z3dEODnth63BnqNZMOfqDcBZ1ERAYElLFa2tryJ1cUJVANJa9MV5smMfhxCkaRCcd%2BDQhCDpjam7gAg7TwAx2vK20y1OlCQpKQdIDQisCXVdzqRChtQ%2FJ27PFalMvmVHUSxHp7pJiluNpz%2F3jn%2FBDwI4wOXFPXIwd%2BMeRyMWjTEBhLNP71lfEyJImvTKu1Z7LiWwSuyilVy2O3dmdkn%2FclAo5vec%2F94Cx%2FP%2Fw7SqWuwlvHNJoUHxyr4yXZHxR73J4RX0Gbeg%2FKXw3J41QjZ4Jg8OhEC8Ih0EYI9CojYvZ4ZNZdJlNyXJYbt7vWZD976K20Xlo8YqKEM47Ng%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAX5ZI6PDWYRIYUHJ2%2F20241202%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20241202T094339Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=a4167e23ad6b5dd484fdb0e714bbeb6ac626ac34a4a37d010887f9b5d27ae18d"
try:
    # Fetch the JSON file
    response = requests.get(presigned_url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse the JSON content
    firebase_credentials = response.json()

    # Initialize Firebase only if it's not initialized yet
    if not firebase_admin._apps:
        # Step 2: Pass the loaded JSON content to Firebase credentials
        cred = credentials.Certificate(firebase_credentials)  # Dynamically loaded credentials
        firebase_admin.initialize_app(cred, name='health')  # Initialize the Firebase app
        # Get Firestore database reference
        db = firestore.client()

    print("Firebase initialized successfully.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the JSON file: {e}")
except json.JSONDecodeError as e:
    print(f"Error parsing the JSON file: {e}")
except firebase_admin.exceptions.FirebaseError as e:
    print(f"Error initializing Firebase: {e}")

# if not firebase_admin._apps:
#     # Initialize Firebase Admin SDK
#     cred = credentials.Certificate(firebase_credentials)  # Ensure the correct path to your credentials
#     firebase_admin.initialize_app(cred, name='health')




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
