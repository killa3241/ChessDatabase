import streamlit as st
import mysql.connector
import hashlib
import uuid
from app import main_app  # Import the main app function from app.py
from admin import admin_dashboard, connect_to_db  

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the player already exists
def player_exists(cursor, email):
    query = "SELECT * FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

def generate_unique_player_id(cursor):
    while True:
        player_id = uuid.uuid4().hex[:15]
        # Check if the player_id already exists in the database
        cursor.execute("SELECT 1 FROM player WHERE player_id = %s", (player_id,))
        if cursor.fetchone() is None:
            return player_id

# Function to add a new player (used during registration)
def add_player(cursor, db, email, password):
    player_id = generate_unique_player_id(cursor)  
    query = "INSERT INTO player (player_id, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (player_id, email, hash_password(password)))
    db.commit()

# Streamlit app for login and registration
def login_page():
    if not st.session_state.get('logged_in', False):
        st.title("Chess Database Login")
    elif st.session_state.get('is_admin', False):
        st.title("Admin Dashboard")
    else:
        st.title("User Dashboard")

    # Initialize session state for login tracking
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_email'] = None
        st.session_state['admin_id'] = None
        st.session_state['page'] = "login"

    # If the user is already logged in, display the main app or admin dashboard
    if st.session_state['logged_in']:
        if st.session_state.get('is_admin', False):
            admin_dashboard()  # Display admin dashboard
        else:
            main_app()  # Display main app from app.py
        return  # Exit the login form

    # Login type selection: User Login or Admin Login
    login_type = st.radio("Login as:", ["User", "Admin"])

    # Connect to the database with default credentials
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if login_type == "User":
        option = st.selectbox("Select an option", ["Login", "Register"])

        # Email and Password input fields for user login/registration
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        if option == "Login":
            if st.button("Login"):
                user = player_exists(cursor, email)
                if user:
                    if user['password'] == hash_password(password):
                        st.success("Login successful!")
                        # Store login state
                        st.session_state['logged_in'] = True
                        st.session_state['user_email'] = email
                        st.session_state['page'] = "Home"
                        st.session_state['is_admin'] = False
                        st.rerun()
                    else:
                            st.error("Incorrect email or password.")
                else:
                    st.error("User not found. Please register first.")
        
        elif option == "Register":
            if st.button("Register"):
                if player_exists(cursor, email):
                    st.warning("User with this email already exists. Please login.")
                else:
                    add_player(cursor, db, email, password)
                    st.success("Registration successful!")
                    st.session_state['logged_in'] = True
                    st.session_state['user_email'] = email
                    st.session_state['page'] = "Home"
                    st.session_state['is_admin'] = False
                    st.rerun()

    elif login_type == "Admin":
        # Admin ID and Password input fields
        admin_id = st.text_input("Admin ID", placeholder="Enter admin ID")
        admin_password = st.text_input("Password", placeholder="Enter your password", type="password")

        if st.button("Login"):
            # Attempt to connect to MySQL as admin using provided credentials
            try:
                # Test connection as admin
                admin_db = connect_to_db(user=admin_id, password=admin_password)
                admin_db.close()  # Close immediately after successful test

                st.success("Admin login successful!")
                # Store admin login state
                st.session_state['logged_in'] = True
                st.session_state['admin_id'] = admin_id
                st.session_state['is_admin'] = True  # Track admin state
                st.session_state['page'] = "Admin Dashboard"
                st.rerun()
            except mysql.connector.Error as err:
                st.error("Admin login failed. Check your ID and password.")

    # Logout functionality
    if st.session_state['logged_in'] and st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_email'] = None
        st.session_state['admin_id'] = None
        st.session_state['is_admin'] = False  # Reset admin state
        st.success("You have been logged out.")
        st.rerun()

    # Close the database connection
    cursor.close()
    db.close()

# Call the login page function
if __name__ == "__main__":
    login_page()
