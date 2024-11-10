import streamlit as st
import mysql.connector
from io import StringIO
from pathlib import Path
import sys
import uuid
import re

def parse_time_control(time_control_str):
    if time_control_str == "?":
        return "Unknown"
    elif time_control_str == "-":
        return "No Time Control"
    
    # Periodic moves/seconds: "40/9000"
    if re.match(r'^\d+/\d+$', time_control_str):
        moves, seconds = time_control_str.split('/')
        if seconds == "86400":
            return f"Daily: {moves} moves per day"
        elif int(seconds) >= 86400:  # if seconds >= 1 day
            days = int(seconds) // 86400
            return f"Daily: {moves} moves every {days} days"
        else:
            return f"Moves/Seconds: {moves} moves in {seconds} sec"
    
    # Sudden death format: "60" or "180" etc.
    if re.match(r'^\d+$', time_control_str):
        seconds = int(time_control_str)
        if seconds <= 120:
            return f"Bullet: {seconds} sec"
        elif 180 <= seconds <= 300:
            return f"Blitz: {seconds // 60} min"
        elif 600 <= seconds <= 1800:
            return f"Rapid: {seconds // 60} min"
        elif seconds > 1800:
            return f"Classical: {seconds // 60} min"
        else:
            return f"Sudden Death: {seconds} sec"
    if re.match(r'^\d+\+\d+$', time_control_str):
        initial, increment = time_control_str.split('+')
        initial = int(initial)
        increment = int(increment)
        if initial <= 120:
            return f"Bullet: {initial} sec + {increment} sec/move"
        elif initial <= 300:
            return f"Blitz: {initial // 60} min + {increment} sec/move"
        elif initial <= 1800:
            return f"Rapid: {initial // 60} min + {increment} sec/move"
        else:
            return f"Classical: {initial // 60} min + {increment} sec/move"
    if re.match(r'^\*\d+$', time_control_str):
        seconds = time_control_str[1:]
        return f"Sandclock: {seconds} sec"
    
    return "Unknown Format"

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
    player_id = uuid.uuid4().hex[:15].upper()  # Generates a 15-character alphanumeric ID
    insert_player_query = "INSERT INTO player (player_id, name) VALUES (%s, %s)"
    cursor.execute(insert_player_query, (player_id, player_name))
    connection.commit()
    
    return player_id

def generate_game_id():
    return uuid.uuid4().hex[:8].upper()  # Take the first 8 characters of the UUID and convert to uppercase

def insert_game_and_moves_to_db(connection, parsed_game):
    cursor = connection.cursor()

    # Get or create player IDs for white and black players
    white_id = get_or_create_player(connection, parsed_game.players['white'].get('name', 'Unknown'))
    black_id = get_or_create_player(connection, parsed_game.players['black'].get('name', 'Unknown'))

    # Map the time control to ENUM values or default to 'Classical'
    game_type = parsed_game.game.get('time_control')
    white_elo = parsed_game.game.get('white_elo') if parsed_game.game.get('white_elo') else None
    black_elo = parsed_game.game.get('black_elo') if parsed_game.game.get('black_elo') else None
    # Generate a unique alphanumeric game_id
    game_id = generate_game_id()

    # Insert the game record into the `game` table
    insert_game_query = """
    INSERT INTO game (game_id, site, date, white_name, white_id, black_name, black_id, result, type, white_elo, black_elo, termination, eco, endtime, link, number_of_moves, tournament_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
    """
    game_data = (
        game_id,
        parsed_game.game.get('site', 'Unknown'),
        parsed_game.tournament.get('date', '0000.00.00'),
        parsed_game.players['white'].get('name', 'Unknown'),
        white_id,
        parsed_game.players['black'].get('name', 'Unknown'),
        black_id,
        parsed_game.game.get('result', '*'),
        parse_time_control(game_type),
        white_elo,
        black_elo,
        parsed_game.game.get('termination', 'Unknown'),
        parsed_game.game.get('eco', 'N/A'),
        parsed_game.game.get('endtime'),
        parsed_game.game.get('link'),
        len(parsed_game.moves)
    )
    cursor.execute(insert_game_query, game_data)

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

def fetch_player_id(connection, email):
    """Fetches the player's ID based on email."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT player_id FROM player WHERE email = %s", (email,))
    player = cursor.fetchone()
    cursor.close()
    return player.get('player_id') if player else None

def fetch_user_name(connection, email):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT name FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    return user['name'] if user and user['name'] else ""

def check_profile_completion(connection, player_id):
    """Checks if the user's profile is complete using the profile_status table."""
    cursor = connection.cursor()
    query = "SELECT is_profile_complete FROM profile_status WHERE player_id = %s"
    cursor.execute(query, (player_id,))
    status = cursor.fetchone()
    cursor.close()
    return status and status[0]

def display_home():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db"
    )

    # Get the logged-in user's email from session state
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
        # Convert the uploaded file to a string-based IO
        pgn_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        # st.text_area("PGN File Content", pgn_content, height=300)

        # Parse the PGN content
        parsed_games = parse_pgn(pgn_content)
        st.success("PGN file parsed successfully!")

        # Insert parsed games and moves into the database
        for parsed_game in parsed_games:
            insert_game_and_moves_to_db(connection, parsed_game)

        st.success("Game data and moves have been inserted into the database!")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    display_home()
