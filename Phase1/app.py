import streamlit as st
from auth import sign_up, sign_in, google_auth
from data_collection import collect_health_data, export_data
import sqlite3

# Establish a database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Main App
st.title("Health Data Analytics Platform")

# Toggle between sign-up and sign-in
option = st.sidebar.selectbox("Choose action", ["Sign Up", "Sign In", "Google Sign-In"])

if option == "Sign Up":
    # Sign up form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    if st.button("Sign Up"):
        sign_up(username, password, email)

elif option == "Sign In":
    # Sign in form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        user = sign_in(username, password)
        if user:
            st.success(f"Welcome back, {username}!")
            collect_health_data(user[0])  # Collect health data if user is authenticated
            export_data(user[0])  # Option to export data
        else:
            st.error("Invalid username or password.")

elif option == "Google Sign-In":
    st.write("Google Authentication")
    if st.button("Login with Google"):
        google_auth()
