import streamlit as st
import os

def display_chess_analysis():
    st.title("Chess Analysis")

    # Load the HTML file from the static directory
    html_file_path = os.path.join("static", "index.html")

    # Check if the HTML file exists
    if os.path.exists(html_file_path):
        # Read and display the HTML content
        with open(html_file_path, "r") as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=600)  # Adjust height as needed
    else:
        st.error("HTML file not found. Please check the path.")


