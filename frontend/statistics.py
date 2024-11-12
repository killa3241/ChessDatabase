import streamlit as st
import mysql.connector
import pandas as pd

def get_player_statistics(player_id):
    connection = mysql.connector.connect(
        host='localhost',
        user='chess_user',
        password='user123',
        database='chess_db'
    )
    cursor = connection.cursor(dictionary=True) 

    try:
        cursor.callproc('get_player_statistics', [player_id])
        
        for result in cursor.stored_results():
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data)
                return df
            return None
            
    except mysql.connector.Error as err:
        st.error(f"Error fetching statistics: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def display_statistics():
    st.title("Chess Player Statistics")
    st.write("Enter a player ID to view their statistics")

    player_id = st.text_input("Player ID", "")

    if st.button("Get Statistics"):
        if player_id:
            df = get_player_statistics(player_id)
            if df is not None and not df.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Player Statistics")
                    st.dataframe(
                        df,
                        column_config={
                            "player_id": "Player ID",
                            "name": "Name",
                            "total_games": "Total Games",
                            "wins": "Wins",
                            "draws": "Draws",
                            "win_rate": st.column_config.NumberColumn(
                                "Win Rate",
                                format="%.2f%%"
                            ),
                            "avg_opponent_elo": st.column_config.NumberColumn(
                                "Avg Opponent ELO",
                                format="%.0f"
                            ),
                            "highest_opponent_elo": "Highest Opponent ELO",
                            "preferred_time_control": "Preferred Time Control",
                            "favorite_white_opening": "Favorite White Opening",
                            "favorite_black_opening": "Favorite Black Opening"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                
                with col2:
                    st.subheader("Summary")
                    st.metric("Total Games", df['total_games'].iloc[0])
                    st.metric("Win Rate", f"{df['win_rate'].iloc[0]:.2f}%")
                    st.metric("Avg Opponent ELO", f"{df['avg_opponent_elo'].iloc[0]:.0f}")
                
                st.subheader("Opening Preferences")
                opening_col1, opening_col2 = st.columns(2)
                
                with opening_col1:
                    st.write("As White")
                    st.info(df['favorite_white_opening'].iloc[0] or "No data")
                
                with opening_col2:
                    st.write("As Black")
                    st.info(df['favorite_black_opening'].iloc[0] or "No data")
                
            else:
                st.warning("No statistics found for this player.")
        else:
            st.error("Please enter a Player ID.")

if __name__ == "__main__":
    display_statistics()