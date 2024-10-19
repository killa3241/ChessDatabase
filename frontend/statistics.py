# statistics.py

import streamlit as st

def display_statistics():
    st.title("Statistics")
    
    st.write("""
    Here you can find statistics related to player performance and game outcomes.
    """)
    
    # Example statistics data (this should ideally come from a database)
    st.write("### Overall Statistics")
    st.write("Total Games Played: 5000")
    st.write("Total Tournaments Held: 200")
    st.write("Average Player Rating: 2500")
