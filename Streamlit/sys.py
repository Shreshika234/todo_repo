import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu

local_host = 'http://localhost:8000/'


# Create a session state object
session_state = st.session_state

st.set_page_config(layout="wide")
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

    selected = option_menu(
        menu_title= "TO DO ",
        options = ["Tasks_todo", "History"],
        orientation = "horizontal"
    )
    if selected == "History":
        
        response = requests.get("http://127.0.0.1:8000/post/")
        if response.status_code==200:
            df=response.json()
            data=pd.DataFrame(df)
            # k = k.iloc[:, 1:] 
            st.write(data)

            
        id = st.selectbox("Select ID to delete", [1, 2, 3, 4, 5])
        if st.button("DELETE"):
            
            response = requests.delete("http://127.0.0.1:8000/items/<int:id>/")
            if response.status_code == 200:
                    st.success("Task deleted successfully")
            else:
                    st.error("Failed to delete the task. Please try again.")

    if selected == "Tasks_todo":
        st.subheader("ADD TASK")
        title = st.text_input("Task Title")
        description = st.text_input("Description")
        status = st.selectbox('Status', ['PENDING', 'COMPLETED', 'IN_PROGRESS'])

        if st.button("ADD"):
                # Create a dictionary to hold the task data
                task_data = {
                    "title": title,
                    "description": description,
                    "status": status
                }

                response = requests.post("http://127.0.0.1:8000/post/", json=task_data)

                # Check the response status code
                if response.status_code == 200:
                    st.success("Task submitted successfully!")
                else:
                    st.error("Failed to submit the task. Please try again.")

                if status == "COMPLETED":
                        uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "xlsx","pdf"])
                        if uploaded_file is not None:
                            df = pd.read_csv(uploaded_file)
                            st.dataframe(df)
                            if response.status_code == 200:
                                st.success("Task submitted successfully!")

        
