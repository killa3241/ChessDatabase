# navbar.py

import streamlit as st

def display_sidebar():
    # Custom CSS for sidebar
    st.markdown("""
        <style>
        .sidebar {
            display: flex;
            flex-direction: column;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }
        .sidebar a {
            padding: 12px 20px;
            text-decoration: none;
            font-size: 18px;
            color: #333;
            border-radius: 5px;
            margin: 5px 0;
        }
        .sidebar a:hover {
            background-color: #ddd;
        }
        .search-icon {
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display sidebar
    with st.sidebar:
        st.markdown("<h3 style='text-align: center;'>Knight's Ledger</h3>", unsafe_allow_html=True)
        
        # Add navigation links
        st.markdown("<div class='sidebar'>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Tournaments</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Games</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>User Profiles</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Rankings</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Statistics</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Settings</a>", unsafe_allow_html=True)
        st.markdown("<a href='#'>Support</a>", unsafe_allow_html=True)
        
        # Search icon
        st.markdown("<div class='search-icon' onclick='openSearch()'>🔍 Search</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# Function to handle search click
def display_search_input():
    search_term = st.text_input("Search tournaments, games or players", "")
