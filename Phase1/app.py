import streamlit as st
from auth import sign_up, sign_in, google_auth
from data_collection import collect_health_data, export_data
import sqlite3

# Establish a database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Main App
st.title("Health Data Analytics Platform")

# Toggle between sign-up, sign-in, and sign-out
if st.session_state.logged_in:
    st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({"logged_in": False, "user_id": None}))
    st.success(f"Welcome back, {st.session_state.user_id}!")
    # Load data collection and export if signed in
    collect_health_data(st.session_state.user_id)
    export_data(st.session_state.user_id)
else:
    option = st.sidebar.selectbox("Choose action", ["Sign Up", "Sign In", "Google Sign-In"])

    if option == "Sign Up":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        if st.button("Sign Up"):
            sign_up(username, password, email)

    elif option == "Sign In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            user = sign_in(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]  # Store user ID in session
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

    elif option == "Google Sign-In":
        st.write("Google Authentication")
        if st.button("Login with Google"):
            google_auth()
