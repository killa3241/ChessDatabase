import streamlit as st
import mysql.connector
import hashlib
from app import main_app  # Import the main app function from app.py

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="chess_admin",
        password="Chessadmin1",
        database="chess_db"
    )

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the player already exists
def player_exists(cursor, email):
    query = "SELECT * FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

# Function to add a new player
def add_player(cursor, db, email, password):
    query = "INSERT INTO player (email, password) VALUES (%s, %s)"
    cursor.execute(query, (email, hash_password(password)))
    db.commit()

# Streamlit app for login and registration
def login_page():
    st.title("Chess Database Login")

    # Initialize session state for login tracking
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_email'] = None
        st.session_state['page'] = "login"
    # If the user is logged in, display app.py instead of login form
    if st.session_state['logged_in']:
        main_app()  # Display main app from app.py
        return  # Exit the login form

    # Login or Register selection
    option = st.selectbox("Select an option", ["Login", "Register"])

    # Email and Password input fields
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    # Connect to the database
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if option == "Login":
        if st.button("Login"):
            user = player_exists(cursor, email)
            if user and user['password'] == hash_password(password):
                st.success("Login successful!")
                # Store login state
                st.session_state['logged_in'] = True
                st.session_state['user_email'] = email
                st.session_state['page'] = "Home"
            else:
                st.error("Incorrect email or password.")
    
    elif option == "Register":
        if st.button("Register"):
            if player_exists(cursor, email):
                st.warning("User with this email already exists. Please login.")
            else:
                add_player(cursor, db, email, password)
                st.success("Registration successful! You can now log in.")

    # Close the database connection
    cursor.close()
    db.close()

    # Check login status again and display the main app if logged in
    if st.session_state['logged_in']:
        main_app()  # Call main app from app.py after successful login or registration

# Call the login page function
if __name__ == "__main__":
    login_page()