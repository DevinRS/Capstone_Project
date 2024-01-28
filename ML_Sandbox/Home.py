import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import smtplib
from email.mime.text import MIMEText

# ----
# Helper Functions
# ----
sender_email = 'mlsandboxproject@gmail.com'
sender_password = 'ubdp ibcf ohms unol'
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
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

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
        authenticator.logout('Logout', 'main')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

elif selected == 'Create Account':
    try:
        if authenticator.register_user(preauthorization=False):
            st.success('User registered successfully')
            with open('users.yaml', 'w') as file:
                yaml.dump(users, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

elif selected == 'Forgot Password':
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

 



