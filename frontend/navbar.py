import streamlit as st

def create_sidebar_item(icon_path, label):
    """Create a sidebar item with an icon and label."""
    st.markdown("<a href='#'>", unsafe_allow_html=True)
    st.image(icon_path, width=24, use_column_width=False)
    st.markdown(f"<span>{label}</span></a>", unsafe_allow_html=True)

def display_sidebar():
    with st.sidebar:
        st.markdown("<h3 style='text-align: center; margin: 0;'>Knight's Ledger</h3>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar'>", unsafe_allow_html=True)

        # Create sidebar items using the helper function
        create_sidebar_item('assets/icons/tournament.png', 'Tournaments')
        create_sidebar_item('assets/icons/game.png', 'Games')
        create_sidebar_item('assets/icons/user.png', 'User')
        create_sidebar_item('assets/icons/profiles.png', 'Profiles')
        create_sidebar_item('assets/icons/ranking.png', 'Rankings')
        create_sidebar_item('assets/icons/statistics.png', 'Statistics')
        create_sidebar_item('assets/icons/settings.png', 'Settings')
        create_sidebar_item('assets/icons/support.png', 'Support')

        st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar CSS
    st.markdown("""
        <style>
        .sidebar {
            display: flex;
            flex-direction: column;
            padding: 0; /* Remove padding */
            margin: 0; /* Remove margin */
            background-color: #f9f9f9;
            border-radius: 8px;
            width: 250px; /* Sidebar width */
            transition: width 0.3s ease-in-out;
        }
        .sidebar a {
            display: flex; /* Use flex to align icon and text */
            align-items: center; /* Center items vertically */
            padding: 10px 20px; /* Adjust padding as needed */
            text-decoration: none;
            font-size: 18px;
            color: #333;
            border-radius: 5px;
            margin: 0; /* Remove margin */
        }
        .sidebar a:hover {
            background-color: #ddd;
        }
        </style>
    """, unsafe_allow_html=True)
