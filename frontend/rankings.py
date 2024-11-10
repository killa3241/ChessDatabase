import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db"
    )

def fetch_player_rankings():
    """Fetch all players and their ratings from the database, sorted by rating."""
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
    """Get the rank of the logged-in user based on their player ID."""
    for rank, player in enumerate(players, start=1):
        if player['player_id'] == player_id:
            return rank, player
    return None, None

def display_rankings():
    st.title("Player Rankings")

    # Connect to the database
    players = fetch_player_rankings()

    if not players:
        st.warning("No player data available.")
        return

    # Get logged-in user's email and player ID from session state
    user_email = st.session_state.get('user_email')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT player_id FROM player WHERE email = %s", (user_email,))
    user_info = cursor.fetchone()
    user_player_id = user_info['player_id'] if user_info else None

    cursor.close()
    connection.close()

    # Get the rank of the logged-in user
    user_rank, user_data = get_user_rank(user_player_id, players)

    # Display the logged-in user's rank at the top
    if user_rank:
        st.markdown(f"### Your Rank: **#{user_rank}**")
        st.markdown(f"**Name**: {user_data['name']}  |  **Rating**: {user_data['rating']}")
    else:
        st.markdown("### Your Rank: **Unranked**")
    
    # Prepare player rankings for display
    ranking_data = []
    for rank, player in enumerate(players, start=1):
        ranking_data.append([rank, player['name'], player['rating']])

    # Define columns for DataFrame
    columns = ["Rank", "Player Name", "Rating"]

    # Convert to DataFrame for better visualization
    df = pd.DataFrame(ranking_data, columns=columns)
    df = df.set_index("Rank")
    # Implement pagination for the rankings table
    items_per_page = 20
    total_items = len(df)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Pagination control
    page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)

    # Calculate start and end indices of the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Display the current page of rankings without row indices
    st.dataframe(df.iloc[start_index:end_index], use_container_width=True)

if __name__ == "__main__":
    display_rankings()
