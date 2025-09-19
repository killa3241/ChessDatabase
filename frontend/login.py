
import streamlit as st
import mysql.connector
import hashlib
import uuid
from app import main_app
from admin import admin_dashboard
from db_utils import connect_to_db  # Import the centralized connection function

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def player_exists(cursor, email):
    query = "SELECT password FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

def generate_unique_player_id(cursor):
    while True:
        player_id = uuid.uuid4().hex[:15].upper()
        cursor.execute("SELECT 1 FROM player WHERE player_id = %s", (player_id,))
        if cursor.fetchone() is None:
            return player_id

def add_player(cursor, db, email, password):
    player_id = generate_unique_player_id(cursor)
    query = "INSERT INTO player (player_id, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (player_id, email, hash_password(password)))
    db.commit()

def login_page():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_email'] = None
        st.session_state['is_admin'] = False

    if st.session_state['logged_in']:
        if st.session_state.get('is_admin'):
            admin_dashboard()
        else:
            main_app()
        if st.button("Logout"):
            st.session_state.update({
                'logged_in': False,
                'user_email': None,
                'is_admin': False
            })
            st.success("You have been logged out.")
            st.rerun()
        return

    st.title("Chess Database Login")
    login_type = st.radio("Login as:", ["User", "Admin"])

    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)

        if login_type == "User":
            option = st.selectbox("Select an option", ["Login", "Register"])
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", placeholder="Enter your password", type="password")

            if option == "Login":
                if st.button("Login"):
                    user = player_exists(cursor, email)
                    if user and user['password'] == hash_password(password):
                        st.success("Login successful!")
                        st.session_state['logged_in'] = True
                        st.session_state['user_email'] = email
                        st.session_state['is_admin'] = False
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")
            elif option == "Register":
                if st.button("Register"):
                    if player_exists(cursor, email):
                        st.warning("User with this email already exists. Please login.")
                    else:
                        add_player(cursor, db, email, password)
                        st.success("Registration successful! You can now log in.")
                        st.session_state['logged_in'] = True
                        st.session_state['user_email'] = email
                        st.session_state['is_admin'] = False
                        st.rerun()

        elif login_type == "Admin":
            admin_id = st.text_input("Admin ID", placeholder="Enter admin ID")
            admin_password = st.text_input("Password", placeholder="Enter your password", type="password")

            if st.button("Login"):
                if admin_id == st.secrets["ADMIN_ID"] and hash_password(admin_password) == st.secrets["ADMIN_PASSWORD"]:
                    st.success("Admin login successful!")
                    st.session_state['logged_in'] = True
                    st.session_state['is_admin'] = True
                    st.rerun()
                else:
                    st.error("Admin login failed. Check your ID and password.")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    login_page()