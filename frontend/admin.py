import streamlit as st
import mysql.connector

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="chess_admin",
        password="Chessadmin1",
        database="chess_db"
    )

# Function to view all players
def view_players(cursor):
    cursor.execute("SELECT * FROM player")
    players = cursor.fetchall()
    st.subheader("Players")
    if players:
        st.table(players)
    else:
        st.info("No players found in the database.")

# Function to view all games
def view_games(cursor):
    cursor.execute("SELECT * FROM game")
    games = cursor.fetchall()
    st.subheader("Games")
    if games:
        st.table(games)
    else:
        st.info("No games found in the database.")

# Function to view all tournaments
def view_tournaments(cursor):
    cursor.execute("SELECT * FROM tournament")
    tournaments = cursor.fetchall()
    st.subheader("Tournaments")
    if tournaments:
        st.table(tournaments)
    else:
        st.info("No tournaments found in the database.")

# Function to delete a player by ID
def delete_player(cursor, db, player_id):
    cursor.execute("SELECT * FROM player WHERE player_id = %s", (player_id,))
    player = cursor.fetchone()
    if player:
        cursor.execute("DELETE FROM player WHERE player_id = %s", (player_id,))
        db.commit()
        st.success(f"Player with ID {player_id} deleted.")
    else:
        st.warning(f"Player with ID {player_id} does not exist.")

# Function to delete a game by ID
def delete_game(cursor, db, game_id):
    cursor.execute("SELECT * FROM game WHERE game_id = %s", (game_id,))
    game = cursor.fetchone()
    if game:
        cursor.execute("DELETE FROM game WHERE game_id = %s", (game_id,))
        db.commit()
        st.success(f"Game with ID {game_id} deleted.")
    else:
        st.warning(f"Game with ID {game_id} does not exist.")

# Function to delete a tournament by ID
def delete_tournament(cursor, db, tournament_id):
    cursor.execute("SELECT * FROM tournament WHERE tournament_id = %s", (tournament_id,))
    tournament = cursor.fetchone()
    if tournament:
        cursor.execute("DELETE FROM tournament WHERE tournament_id = %s", (tournament_id,))
        db.commit()
        st.success(f"Tournament with ID {tournament_id} deleted.")
    else:
        st.warning(f"Tournament with ID {tournament_id} does not exist.")

# Function to log out the admin
def logout():
    st.session_state['logged_in'] = False
    st.session_state['admin_id'] = None
    st.success("You have been logged out.")
    st.rerun()  # Refreshes the page

# Main function for the admin dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    # Logout button
    if st.button("Logout"):
        logout()

    # Connect to the database
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Create a navigation bar
    choice = st.sidebar.selectbox("Navigate", ["View Players", "View Games", "View Tournaments", "Delete Data"])

    if choice == "View Players":
        view_players(cursor)

    elif choice == "View Games":
        view_games(cursor)

    elif choice == "View Tournaments":
        view_tournaments(cursor)

    elif choice == "Delete Data":
        delete_choice = st.radio("Choose what to delete", ["Player", "Game", "Tournament"])

        if delete_choice == "Player":
            player_id = st.number_input("Enter Player ID to delete", min_value=1)
            if st.button("Delete Player"):
                delete_player(cursor, db, player_id)

        elif delete_choice == "Game":
            game_id = st.number_input("Enter Game ID to delete", min_value=1)
            if st.button("Delete Game"):
                delete_game(cursor, db, game_id)

        elif delete_choice == "Tournament":
            tournament_id = st.number_input("Enter Tournament ID to delete", min_value=1)
            if st.button("Delete Tournament"):
                delete_tournament(cursor, db, tournament_id)

    # Close the database connection
    cursor.close()
    db.close()

# Run the admin dashboard if this file is the entry point
if __name__ == "__main__":
    admin_dashboard()
