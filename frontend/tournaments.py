# tournaments.py

import streamlit as st

def display_tournaments():
    st.title("Tournaments")
    
    st.write("""
    Here you can find information about upcoming and past tournaments.
    """)
    
    # Example tournament data (this should ideally come from a database)
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
