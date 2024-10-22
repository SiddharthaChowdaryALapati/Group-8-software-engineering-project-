import sqlite3
import os
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Determine the path of the current script and place the database in the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'users.db')

# Database setup
conn = sqlite3.connect(users.db)
c = conn.cursor()

# Create a user table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
    )
''')
conn.commit()

# Function for signing up new users
def sign_up(username, password, email):
    c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
    conn.commit()
    st.success("Account created successfully! You can now log in.")

# Function for signing in users
def sign_in(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    return c.fetchone()

# Google Authentication
def google_auth():
    client_id = 'your-google-client-id'
    client_secret = 'your-google-client-secret'

    # OAuth2Session to manage the authentication
    session = OAuth2Session(client_id, client_secret)
    authorization_url, state = session.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )
    st.write(f"Login with Google: {authorization_url}")
