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

    # Sidebar header
    st.sidebar.markdown("<div class='sidebar-title'>CONTENTS</div>", unsafe_allow_html=True)

    # Initialize page variable if not already in session state
    if 'page' not in st.session_state:
        st.session_state.page = "Home"  # Default to Home

    # Navigation buttons
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
    '''
    if st.sidebar.button("Best moves"):
        st.session_state.page = "Best Move"
    '''
    if st.sidebar.button("Support"):
        st.session_state.page = "Support"

    if st.sidebar.button("Logout"):
        st.session_state.update({
        "logged_in": False,
        "user_email": None,
        "page": "login"  
    })
        st.rerun()
    # Display the selected page
    if st.session_state.page == "Home":
        from home import display_home
        display_home()
    elif st.session_state.page == "Your Profile":
        from yourprofile import display_profile
        display_profile()
    elif st.session_state.page == "Tournaments":
        from tournaments import display_tournaments
        display_tournaments()
    elif st.session_state.page == "Games":
        from games import display_games
        display_games()
    elif st.session_state.page == "Rankings":
        from rankings import display_rankings
        display_rankings()
    elif st.session_state.page == "Statistics":
        from statistics import display_statistics
        display_statistics()
    #elif st.session_state.page == "Best Move":
    #    from get_bestmove import fetch_and_display_best_move
    #    fetch_and_display_best_move()
    elif st.session_state.page == "Support":
        from support import display_support
        display_support()
