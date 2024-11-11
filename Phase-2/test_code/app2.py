import streamlit as st
from firebase import signup_user, login_user, check_existing_data
from data_collection import weekly_data
import re
from datetime import datetime
from dummy_data3 import fetch_data_main
from dashboard import start_dashboard

# Validate email format
def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Function to show messages
def show_message(message: str, is_error: bool = False):
    if is_error:
        st.error(message)
    else:
        st.success(message)

def calculate_age(dob: datetime) -> int:
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Signup Page
def signup_page():
    st.title("Sign Up")
    email = st.text_input("Email", key="signup_email")
    username = st.text_input("Username", key="signup_username")
    
    # New fields
    dob = st.date_input("Date of Birth", key="signup_dob", min_value=datetime(1900, 1, 1), max_value=datetime.today())
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="signup_gender")
    blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="signup_blood_type")

    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    
    if st.button("Sign Up"):
        # Check all fields are filled
        if not email or not username or not password or not confirm_password or not dob or not gender or not blood_type:
            show_message("Please fill in all fields", True)
            return

        # Validate email format
        if not is_valid_email(email):
            show_message("Invalid email format", True)
            return

        # Check password match
        if password != confirm_password:
            show_message("Passwords do not match", True)
            return

        # Calculate age from date of birth
        age = calculate_age(dob)

        # Attempt signup
        success, message, uid = signup_user(email, password, username, age, gender, blood_type)
        
        if success:
            show_message(message)
            st.session_state['uid'] = uid
            st.session_state['logged_in'] = True  # Set login state to true
            st.experimental_rerun()  # Rerun the app to go to the main page
        else:
            show_message(message, True)

# Login Page
def login_page():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if not email or not password:
            show_message("Please fill in both fields", True)
            return

        success, message, uid = login_user(email, password)
        
        if success:
            show_message(message)
            st.session_state['logged_in'] = True  # Set login state to true
            st.session_state['uid'] = uid  # Save the user ID in session
            
            st.experimental_rerun()  # Rerun to go to the main page
        else:
            show_message(message, True)

# Main Data Collection Page
def main_data_collection_page():
    
    if check_existing_data(st.session_state['uid']):
        start_dashboard() # Redirect to dashboard
    else:
        weekly_data()  # Call the weekly_data function from data_collection.py

    # Logout button
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['uid'] = None
        st.experimental_rerun()

# Main function to manage the flow between Login, SignUp, and Data Collection pages
def main():
    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Render pages based on login state
    if st.session_state['logged_in']:
        main_data_collection_page()  # Show data collection page if logged in
    else:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            login_page()
        with tab2:
            signup_page()

if __name__ == "__main__":
    main()
