import streamlit as st
import pandas as pd
import mysql.connector
from io import StringIO
from pathlib import Path
import sys
import uuid

# Add backend path for module imports
backend_path = Path(__file__).resolve().parent.parent / 'backend'
sys.path.append(str(backend_path))

from pgn_parser import parse_pgn  # Import the PGN parser function

# Mapping of PGN time controls to ENUM values
time_control_mapping = {
    'Classical': 'Classical',
    'Rapid': 'Rapid',
    'Blitz': 'Blitz',
    'Bullet': 'Bullet'
}

def get_or_create_player(connection, player_name):
    """Fetches the player_id if exists, otherwise inserts the player with a unique alphanumeric ID and returns the new player_id."""
    cursor = connection.cursor()

    # Check if player exists
    select_player_query = "SELECT player_id FROM player WHERE name = %s"
    cursor.execute(select_player_query, (player_name,))
    player = cursor.fetchone()

    if player:
        return player[0]

    # Generate a unique alphanumeric player_id
    player_id = uuid.uuid4().hex[:15]  # Generates a 15-character alphanumeric ID
    insert_player_query = "INSERT INTO player (player_id, name) VALUES (%s, %s)"
    cursor.execute(insert_player_query, (player_id, player_name))
    connection.commit()
    
    return player_id

def insert_game_and_moves_to_db(connection, parsed_game):
    cursor = connection.cursor()

    # Get or create player IDs for white and black players
    white_id = get_or_create_player(connection, parsed_game.players['white'].get('name', 'Unknown'))
    black_id = get_or_create_player(connection, parsed_game.players['black'].get('name', 'Unknown'))

    # Map the time control to ENUM values or default to 'Classical'
    game_type = parsed_game.game.get('time_control', 'Classical')
    game_type = time_control_mapping.get(game_type, 'Classical')

    # Insert the game record into the `game` table
    insert_game_query = """
    INSERT INTO game (site, date, white_name, white_id, black_name, black_id, result, type, white_elo, black_elo, termination, eco, endtime, link, number_of_moves, tournament_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
    """
    game_data = (
        parsed_game.game.get('site', 'Unknown'),
        parsed_game.tournament.get('date', '0000.00.00'),
        parsed_game.players['white'].get('name', 'Unknown'),
        white_id,
        parsed_game.players['black'].get('name', 'Unknown'),
        black_id,
        parsed_game.game.get('result', '*'),
        game_type,  # Ensured ENUM type
        parsed_game.players['white'].get('elo'),
        parsed_game.players['black'].get('elo'),
        parsed_game.game.get('termination', 'Unknown'),
        parsed_game.game.get('eco', 'N/A'),
        parsed_game.game.get('endtime'),
        parsed_game.game.get('link'),
        len(parsed_game.moves)
    )
    cursor.execute(insert_game_query, game_data)
    game_id = cursor.lastrowid  # Get the ID of the inserted game

    # Insert moves into the `move` table
    insert_move_query = """
    INSERT INTO move (game_id, move_number, white_move, black_move)
    VALUES (%s, %s, %s, %s)
    """
    for move in parsed_game.moves:
        move_data = (game_id, move['move_number'], move['white_move'], move.get('black_move'))
        cursor.execute(insert_move_query, move_data)

    # Commit the transaction
    connection.commit()
    cursor.close()

def display_home():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="chess_admin",
        password="Chessadmin1",
        database="chess_db"
    )

    st.title("Welcome to Knight's Ledger")
    st.markdown("#### Your Chess Database Management System")

    st.subheader("Upload Your PGN File")
    uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")

    if uploaded_file is not None:
        # Convert the uploaded file to a string-based IO
        pgn_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        st.text_area("PGN File Content", pgn_content, height=300)

        # Parse the PGN content
        parsed_games = parse_pgn(pgn_content)
        st.success("PGN file parsed successfully!")

        # Insert parsed games and moves into the database
        for parsed_game in parsed_games:
            insert_game_and_moves_to_db(connection, parsed_game)

        st.success("Game data and moves have been inserted into the database!")

    # Close the connection
    connection.close()

    # Display additional sections
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Tournaments")
        tournaments = [
            {"Name": "City Open 2024", "Winner": "John Doe", "Date": "Oct 15, 2024"},
            {"Name": "National Chess Challenge", "Winner": "Jane Smith", "Date": "Oct 12, 2024"},
            {"Name": "Knight's Battle Royale", "Winner": "Arthur King", "Date": "Oct 10, 2024"}
        ]
        tournament_data = pd.DataFrame(tournaments)
        st.table(tournament_data)

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
    st.subheader("Recent Games")
    games = [
        {"White": "Magnus Carlsen", "Black": "Ian Nepomniachtchi", "Result": "1-0", "Date": "Oct 18, 2024"},
        {"White": "Fabiano Caruana", "Black": "Vishy Anand", "Result": "0.5-0.5", "Date": "Oct 17, 2024"},
        {"White": "Hikaru Nakamura", "Black": "Alireza Firouzja", "Result": "0-1", "Date": "Oct 16, 2024"}
    ]
    game_data = pd.DataFrame(games)
    st.table(game_data)

    st.markdown("---")
    st.subheader("Filter Recent Games")
    selected_player = st.selectbox("Select a player:", options=["All"] + [game["White"] for game in games] + [game["Black"] for game in games])
    
    if selected_player != "All":
        filtered_games = game_data[(game_data["White"] == selected_player) | (game_data["Black"] == selected_player)]
    else:
        filtered_games = game_data

    st.write(f"Recent games for {selected_player}:")
    st.table(filtered_games)

if __name__ == "__main__":
    display_home()
