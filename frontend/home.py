import streamlit as st
import pandas as pd

def display_home():
    # Main header for the homepage
    st.title("Welcome to Knight's Ledger")
    st.markdown("#### Your Chess Database Management System")

    # Introduction section with a nicer format
    st.markdown("""
    Knight's Ledger is a comprehensive platform for managing chess tournaments, 
    tracking game history, and analyzing player performance. Stay updated with 
    the latest tournament results, top player rankings, and your personal game stats, 
    all in one place.
    """)

    # File upload bar for PGN files
    st.markdown("---")
    st.subheader("Upload Your PGN File")
    uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")

    # Process the uploaded PGN file if it's not None
    if uploaded_file is not None:
        # Read and display the PGN file contents (assuming it's a text file)
        pgn_content = uploaded_file.read().decode("utf-8")
        st.text_area("PGN File Content", pgn_content, height=300)

        # Success message
        st.success("PGN file uploaded successfully!")

        # TODO: Add further processing, like parsing and storing in the database

    st.markdown("---")  # Horizontal separator

    # Split layout for displaying recent tournaments and user statistics
    # Display columns for recent tournaments and player statistics
    col1, col2 = st.columns(2)

    # Recent Tournaments section
    with col1:
        st.subheader("Recent Tournaments")
        tournaments = [
            {"Name": "City Open 2024", "Winner": "John Doe", "Date": "Oct 15, 2024"},
            {"Name": "National Chess Challenge", "Winner": "Jane Smith", "Date": "Oct 12, 2024"},
            {"Name": "Knight's Battle Royale", "Winner": "Arthur King", "Date": "Oct 10, 2024"}
        ]
        tournament_data = pd.DataFrame(tournaments)
        st.table(tournament_data)

    # Player Statistics section
    with col2:
        st.subheader("Top Player Rankings")
        players = [
            {"Player": "Magnus Carlsen", "Rating": 2847, "Games Played": 1250},
            {"Player": "Ian Nepomniachtchi", "Rating": 2789, "Games Played": 1180},
            {"Player": "Fabiano Caruana", "Rating": 2764, "Games Played": 1140}
        ]
        player_data = pd.DataFrame(players)
        st.table(player_data)

    st.markdown("---")

    # Section for recent games or other important information
    st.subheader("Recent Games")
    st.write("Below is a summary of some of the most recent games played:")

    # Sample game data (in practice, this would come from your database)
    games = [
        {"White": "Magnus Carlsen", "Black": "Ian Nepomniachtchi", "Result": "1-0", "Date": "Oct 18, 2024"},
        {"White": "Fabiano Caruana", "Black": "Vishy Anand", "Result": "0.5-0.5", "Date": "Oct 17, 2024"},
        {"White": "Hikaru Nakamura", "Black": "Alireza Firouzja", "Result": "0-1", "Date": "Oct 16, 2024"}
    ]

    # Display game data as a table
    game_data = pd.DataFrame(games)
    st.table(game_data)

    # Add an interactive feature: Filter recent games by player
    st.markdown("---")
    st.subheader("Filter Recent Games")
    selected_player = st.selectbox("Select a player:", options=["All"] + [game["White"] for game in games] + [game["Black"] for game in games])
    
    if selected_player != "All":
        filtered_games = game_data[(game_data["White"] == selected_player) | (game_data["Black"] == selected_player)]
    else:
        filtered_games = game_data

    st.write(f"Recent games for {selected_player}:")
    st.table(filtered_games)

# Call the display function when this script is run
if __name__ == "__main__":
    display_home()
