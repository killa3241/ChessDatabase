# File: frontend/yourprofile.py

import streamlit as st
import mysql.connector
from db_utils import connect_to_db
import pandas as pd

def get_user_info(cursor, email):
    """Fetches user profile information from the database."""
    query = "SELECT name, country, rating, online_profile, date_of_birth, gender FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

def update_user_info(cursor, db, email, name, country, rating, online_profile, date_of_birth, gender):
    """Updates user profile information in the database."""
    query = """
    UPDATE player
    SET name = %s, country = %s, rating = %s, online_profile = %s, date_of_birth = %s, gender = %s
    WHERE email = %s
    """
    cursor.execute(query, (name, country, rating, online_profile, date_of_birth, gender, email))
    db.commit()

def display_profile():
    st.title("Your Profile")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Please log in to access your profile.")
        return

    email = st.session_state['user_email']
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        user_info = get_user_info(cursor, email)
        
        if user_info:
            st.subheader("Current Information")
            st.text(f"Name: {user_info['name'] if user_info['name'] else 'Not set'}")
            st.text(f"Country: {user_info['country'] if user_info['country'] else 'Not set'}")
            st.text(f"Rating: {user_info['rating'] if user_info['rating'] else 'Not set'}")
            st.text(f"Online Profile: {user_info['online_profile'] if user_info['online_profile'] else 'Not set'}")
            st.text(f"Date of Birth: {user_info['date_of_birth'] if user_info['date_of_birth'] else 'Not set'}")
            st.text(f"Gender: {user_info['gender'] if user_info['gender'] else 'Not set'}")

            st.subheader("Update Your Information")
            with st.form("profile_form"):
                name = st.text_input("Name", value=user_info['name'] or "")
                country = st.text_input("Country", value=user_info['country'] or "")
                rating = st.number_input("Rating", value=user_info['rating'] or 0, min_value=0)
                online_profile = st.text_input("Online Profile", value=user_info['online_profile'] or "")
                date_of_birth = st.date_input("Date of Birth", value=user_info['date_of_birth'] if user_info['date_of_birth'] else None)
                gender_options = ['Male', 'Female', 'Other']
                gender_index = gender_options.index(user_info['gender']) if user_info['gender'] else 0
                gender = st.selectbox("Gender", options=gender_options, index=gender_index)

                if st.form_submit_button("Update Information"):
                    update_user_info(cursor, connection, email, name, country, rating, online_profile, date_of_birth, gender)
                    st.success("Your information has been updated!")
                    st.rerun()
        else:
            st.error("Failed to load user information.")

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    display_profile()