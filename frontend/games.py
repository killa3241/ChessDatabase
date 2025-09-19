# File: frontend/games.py

import streamlit as st
import mysql.connector
import pandas as pd
from db_utils import connect_to_db

def fetch_all_games():
    """Fetches all game data from the database."""
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            g.game_id,
            g.date,
            g.white_name AS player1,
            p1.rating AS white_elo,
            g.black_name AS player2,
            p2.rating AS black_elo,
            g.result,
            g.type,
            g.number_of_moves,
            g.termination,
            t.name AS tournament_name
        FROM game g
        LEFT JOIN player p1 ON g.white_id = p1.player_id
        LEFT JOIN player p2 ON g.black_id = p2.player_id
        LEFT JOIN tournament t ON g.tournament_id = t.tournament_id
        ORDER BY g.date DESC, g.game_id
        """
        
        cursor.execute(query)
        games = cursor.fetchall()
        
        return games
    except mysql.connector.Error as err:
        st.error(f"Error fetching games: {err}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def display_games():
    """Renders the Games page with a table of all games."""
    st.title("All Chess Games")
    st.markdown("### Explore all games stored in the database")

    games = fetch_all_games()
    
    if games:
        st.write(f"Total games found: {len(games)}")
        
        df = pd.DataFrame(games)
        df.rename(columns={
            'game_id': 'Game ID',
            'date': 'Date',
            'player1': 'White Player',
            'white_elo': 'White ELO',
            'player2': 'Black Player',
            'black_elo': 'Black ELO',
            'result': 'Result',
            'type': 'Type',
            'number_of_moves': 'Moves',
            'termination': 'Termination',
            'tournament_name': 'Tournament'
        }, inplace=True)
        
        df = df.fillna('N/A')
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No games found in the database. Please add some games to view them here.")

if __name__ == "__main__":
    display_games()