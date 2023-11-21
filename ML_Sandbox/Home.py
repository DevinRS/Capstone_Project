import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

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
    menu_title= "Pathfinder",
    options=['Login', 'Create Account', 'Forgot Password'],
    icons=['box-arrow-in-right', 'person-plus', 'x-circle'],
    orientation="horizontal"
)

# ----
# Body
# ----
if selected == 'Login':
    st.write('#')
    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        with st.form('login_form'):
            st.subheader('Login')
            username = st.text_input(label='Username', placeholder='Enter Username')
            password = st.text_input(label='Password', placeholder='Enter Password', type='password')
            st.write('#')
            submit_button = st.form_submit_button(label='Login')
    with col3:
        st.image(Image.open('first.png'), width=300)

elif selected == 'Create Account':
    st.write('#')
    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        with st.form('create_form'):
            st.subheader('Sign Up')
            email = st.text_input(label='Email', placeholder='Enter Email')
            username = st.text_input(label='Username', placeholder='Enter Username')
            password = st.text_input(label='Password', placeholder='Enter Password', type='password')
            st.write('#')
            submit_button = st.form_submit_button(label='Sign Up')
    with col3:
        st.image(Image.open('first.png'), width=300)

elif selected == 'Forgot Password':
    st.write('#')
    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        with st.form('forgot_form'):
            st.subheader('Forgot Password')
            email = st.text_input(label='Email', placeholder='Enter Email')
            st.write('#')
            submit_button = st.form_submit_button(label='Forgot Password')
    with col3:
        st.image(Image.open('first.png'), width=300)

 



