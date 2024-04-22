import streamlit as st
from PIL import Image, ImageOps
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import smtplib
from email.mime.text import MIMEText
import os

from streamlit.components.v1 import html

# ----
# Helper Functions
# ----
sender_email = 'mlsandboxproject@gmail.com'
sender_password = st.secrets['email_password']
def send_email(body, to, subject):
    try:
        msg = MIMEText(body, 'html')
        msg['From'] = sender_email
        msg['To'] = to
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Error sending email: {e}")

# ----
# Page Config
# ----
st.set_page_config(
    page_title='ML SandBox!',
    page_icon='🚀',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

# ----
# Sidebar
# ----
    
    

# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "ML SandBox",
    options=['Login', 'Create Account', 'Forgot Password', 'Forgot Username'],
    icons=['box-arrow-in-right', 'person-plus', 'x-circle', 'question-square'],
    orientation="horizontal",
    menu_icon="rocket",
)

# ----
# Body
# ----
# ----
# Authenticator
# ----
with open('users.yaml') as f:
    users = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(users['credentials'],
                                     users['cookie']['name'],
                                     users['cookie']['key'],
                                     users['cookie']['expiry_days'],
                                     users['preauthorized'])

if selected == 'Login':
    name, authentication_status, username = authenticator.login()

    if st.session_state["authentication_status"]:
        # Sidebar
        with st.sidebar:
            try:
                file_name = 'profilepic_files/' + st.session_state['username'] + '_pic.png'
                st.image(file_name, use_column_width=True)
            except Exception as e:
                st.image('profilepic_files/default_avatar.jpg', use_column_width=True)  

        col1, col2 = st.columns([2, 1])
        with col1:
            st.title(f'Welcome, *:orange[{st.session_state["name"]}]*')
            st.write('##')
            st.write('Discover a world where innovation meets simplicity. At :orange[MLSandbox], we bring you a seamless blend of cutting-edge technology and user-friendly tools to empower your journey in data science and machine learning. Our platform is designed to help you learn, experiment, and collaborate with like-minded individuals. We are committed to providing you with the best resources to help you grow and succeed in your career.')
            st.write('#')
            st.write('Our team consist of 5 members: *:orange[Devin Setiawan]*, *:orange[Tristan Tjandra]*, *:orange[Cody Doze]*, *:orange[Hubert Maximus]*, and *:orange[Nicholas Dang]*. We are all currently studying at the *:orange[University of Kansas]* in Lawrence, Kansas. We are all in our senior year and we are all majoring in *:orange[Computer Science]*. This project is our final project for our *:orange[EECS581/582: Senior Capstone Project]* class.')
        with col2:
            # image first.png
            st.image('first.png')
        with st.expander('Edit Profile'):
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.update_user_details(st.session_state["username"]):
                        st.success('Entries updated successfully')
                        with open('users.yaml', 'w') as file:
                            yaml.dump(users, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
        with st.expander('Change Password'):
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.reset_password(st.session_state["username"]):
                        st.success('Password modified successfully')
                        with open('users.yaml', 'w') as file:
                            yaml.dump(users, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
        with st.expander('Edit Profile Picture'):
            if st.session_state["authentication_status"]:
                if 'profile_updated' not in st.session_state:
                    st.session_state['profile_updated'] = False
                profile_pic = st.file_uploader('Upload a new profile picture', type=['png', 'jpg', 'jpeg'], key='profile_picture')
                if profile_pic and not st.session_state['profile_updated']:
                    # convert to png using PIL
                    image = Image.open(st.session_state['profile_picture'])
                    # convert to 200x200
                    image = image.resize((200, 200))
                    image.save(file_name)
                    st.success('Profile picture updated successfully, refresh the page to see the changes')
                if st.button('Reset Profile Picture'):
                    try:
                        os.remove(file_name)
                        st.success('Profile picture reset successfully, refresh the page to see the changes')
                    except Exception as e:
                        st.error('Profile picture is already default')


        authenticator.logout('Logout', 'main')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

elif selected == 'Create Account':
    if st.session_state["authentication_status"]:
        # Sidebar
        with st.sidebar:
            try:
                file_name = 'profilepic_files/' + st.session_state['username'] + '_pic.png'
                st.image(file_name, use_column_width=True)
            except Exception as e:
                st.image('profilepic_files/default_avatar.jpg', use_column_width=True) 
    try:
        if authenticator.register_user(preauthorization=False):
            st.success('User registered successfully')
            with open('users.yaml', 'w') as file:
                yaml.dump(users, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

elif selected == 'Forgot Password':
    if st.session_state["authentication_status"]:
        # Sidebar
        with st.sidebar:
            try:
                file_name = 'profilepic_files/' + st.session_state['username'] + '_pic.png'
                st.image(file_name, use_column_width=True)
            except Exception as e:
                st.image('profilepic_files/default_avatar.jpg', use_column_width=True) 
    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
        if username_of_forgotten_password:
            st.success('New password to be sent securely')
            with open('users.yaml', 'w') as file:
                yaml.dump(users, file, default_flow_style=False)
            # Random password should be transferred to the user securely
            body = f'''
Hello, {st.session_state["name"]}! <br><br>
You have requested to reset your password. Your new password is: <br><br><b><p style="color:orange;">{new_random_password}</p></b> <br><br>
Please login with your new password and change it to something more personal. <br>
<br>
Best regards, <br>
MLSandbox Team
        '''
            send_email(body, email_of_forgotten_password, 'MLSandbox ~ Forgot Password')
        elif username_of_forgotten_password is not None:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

elif selected == 'Forgot Username':
    if st.session_state["authentication_status"]:
        # Sidebar
        with st.sidebar:
            try:
                file_name = 'profilepic_files/' + st.session_state['username'] + '_pic.png'
                st.image(file_name, use_column_width=True)
            except Exception as e:
                st.image('profilepic_files/default_avatar.jpg', use_column_width=True) 
    try:
        username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username()
        if username_of_forgotten_username:
            st.success('Username to be sent securely')
            # Username should be transferred to the user securely
            body = f'''
Hello, {st.session_state["name"]}! <br><br>
You have requested your username. Your username is: <br><br><b><p style="color:orange;">{username_of_forgotten_username}</p></b> <br><br>
Please login with your username to be able to access the community. <br>
<br>
Best regards, <br>
MLSandbox Team
        '''
            send_email(body, email_of_forgotten_username, 'MLSandbox ~ Forgot Username')
        elif username_of_forgotten_username is not None:
            st.error('Email not found')
    except Exception as e:
        st.error(e)


on = st.toggle('Experimental Features')
if on:
    text_input = st.text_input(' ')
    if text_input == 'balloons' or text_input == 'balloon':
        st.balloons()
    if text_input == 'snow':
        st.snow()
    if text_input == 'iwannaplaygame':
        html_str = "<iframe src=\"https://solitaires-online.com/tic-tac-toe/#id=416pwfdn3s,no-nav,no-article,no-feedback,no-ads\" title=\"Tic-Tac-Toe game\" width=\"280\" height=\"280\"></iframe>"
        with st.sidebar:
            html(html_str, width=280, height=280)


 



