import streamlit as st
import requests
from streamlit_option_menu import option_menu



st.set_page_config(layout="wide",initial_sidebar_state="expanded",)

local_host = 'http://192.168.70.4:8008/'

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
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/premium-photo/empty-white-wall-background-with-sunlight-shadow_386045-98.jpg?w=2000");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
    unsafe_allow_html=True
     )
    
    st.markdown("<h1 style='text-align: center; '><u>LOGIN</h1></u><br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("**:blue[Username]**")
        password = st.text_input("**:blue[Password]**", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("**:blue[Login]**")

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
                 st.write("You cannot access next page")

        else:
            st.error("Invalid username or password.")
            
    

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/114979/pexels-photo-114979.jpeg?cs=srgb&dl=pexels-veeterzy-114979.jpg&fm=jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
    unsafe_allow_html=True
     )

    token = st.session_state['token']  
    UserName = st.session_state['username']


    st.markdown("<h1 style='text-align: center; color: red'>To-Do List</h1>", unsafe_allow_html=True)

    col1,col2 = st.columns([8,2])
    with col1:
        selected = option_menu(
            menu_title = "",
            options = ["TASK","HISTORY",],
            icons = ["card-checklist","journal-text"],
            menu_icon = "cast",
            default_index = 1,
            orientation = "horizontal",
        )
    
        if selected == "TASK":
            
            a,b = st.columns([3,7])
            with a:
                with st.form(key="form",clear_on_submit=True):             
                    task = st.text_input(":pencil:**TASK**",key='task')
                    add = st.form_submit_button("**:red[ADD]**")    
                
            with b:
                if task:
                    if add:
                        st.session_state['session_state'] = {'task': ''}
                        url = local_host + "todo/?type=create"
                        headers = {'Authorization': f'Bearer {token}'}
                        params={
                            "userName":UserName,
                            "task":task,
                            "description":"",
                            "status":"Pending",
                        }        
                        response = requests.get(url,headers=headers,params=params)
                        if response.status_code == 200: 
                            pass
                        else:
                            st.error("You don't have permission to create the task")
                        
                params={
                            "userName":UserName,
                        }     
                
                url = local_host + "todo/?type=read"
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url,headers=headers,params=params)
                if response.status_code == 200:
                    data = response.json()
                    task = data['task']  
                    for i in range(len(task)):
                        # st.radio(task[i], task, index=i, key=task[i])
                        tasks = st.checkbox(task[i],key=task[i])
                        if tasks:
                            with st.container():
                                with st.form(key="forms",clear_on_submit=True):
                                    description = st.text_area("**Description**")
                                    file = st.file_uploader("**Please Choose a File**")
                                    submit = st.form_submit_button("**SUBMIT**")
                                    if description:
                                        if submit :
                                                url = local_host + "todo/?type=uploadfile"
                                                headers = {'Authorization': f'Bearer {token}'}
                                                params = {
                                                    "userName":UserName,
                                                    "description":description,
                                                    "status":"Completed",
                                                    "task":task[i],
                                                }
                                                files = {
                                                    'file': file
                                                }
                                                st.success("Submited Successfully")
                                                response = requests.post(url,headers=headers,params=params,files=files)
                                                if response.status_code == 200:
                                                    pass
                                                else:
                                                    st.error("ERROR")     
                else:
                    st.error(f'Error: {response.status_code}')
                    
                              
        if selected == "HISTORY":
            params={
                    "userName":UserName,
                }     
            
            url = local_host + "todo/?type=history"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            
                        
            if response.status_code == 200:
                data = response.json()
                tasks = data['tasks']
                files = data['files']
                description = data['description']
                p,q = st.columns(2)
                with p: 
                    st.header("COMPLETED TASKS")
                with q:
                    st.header("TASK DETAILS")

                for i in range(len(tasks)):
                  
                    with p:                      
                        details = st.button(f'{i+1} . {tasks[i]}')
                    # Apply CSS styles to hide the button structure
                    with q:                      
                        button_style = """
                            <style>
                            .stButton>button {
                                background: none;
                                border: none;
                                padding: 0;
                                margin: 0;
                                font-size: inherit;
                                font-family: inherit;
                                cursor: pointer;
                                outline: inherit;
                            }
                            </style>
                        """
                        st.markdown(button_style, unsafe_allow_html=True)
                        if details:
                            st.write("Description:", description[i])                        
                            st.write("click the link to download the file:", files[i])         
            else:
                st.error("Failed to fetch data from the backend")

                       
    with col2:
        a,b = st.columns([4,6])
        with b:
            image ="data:image/jpeg;base64,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"
            st.image(image, caption=UserName, width=200)
        
               
