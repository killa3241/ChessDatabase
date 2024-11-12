import streamlit as st
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="chess_user",
        password="user123",
        database="chess_db"
    )

def get_user_info(cursor, email):
    query = "SELECT name, country, rating, online_profile, date_of_birth, gender FROM player WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()

def update_user_info(cursor, db, email, name, country, rating, online_profile, date_of_birth, gender):
    query = """
    UPDATE player
    SET name = %s, country = %s, rating = %s, online_profile = %s, date_of_birth = %s, gender = %s
    WHERE email = %s
    """
    cursor.execute(query, (name, country, rating, online_profile, date_of_birth, gender, email))
    db.commit()

def display_profile():
    st.title("Your Profile")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Please log in to access your profile.")
        st.stop()

    email = st.session_state['user_email']
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    user_info = get_user_info(cursor, email)
    
    if user_info:
        st.subheader("Current Information")
        st.text(f"Name: {user_info['name'] if user_info['name'] else 'Not set'}")
        st.text(f"Country: {user_info['country'] if user_info['country'] else 'Not set'}")
        st.text(f"Rating: {user_info['rating'] if user_info['rating'] else 'Not set'}")
        st.text(f"Online Profile: {user_info['online_profile'] if user_info['online_profile'] else 'Not set'}")
        st.text(f"Date of Birth: {user_info['date_of_birth'] if user_info['date_of_birth'] else 'Not set'}")
        st.text(f"Gender: {user_info['gender'] if user_info['gender'] else 'Not set'}")

        st.subheader("Update Your Information")
        name = st.text_input("Name", user_info['name'])
        country = st.text_input("Country", user_info['country'])
        rating = st.number_input("Rating", value=user_info['rating'] if user_info['rating'] else 0, min_value=0)
        online_profile = st.text_input("Online Profile", user_info['online_profile'])
        date_of_birth = st.date_input("Date of Birth", user_info['date_of_birth'] if user_info['date_of_birth'] else None)
        gender = st.selectbox("Gender", ['Male', 'Female', 'Other'], index=['Male', 'Female', 'Other'].index(user_info['gender']) if user_info['gender'] else 0)

        if st.button("Update Information"):
            update_user_info(cursor, db, email, name, country, rating, online_profile, date_of_birth, gender)
            st.success("Your information has been updated!")
            
            if name:
                st.session_state['user_name'] = name

    else:
        st.error("Failed to load user information.")

    cursor.close()
    db.close()

if __name__ == "__main__":
    display_profile()
