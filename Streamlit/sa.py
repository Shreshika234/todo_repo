import json
import streamlit as st
import requests
import datetime
import os
from datetime import datetime
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_modal import Modal



st.set_page_config(layout="wide",initial_sidebar_state="expanded",)

local_host = 'http://localhost:8000/'

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
        return token
    else:
        return None

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    
    st.markdown("<h1 style='text-align: center; '>LOGIN</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")
            
    

if 'logged_in' in st.session_state and st.session_state['logged_in']:

    token = st.session_state['token']  
    UserName = st.session_state['username']
    st.markdown("<u><h1 style='text-align: center'>To-Do List</h1><u> <br>", unsafe_allow_html=True)

    selected = option_menu(
        menu_title= "TO DO ",
        options = ["Tasks_todo","Pending" ,"History"],
        orientation = "horizontal"
    )
    # if selected == "Pending":
    #     response = requests.get("http://127.0.0.1:8000/post/")
    #     if response.status_code==200:
    #         df=response.json()
    #         filtered_data = [obj for obj in df if obj["status"] in ["PENDING", "IN_PROGRESS"] and obj["username"] == UserName]
    #         df = pd.DataFrame(filtered_data)
    #         st.write(df)
#         import requests
# import streamlit as st

    if selected == "Pending":
        response = requests.get("http://127.0.0.1:8000/post/")
        
        if response.status_code == 200:
       
            data = response.json()
            filtered_data = [obj for obj in data if obj["status"] in ["PENDING", "IN_PROGRESS"] and obj["username"] == UserName]
            
            title_options = [obj["title"] for obj in filtered_data]
            selected_title = st.radio("Pending and In_progress tasks", title_options)
           
            filtered_data = [obj for obj in filtered_data if obj["title"] == selected_title]
            
            
            for obj in filtered_data:
                obj["status"] = "COMPLETED"
                obj["description"] = st.text_area("Enter description", "")
                if st.button("Save"):
                    # updated_data = json.dumps(filtered_data)
              
                    update_response = requests.post("http://127.0.0.1:8000/post/", json=filtered_data)
                    if response.status_code == 200:
                        st.write(filtered_data)
                        st.write(update_response)
                        
                        
                        st.success("Task submitted successfully!")

                        if obj["status"] == "COMPLETED":
                            uploaded_file = st.file_uploader("Upload a file")
                            if uploaded_file is not None:
                                file_name = uploaded_file.name
                                save_directory = "/home/shreshika/todo_list/todo_project/taskfiles"  
                                save_path = os.path.join(save_directory, file_name)
                                with open(save_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                    st.success("File saved successfully!")

                                # Redirect to another page with description text field
                                st.write("")  # Add some spacing
                                st.header("Description")
                                description = st.text_area("Enter description", "")

                                # Do something with the description (e.g., save it to a database)
                                if st.button("Save Description"):
                                    # Perform the save operation here
                                    st.success("Description saved successfully!")  
                    else:
                        st.error("Failed to submit the task. Please try again.")
                    

    if selected == "History":

        response = requests.get("http://127.0.0.1:8000/post/")
        if response.status_code==200:
            df=response.json()
            filtered_data = [obj for obj in df if obj["status"] == "COMPLETED" and obj["username"]==UserName]
            df = pd.DataFrame(filtered_data)
            st.write(df)

    if selected == "Tasks_todo":
        st.subheader("ADD TASK")
        username = st.text_input("User Name",value=UserName)
        title = st.text_input("Task Title")
        # description = st.text_input("Description")
        status = st.selectbox('Status', ['PENDING', 'COMPLETED', 'IN_PROGRESS'])

        # if status == "COMPLETED":
        #     uploaded_file = st.file_uploader("Upload a file")
        #     if uploaded_file is not None:
        #         file_name = uploaded_file.name
        #         save_directory = "/home/shreshika/todo_list/todo_project/taskfiles"  
        #         save_path = os.path.join(save_directory, file_name)
        #         with open(save_path, "wb") as f:
        #             f.write(uploaded_file.getbuffer())
        #             st.success("File saved successfully!")

        #         # Redirect to another page with description text field
        #         st.write("")  # Add some spacing
        #         st.header("Description")
        #         description = st.text_area("Enter description", "")

        #         # Do something with the description (e.g., save it to a database)
        #         if st.button("Save Description"):
        #             # Perform the save operation here
        #             st.success("Description saved successfully!")


        if status in ["PENDING", "IN_PROGRESS"]:
            st.write("")  # Add some spacing
            description = st.text_area("Description", value="Description cannot be added", key="description", disabled=True)
            st.info("Description cannot be edited for PENDING or IN_PROGRESS tasks.")


           
        if st.button("ADD"):
               
            task_data = {
                "username":username,
                "title": title,
                "description": description,
                "status": status
            }
            response = requests.post("http://127.0.0.1:8000/post/", json=task_data)
            if response.status_code == 200:
                st.success("Task submitted successfully!")
            else:
                st.error("Failed to submit the task. Please try again.")

               
