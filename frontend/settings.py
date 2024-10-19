# settings.py

import streamlit as st

def display_settings():
    st.title("Settings")
    
    st.write("""
    Manage your account settings here.
    """)
    
    # Placeholder for settings options
    st.write("### Account Settings")
    st.text_input("Change Username")
    st.text_input("Change Password", type="password")
    st.button("Update Settings")
