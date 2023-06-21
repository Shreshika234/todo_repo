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

                       
    # with col2:
    #     a,b = st.columns([4,6])
    #     with b:
    #         image = "/home/shreshika/Downloads/dp.jpg"
    #         st.image(image, caption=UserName, width=200)
        
               
