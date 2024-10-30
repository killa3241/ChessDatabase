import streamlit as st
from navbar import display_sidebar
from home import display_home

# Set page config (only at the beginning of the script)
st.set_page_config(page_title="Knight's Ledger", layout="wide")

# Main app function
def main_app():
    # Check if the user is logged in
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        # Display the sidebar and main content
        display_sidebar()
        display_home()  # Your main app content goes here
    else:
        st.warning("Please log in to access the application.")

# Run the main app function
if __name__ == "__main__":
    main_app()
