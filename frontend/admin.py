import streamlit as st
import mysql.connector

# Function to connect to the database
def connect_to_db(user="chess_admin", password="Chessadmin1", database="chess_db"):
    return mysql.connector.connect(
        host="localhost", 
        user=user, 
        password=password, 
        database=database
    )

def view_table(cursor, table_name, title):
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    st.subheader(title)
    st.table(records) if records else st.info(f"No records found in {title.lower()}.")

# Delete a record by ID from a specified table
def delete_record(cursor, db, table_name, record_id, id_column):
    cursor.execute(f"SELECT * FROM {table_name} WHERE {id_column} = %s", (record_id,))
    if cursor.fetchone():
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
        db.commit()
        st.success(f"Deleted {table_name} with ID {record_id}.")
    else:
        st.warning(f"No record with ID {record_id} found in {table_name}.")

# Function to log out the admin
def logout():
    st.session_state['logged_in'] = False
    st.session_state['admin_id'] = None
    st.success("You have been logged out.")
    st.rerun()  # Refreshes the page

# Main function for the admin dashboard
def admin_dashboard():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Navigation menu
    choice = st.sidebar.selectbox("Options", ["View Players", "View Games", "View Tournaments", "Delete Data"])
    if choice == "View Players":
        view_table(cursor, "player", "Players")
    elif choice == "View Games":
        view_table(cursor, "game", "Games")
    elif choice == "View Tournaments":
        view_table(cursor, "tournament", "Tournaments")
    elif choice == "Delete Data":
        delete_choice = st.radio("Choose what to delete", ["Player", "Game", "Tournament"])
        record_id = st.text_input("Enter ID to delete")
        if st.button(f"Delete {delete_choice}"):
            table_name = delete_choice.lower()
            id_column = f"{table_name}_id"
            delete_record(cursor, db, table_name, record_id, id_column)

    # Logout button
    if st.sidebar.button("Logout"):
        logout()

    cursor.close()
    db.close()

# Run the admin dashboard if this file is the entry point
if __name__ == "__main__":
    admin_dashboard()
