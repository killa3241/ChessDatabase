# games.py

import streamlit as st

def display_games():
    st.title("Games")
    
    st.write("""
    Check out the latest games and their results.
    """)
    
    # Example game data (this should ideally come from a database)
    games = [
        {"White": "Magnus Carlsen", "Black": "Ian Nepomniachtchi", "Result": "1-0", "Date": "Oct 18, 2024"},
        {"White": "Fabiano Caruana", "Black": "Vishy Anand", "Result": "0.5-0.5", "Date": "Oct 17, 2024"},
        {"White": "Hikaru Nakamura", "Black": "Alireza Firouzja", "Result": "0-1", "Date": "Oct 16, 2024"}
    ]
    
    for game in games:
        st.subheader(f"{game['White']} vs {game['Black']}")
        st.write(f"**Result:** {game['Result']}")
        st.write(f"**Date:** {game['Date']}")
        st.markdown("---")
