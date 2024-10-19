# rankings.py

import streamlit as st

def display_rankings():
    st.title("Rankings")
    
    st.write("""
    Here you can find the top player rankings.
    """)
    
    # Example ranking data (this should ideally come from a database)
    rankings = [
        {"Player": "Magnus Carlsen", "Ranking": 1, "Rating": 2847},
        {"Player": "Ian Nepomniachtchi", "Ranking": 2, "Rating": 2789},
        {"Player": "Fabiano Caruana", "Ranking": 3, "Rating": 2764}
    ]
    
    for rank in rankings:
        st.subheader(f"#{rank['Ranking']} - {rank['Player']}")
        st.write(f"**Rating:** {rank['Rating']}")
        st.markdown("---")
