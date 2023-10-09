import streamlit as st
from streamlit_option_menu import option_menu


# ----
# Page Config
# ----
st.set_page_config(
    page_title='Explore the Community!',
    page_icon='📊',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)



# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "Community Cloud",
    options=['Create Post', 'Rating', 'Used', 'Trending', 'Alphabetical'],
    orientation="horizontal",
)

# ----
# Body
# ----
if(selected == 'Create Post'):
    st.header('Create a Post!')
    st.text_area(label='Post Body')
    st.file_uploader(label='Have a Model? Upload It Here 😊')
    st.button(label='Upload Your Post')

if(selected == 'Rating'):
    st.header('This will be the area where user see other\'s post, sorted by rating')

if(selected == 'Used'):
    st.header('This will be the area where user see other\'s post, sorted by used')
 
if(selected == 'Trending'):
    st.header('This will be the area where user see other\'s post, sorted by Trending')

if(selected == 'Alphabetical'):
    st.header('This will be the area where user see other\'s post, sorted by Alphabetical')


