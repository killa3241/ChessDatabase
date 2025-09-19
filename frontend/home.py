# File: frontend/home.py

import streamlit as st
from io import StringIO
import sys
from pathlib import Path
import mysql.connector

# Import the centralized database utility
from db_utils import connect_to_db

# Append the backend path to the system path to allow imports
backend_path = Path(__file__).resolve().parent.parent / 'backend'
sys.path.append(str(backend_path))
from pgn_parser import parse_pgn

def get_or_create_player(connection, player_name):
    """Fetches player_id or creates a new player."""
    cursor = connection.cursor()
    select_player_query = "SELECT player_id FROM player WHERE name = %s"
    cursor.execute(select_player_query, (player_name,))
    player = cursor.fetchone()

    if player:
        return player[0]

    import uuid
    player_id = uuid.uuid4().hex[:15].upper()
    insert_player_query = "INSERT INTO player (player_id, name) VALUES (%s, %s)"
    cursor.execute(insert_player_query, (player_id, player_name))
    connection.commit()
    
    return player_id

def generate_game_id():
    """Generates a unique game ID."""
    import uuid
    return uuid.uuid4().hex[:8].upper()

def parse_time_control(time_control_str):
    """Parses and formats the time control string."""
    import re
    if time_control_str == "?" or time_control_str == "-":
        return "Unknown"
    
    if re.match(r'^\d+$', time_control_str):
        seconds = int(time_control_str)
        if seconds <= 180: return "Bullet"
        elif seconds <= 600: return "Blitz"
        elif seconds <= 1800: return "Rapid"
        return "Classical"
    
    if re.match(r'^\d+\+\d+$', time_control_str):
        initial, increment = time_control_str.split('+')
        initial = int(initial)
        if initial <= 180: return "Bullet"
        elif initial <= 600: return "Blitz"
        elif initial <= 1800: return "Rapid"
        return "Classical"
        
    return "Unknown"

def insert_game_and_moves_to_db(connection, parsed_game):
    """Inserts a single game and its moves into the database."""
    cursor = connection.cursor()

    white_name = parsed_game.players['white'].get('name', 'Unknown')
    black_name = parsed_game.players['black'].get('name', 'Unknown')
    white_id = get_or_create_player(connection, white_name)
    black_id = get_or_create_player(connection, black_name)

    game_id = generate_game_id()
    game_type = parsed_game.game.get('time_control', 'Unknown')
    result = parsed_game.game.get('result', '*')
    
    insert_game_query = """
    INSERT INTO game (game_id, site, date, white_name, white_id, black_name, black_id, result, type, white_elo, black_elo, termination, eco, endtime, link, number_of_moves, tournament_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
    """
    game_data = (
        game_id,
        parsed_game.game.get('site', 'Unknown'),
        parsed_game.tournament.get('date', '0000.00.00'),
        white_name,
        white_id,
        black_name,
        black_id,
        result,
        parse_time_control(game_type),
        parsed_game.game.get('white_elo'),
        parsed_game.game.get('black_elo'),
        parsed_game.game.get('termination', 'Normal'),
        parsed_game.game.get('eco', 'N/A'),
        parsed_game.game.get('endtime'),
        parsed_game.game.get('link'),
        len(parsed_game.moves)
    )
    cursor.execute(insert_game_query, game_data)

    insert_move_query = """
    INSERT INTO move (game_id, move_number, white_move, black_move)
    VALUES (%s, %s, %s, %s)
    """
    for move in parsed_game.moves:
        move_data = (game_id, move['move_number'], move['white_move'], move.get('black_move'))
        cursor.execute(insert_move_query, move_data)

    connection.commit()
    cursor.close()

def fetch_player_id(connection, email):
    """Fetches the player_id from the database based on email."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT player_id FROM player WHERE email = %s", (email,))
    player = cursor.fetchone()
    cursor.close()
    return player.get('player_id') if player else None

def fetch_user_name(connection, email):
    """Fetches the user's name from the database based on email."""
    cursor = connection.cursor(dictionary=True)
    query = "SELECT name FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    return user['name'] if user and user['name'] else ""

def check_profile_completion(connection, player_id):
    """Checks if a user's profile is complete."""
    cursor = connection.cursor()
    query = "SELECT is_profile_complete FROM profile_status WHERE player_id = %s"
    cursor.execute(query, (player_id,))
    status = cursor.fetchone()
    cursor.close()
    return status and status[0]

def display_home():
    """Renders the Home page of the application."""
    try:
        connection = connect_to_db()

        user_email = st.session_state.get('user_email')
        user_name = fetch_user_name(connection, user_email)
        player_id = fetch_player_id(connection, user_email)

        if user_name:
            st.title(f"Welcome to Knight's Ledger, {user_name}!")
        else:
            st.title("Welcome to Knight's Ledger!")
        
        st.markdown("#### Your Chess Database Management System")
        
        if player_id and not check_profile_completion(connection, player_id):
            st.warning("Please update your profile information by going to 'Your Profile'.")

        st.subheader("Upload Your PGN File")
        uploaded_file = st.file_uploader("Upload a PGN file", type="pgn")

        if uploaded_file is not None:
            pgn_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            st.text_area("PGN File Content", pgn_content, height=300)

            try:
                parsed_games = parse_pgn(pgn_content)
                if not parsed_games:
                    st.warning("No games found in the PGN file. Please check the file content.")
                    return

                with st.spinner('Inserting games into database...'):
                    for parsed_game in parsed_games:
                        insert_game_and_moves_to_db(connection, parsed_game)
                
                st.success(f"{len(parsed_games)} game(s) and their moves have been inserted into the database!")

            except Exception as e:
                st.error(f"Error parsing or inserting game data: {e}")

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    display_home()