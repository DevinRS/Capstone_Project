import streamlit as st
from streamlit_option_menu import option_menu



# ----
# Page Config
# ----
st.set_page_config(
    page_title='Train a Model!',
    page_icon='📊',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "Pathfinder",
    options=['Upload', 'Modify Model', 'Run Model'],
    orientation="horizontal"
)

# ----
# Body
# ----
# 1. Input Section
input_file = None

if selected == 'Upload':
    st.header('Upload File')
    input_file = st.file_uploader('Choose a CSV file', type='csv', key='input_file')
    df = None

if selected == 'Modify Model':
    st.header("Modify your ML Model")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_model = st.selectbox(
            'Select ML Model to work with',
            ('Model 1', 'Model 2', 'Model 3')
        )
    with col3:    
        st.link_button('Browse community models', url="/Community_Cloud")

    st.subheader(selected_model + " settings")
    col4, col5 = st.columns((1,5))
    st.write('\n')
    
    with col4:
        st.text_input("Setting 1")
        st.text_input("Setting 2")
        st.text_input("Setting 3")
        st.text_input("Setting 4")



if selected == 'Run Model':
    st.header('Run Model')
    st.subheader(f'Running Model (selected model) on (input file)')

