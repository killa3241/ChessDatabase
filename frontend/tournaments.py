import streamlit as st
import mysql.connector
import uuid
import pandas as pd
def generate_tournament_id():
    """Generates a random 6-character uppercase tournament ID"""
    return uuid.uuid4().hex[:6].upper()

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db" 
    )
    return connection

def insert_tournament(name, date, duration, location, type, organizer):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    tournament_id = generate_tournament_id()
    query = """
    INSERT INTO tournament (tournament_id, name, date, duration, location, type, organizer)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (tournament_id, name, date, duration, location, type, organizer))
    
    connection.commit()
    cursor.close()
    connection.close()

def update_game_tournament_id(game_id, tournament_id):
    """Updates the tournament_id in the game table based on the game_id"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
    UPDATE game SET tournament_id = %s WHERE game_id = %s
    """
    cursor.execute(query, (tournament_id, game_id))
    
    connection.commit()
    cursor.close()
    connection.close()

def display_tournaments():
    st.title("Tournaments")
    st.write("""Here you can add tournaments.""")
    st.write("""Also you can find information about tournaments.""")

    st.subheader("Add a New Tournament")
    with st.form("tournament_form"):
        name = st.text_input("Tournament Name")
        date = st.date_input("Date")
        duration = st.number_input("Duration (in days)", min_value=1, step=1)
        location = st.text_input("Location")
        type = st.selectbox("Tournament Type", ['Round Robin', 'Knock Out', 'Swiss System', 'Scheveningen System'])
        organizer = st.text_input("Organizer", value="Unknown")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            try:
                insert_tournament(name, date, duration, location, type, organizer)
                st.success(f"Tournament '{name}' added successfully!")
            except Exception as e:
                st.error("Error adding tournament to database.")
                st.write(e)

    st.subheader("Add a Game to a Tournament")
    with st.form("game_form"):
        game_id = st.text_input("Game ID")
        tournament_name = st.text_input("Tournament Name (for matching games)")
        
        submitted_game = st.form_submit_button("Assign Game to Tournament")
        
        if submitted_game:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT tournament_id FROM tournament WHERE name = %s", (tournament_name,))
            tournament = cursor.fetchone()
            
            if tournament:
                tournament_id = tournament[0]
                try:
                    update_game_tournament_id(game_id, tournament_id)
                    st.success(f"Game {game_id} has been assigned to tournament '{tournament_name}'")
                except Exception as e:
                    st.error("Error updating game with tournament ID.")
                    st.write(e)
            else:
                st.error("Tournament not found.")
            cursor.close()
            connection.close()

    st.subheader("Display Games for a Tournament")
    tournament_name_to_display = st.text_input("Enter Tournament Name to Display Games")
    
    if st.button("Display Games"):
        if tournament_name_to_display:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("""
            SELECT g.game_id, g.white_name, g.black_name, g.result
            FROM game g
            JOIN tournament t ON g.tournament_id = t.tournament_id
            WHERE t.name = %s
            """, (tournament_name_to_display,))
            games = cursor.fetchall()
            
            if games:
                st.write("### Games in Tournament:", tournament_name_to_display)
                for game in games:
                    st.write(f"**Game ID:** {game['game_id']}, **White:** {game['white_name']}, **Black:** {game['black_name']}, **Result:** {game['result']}")
            else:
                st.write("No games found for this tournament.")
            cursor.close()
            connection.close()
    st.subheader("All Tournaments")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT tournament_id, name, date, duration, location, type, organizer FROM tournament")
    tournaments = cursor.fetchall()
    
    if tournaments:
            df = pd.DataFrame(tournaments)
            
            df.index = df.index + 1
            df.index.name = 'Index'
            
            st.dataframe(df, use_container_width=True)
        
    else:
        st.write("No tournaments found.")
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    display_tournaments()