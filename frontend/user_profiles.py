# user_profiles.py

import streamlit as st

def display_user_profiles():
    st.title("User Profiles")
    
    st.write("""
    Here you can find profiles of players.
    """)
    
    # Example user data (this should ideally come from a database)
    users = [
        {"Username": "MagnusCarlsen", "Rating": 2847, "Games Played": 1250},
        {"Username": "IanNepomniachtchi", "Rating": 2789, "Games Played": 1180},
        {"Username": "FabianoCaruana", "Rating": 2764, "Games Played": 1140}
    ]
    
    for user in users:
        st.subheader(user['Username'])
        st.write(f"**Rating:** {user['Rating']}")
        st.write(f"**Games Played:** {user['Games Played']}")
        st.markdown("---")
