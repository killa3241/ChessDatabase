import streamlit as st
import mysql.connector
from datetime import datetime

# Database connection (adjust parameters as per your database configuration)
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="chess_admin",
        password="Chessadmin1",
        database="chess_db" 
    )
    return connection

def insert_tournament(name, date, duration, location, type, organizer):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # SQL query to insert tournament data
    query = """
    INSERT INTO tournament (name, date, duration, location, type, organizer)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, date, duration, location, type, organizer))
    
    connection.commit()
    cursor.close()
    connection.close()

def display_tournaments():
    st.title("Tournaments")
    
    st.write("""
    Here you can find information about upcoming and past tournaments.
    """)

    # Display form to add a new tournament
    st.subheader("Add a New Tournament")
    with st.form("tournament_form"):
        name = st.text_input("Tournament Name")
        date = st.date_input("Date")
        duration = st.number_input("Duration (in days)", min_value=1, step=1)
        location = st.text_input("Location")
        type = st.selectbox("Tournament Type", ['Round Robin', 'Knock Out', 'Swiss System', 'Scheveningen System'])
        organizer = st.text_input("Organizer", value="Unknown")
        
        # Form submission
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Insert data into the database
            try:
                insert_tournament(name, date, duration, location, type, organizer)
                st.success(f"Tournament '{name}' added successfully!")
            except Exception as e:
                st.error("Error adding tournament to database.")
                st.write(e)

    # Example display of existing tournaments (Replace with database data if needed)
    tournaments = [
        {"Name": "City Open 2024", "Date": "Oct 15, 2024", "Location": "New York", "Participants": 100},
        {"Name": "National Chess Challenge", "Date": "Oct 12, 2024", "Location": "Los Angeles", "Participants": 150},
        {"Name": "Knight's Battle Royale", "Date": "Oct 10, 2024", "Location": "San Francisco", "Participants": 80}
    ]
    
    for tournament in tournaments:
        st.subheader(tournament['Name'])
        st.write(f"**Date:** {tournament['Date']}")
        st.write(f"**Location:** {tournament['Location']}")
        st.write(f"**Participants:** {tournament['Participants']}")
        st.markdown("---")
