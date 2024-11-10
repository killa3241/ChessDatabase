import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db"
    )

def fetch_all_games():
    """Fetches all games from the database with detailed information."""
    connection = get_db_connection()
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
    
    cursor.close()
    connection.close()
    return games

def display_games():
    st.title("All Chess Games")
    st.markdown("### Explore all games stored in the database")

    # Fetch all games
    games = fetch_all_games()
    
    if games:
        st.write(f"Total games found: {len(games)}")
        
        # Display game details in a table format
        game_data = []
        for index, game in enumerate(games, start=1):
            game_data.append([
                index,
                game['game_id'],
                game['date'],
                game['player1'],
                game['white_elo'],
                game['player2'],
                game['black_elo'],
                game['result'],
                game['type'],
                game['number_of_moves'],
                game['termination'],
                game['tournament_name'] if game['tournament_name'] else "N/A"
            ])
        
        # Define columns for better readability
        columns = [
            "Index", "Game ID", "Date", "Player 1 (White)", "White ELO", 
            "Player 2 (Black)", "Black ELO", "Result", "Type", 
            "Total Moves", "Termination", "Tournament"
        ]
        
        df = pd.DataFrame(game_data, columns=columns)
        df = df.set_index("Index")
        # Implement pagination
        items_per_page = 20
        total_items = len(df)
        total_pages = (total_items + items_per_page - 1) // items_per_page

        # Create a pagination control
        page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)

        # Calculate start and end indices of the current page
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        # Display the current page of data
        st.dataframe(df.iloc[start_index:end_index], use_container_width=True)
    else:
        st.warning("No games found in the database. Please add some games to view them here.")

# Main function to run when this file is executed
if __name__ == "__main__":
    display_games()
