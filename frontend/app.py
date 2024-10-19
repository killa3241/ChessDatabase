# app.py

import streamlit as st
from navbar import display_sidebar
from home import display_home

# Set page config
st.set_page_config(page_title="Knight's Ledger", layout="wide")

# Display the sidebar
display_sidebar()


