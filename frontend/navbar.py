# File: frontend/navbar.py

import streamlit as st
import mysql.connector

# Import all page display functions
from home import display_home
from yourprofile import display_profile
from tournaments import display_tournaments
from games import display_games
from rankings import display_rankings
from statistics import display_statistics
from support import display_support

def display_sidebar():
    """Displays the navigation sidebar with buttons."""
    st.markdown("""
        <style>
        .sidebar {
            display: flex;
            flex-direction: column;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }
        .sidebar .sidebar-title {
            text-align: center;
            font-size: 24px;
            color: #496C9F;
            margin-bottom: 20px;
        }
        .sidebar button {
            margin: 5px 0;
            padding: 10px;
            border: none;
            background-color: #e7e7e7;
            color: #333;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s;
        }
        .sidebar button:hover {
            background-color: #ddd;
        }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("<div class='sidebar-title'>CONTENTS</div>", unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state.page = "Home"  # Default 

    # Buttons for navigation
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("Your Profile"): 
        st.session_state.page = "Your Profile"
    if st.sidebar.button("Tournaments"):
        st.session_state.page = "Tournaments"
    if st.sidebar.button("Games"):
        st.session_state.page = "Games"
    if st.sidebar.button("Rankings"):
        st.session_state.page = "Rankings"
    if st.sidebar.button("Statistics"):
        st.session_state.page = "Statistics"
    # if st.sidebar.button("Best moves"):
    #     st.session_state.page = "Best Move"
    if st.sidebar.button("Support"):
        st.session_state.page = "Support"
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.update({
            "logged_in": False,
            "user_email": None,
            "page": "login" 
        })
        st.rerun()

    # Dictionary mapping page names to their display functions
    pages = {
        "Home": display_home,
        "Your Profile": display_profile,
        "Tournaments": display_tournaments,
        "Games": display_games,
        "Rankings": display_rankings,
        "Statistics": display_statistics,
        "Support": display_support
    }

    # Call the appropriate function based on the current page
    if st.session_state.page in pages:
        pages[st.session_state.page]()
    else:
        # Handle cases where the page is not in the dictionary (e.g., login page)
        st.write("") # Do nothing, the main app file will handle it.