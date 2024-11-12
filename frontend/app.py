import streamlit as st
from navbar import display_sidebar
from home import display_home

st.set_page_config(page_title="Knight's Ledger", layout="wide")

def main_app():
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        display_sidebar()
    else:
        st.warning("Please log in to access the application.")
        st.session_state['current_page'] = "login"
        st.stop()  

if __name__ == "__main__":
    main_app()