# File: frontend/db_utils.py

import mysql.connector
import streamlit as st

def connect_to_db():
    """Establishes a connection to the MySQL database using Streamlit secrets."""
    try:
        return mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database="chess_db"
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        st.stop()  # Stop the app on a critical connection error