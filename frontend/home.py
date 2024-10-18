# home.py

import streamlit as st
from navbar import display_sidebar, display_search_input

def display_home():
    # Display the sidebar
    display_sidebar()

    # Check if search term is requested
    if st.session_state.get('show_search', False):
        display_search_input()

    # Welcome Banner
    st.markdown("<h2 style='text-align: center;'>Welcome to Knight's Ledger</h2>", unsafe_allow_html=True)

    # Layout for Recent Tournaments, Latest Games, User Profile Summary
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("<h3 style='text-align: center;'>Recent Tournaments</h3>", unsafe_allow_html=True)
        st.write("• Tournament A")
        st.write("• Tournament B")
        st.write("• Tournament C")

    with col2:
        st.markdown("<h3 style='text-align: center;'>Latest Games</h3>", unsafe_allow_html=True)
        st.write("Game 1: Player A vs Player B")
        st.write("Game 2: Player C vs Player D")
        st.write("Game 3: Player E vs Player F")

    with col3:
        st.markdown("<h3 style='text-align: center;'>User Profile Summary</h3>", unsafe_allow_html=True)
        st.write("Name: John Doe")
        st.write("Rating: 1200")
        st.write("Games Played: 150")
        st.write("Tournaments Won: 3")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 Knight's Ledger</p>", unsafe_allow_html=True)

# Initialize session state for search visibility
if 'show_search' not in st.session_state:
    st.session_state.show_search = False

# Callback function for toggling search input
def toggle_search():
    st.session_state.show_search = not st.session_state.show_search
