import streamlit as st
import pandas as pd 
import requests


local_host = 'http://localhost:8000/'


# Create a session state object
session_state = st.session_state

def get_jwt_token(username, password):
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def login_page():
    st.markdown("<h1 style='text-align: center; '>Login Page</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2,col3,col4,col5 = st.columns(5)
        with col3:
            login_button = st.button(":blue[Login]")

    if login_button:
        token = get_jwt_token(username, password)
        if token:
            data = get_data(token)
            if data:
                return True  

        else:
            st.error("Invalid username or password.")
            return False  # Return False to indicate unsuccessful login

# Display the login page
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_success = login_page()

    if login_success:
        st.session_state['logged_in'] = True
        st.experimental_rerun()
else:
    
    st.markdown("<u><h1 style='text-align: center'>Toucan Analytics</h1><u> <br>", unsafe_allow_html=True)

def main():
    # st.title("TO DO TASK")
    menu = ["CREATE","DELETE"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Create":
        st.subheader("ADD TASK")
        title = st.text_input("Task Title")
        description = st.text_input("Description")
        created_date = st.date_input("Created Date")
        due_date = st.date_input("Due Date")
        status = st.selectbox('PENDING','COMPLETED','IN_PROGRESS')


    if status == "PENDING":
        st.button("ADD")

    if choice == "Delete":
        pass
