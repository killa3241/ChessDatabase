import streamlit as st
import pandas as pd
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db"
    )

def fetch_player_rankings():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT player_id, name, rating
    FROM player
    WHERE rating IS NOT NULL
    ORDER BY rating DESC
    """
    cursor.execute(query)
    players = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return players

def get_user_rank(player_id, players):
    for rank, player in enumerate(players, start=1):
        if player['player_id'] == player_id:
            return rank, player
    return None, None

def display_rankings():
    st.title("Player Rankings")

    players = fetch_player_rankings()

    if not players:
        st.warning("No player data available.")
        return

    user_email = st.session_state.get('user_email') #logged-in user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT player_id FROM player WHERE email = %s", (user_email,))
    user_info = cursor.fetchone()
    user_player_id = user_info['player_id'] if user_info else None

    cursor.close()
    connection.close()

    user_rank, user_data = get_user_rank(user_player_id, players)

    if user_rank:
        st.markdown(f"### Your Rank: **#{user_rank}**")
        st.markdown(f"**Name**: {user_data['name']}  |  **Rating**: {user_data['rating']}")
    else:
        st.markdown("### Your Rank: **Unranked**")
    
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
