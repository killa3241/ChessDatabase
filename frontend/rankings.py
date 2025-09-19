# File: frontend/rankings.py

import streamlit as st
import pandas as pd
import mysql.connector
from db_utils import connect_to_db

def fetch_player_rankings():
    """Fetches all players with a rating, ordered by rating."""
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT player_id, name, rating
        FROM player
        WHERE rating IS NOT NULL
        ORDER BY rating DESC
        """
        cursor.execute(query)
        players = cursor.fetchall()
        
        return players
    except mysql.connector.Error as err:
        st.error(f"Error fetching player rankings: {err}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_user_rank(player_id, players):
    """Finds the rank and data for a specific player."""
    for rank, player in enumerate(players, start=1):
        if player['player_id'] == player_id:
            return rank, player
    return None, None

def display_rankings():
    st.title("Player Rankings")
    
    players = fetch_player_rankings()

    if not players:
        st.warning("No player data available. Rankings cannot be displayed.")
        return

    user_email = st.session_state.get('user_email')
    
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT player_id FROM player WHERE email = %s", (user_email,))
        user_info = cursor.fetchone()
        user_player_id = user_info['player_id'] if user_info else None
    
        user_rank, user_data = get_user_rank(user_player_id, players)

        st.subheader("Your Rank")
        if user_rank:
            st.markdown(f"**Rank**: #{user_rank} | **Name**: {user_data['name']} | **Rating**: {user_data['rating']}")
        else:
            st.markdown("You are currently **Unranked**. Please ensure your profile rating is set.")
    except mysql.connector.Error as err:
        st.error(f"Error retrieving your rank: {err}")
        return
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    st.subheader("All Player Rankings")
    ranking_data = []
    for rank, player in enumerate(players, start=1):
        ranking_data.append([rank, player['name'], player['rating']])

    columns = ["Rank", "Player Name", "Rating"]

    df = pd.DataFrame(ranking_data, columns=columns)
    df = df.set_index("Rank")
    items_per_page = 20
    total_items = len(df)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    st.dataframe(df.iloc[start_index:end_index], use_container_width=True)

if __name__ == "__main__":
    display_rankings()