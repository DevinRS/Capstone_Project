import string
import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
import yaml
from yaml.loader import SafeLoader
import requests
from PIL import Image
import io
import os


# ----
# Page Config
# ----
st.set_page_config(
    page_title='Explore the Community!',
    page_icon='🚀',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)


with hc.HyLoader('Loading Community Cloud',hc.Loaders.standard_loaders,index=5):
    import pickle
    from sqlalchemy import create_engine, Column, Integer, String, DateTime
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.types import PickleType
    import datetime
    import base64
    import streamlit.components.v1 as components
    import json


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if st.session_state['authentication_status'] is not True:
    st.warning('You are not logged in! Please login to access this page.')
    st.stop()

# ----
# Sidebar
# ----
with st.sidebar:
    try:
        file_name = 'profilepic_files/' + st.session_state['username'] + '_pic.png'
        st.image(file_name, use_column_width=True)
    except Exception as e:
        st.image('profilepic_files/default_avatar.jpg', use_column_width=True)  
    
    # Get Merit for the user using API: http://localhost:8000/calculateusermerit/{username}
    url = 'http://localhost:8000/calculateusermerit/' + st.session_state['username']
    response = requests.get(url)
    if response.status_code == 200:
        st.write('Merit: ' + str(response.json().get('merit')))
    else:
        st.error('Failed to get merit. Please try again later.')
        # get the response content details only
        st.error(response.json().get('detail'))


# ----
# Title of the Page
# ----

# ----
# Create a new post
# ----
with st.form(key="uploadModelForm", clear_on_submit=True):
    post_owner = st.session_state['username']
    
    modelName = st.text_input(label='Model Name:')
    modelDescription = st.text_area(label='Short Description of Model', 
                                    placeholder='e.g.  probabilistic machine learning algorithm')
    modelLongDesc = st.text_area(label='Detailed Description of Model', 
                                placeholder='e.g. Naïve Bayes is a probabilistic machine learning algorithm used for many classification functions and is based on the Bayes theorem. Gaussian Naïve Bayes is the extension of naïve Bayes. While other functions are used to estimate data distribution, Gaussian or normal distribution is the simplest to implement as you will need to calculate the mean and standard deviation for the training data.')
    modelItem = st.file_uploader(label='Upload Model', type = ['pkl', 'pickle'], key = 'model_file')
    uploadButton = st.form_submit_button(label='Upload Your Post')
    modelTime = datetime.datetime.now().strftime('%m/%d/%Y')
    if (uploadButton == True):
        if (len(modelName) == 0):
            st.warning('Please enter a model name')
        elif (modelItem == None):
            st.warning('Please upload a file for your model.')
        else:
            # Send a request to the API instead of directly adding to the database. API is hosted locally on port 8000. Ignore file upload for now
            url = 'http://localhost:8000/posts/'
            data = {
                "MLname": modelName,
                "post_owner": post_owner,
                "description": modelDescription,
                "longDescription": modelLongDesc,
                "uploadTime": modelTime
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.write(response.json().get('post_id'))
                post_id = response.json().get('post_id')
                filename = 'postmodel_files/' + (str)(post_id) + '_model.pkl'
                with open(filename, 'wb') as f:
                    f.write(modelItem.getvalue())

                st.success(f'Model "{modelName}" has been successfully uploaded!')
            else:
                st.error(f'Failed to upload model. Please try again later.')
                # get the response content details only
                st.error(response.json().get('detail'))

# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "Community Cloud",
    options=['Sort By Date' , 'Sort By Name', 'Sort By Popularity'],
    orientation="horizontal",
    menu_icon="cloud-sun",
)

# ----
# Get Posts
# ----
with hc.HyLoader('Loading Posts',hc.Loaders.standard_loaders,index=5):
    if selected == 'Sort By Date':
        url = 'http://localhost:8000/postsdenormalizedsortedbydate/'
    elif selected == 'Sort By Name':
        url = 'http://localhost:8000/postsdenormalizedsortedbyname/'
    elif selected == 'Sort By Popularity':
        url = 'http://localhost:8000/postsdenormalizedsortedbyratio/'
    response = requests.get(url)

    for model in response.json():
        with st.container(border=1):
            col1, col2, col3= st.columns([1, 10, 1])
            with col1:
                try:
                    pimage = Image.open('profilepic_files/' + model['post_owner'] + '_pic.png')
                    st.image(pimage, use_column_width=True)
                except:
                    st.image('profilepic_files/default_avatar.jpg', use_column_width=True)
                st.write('👍: ' + str(model['like']))
                st.write('👎: ' + str(model['dislike']))
            with col2:
                st.write(model['post_owner'] + ', ' + model['uploadTime'])
                st.title(model['MLname'])
                st.write(model['description'])
                with st.expander('View More'):
                    st.write(model['longDescription'])
            with col3:
                try:
                    file_name = 'postmodel_files/' + (str)(model['post_id']) + '_model'
                    with open(file_name + '.pkl', 'rb') as f:
                        model_data = io.BytesIO(f.read())
                    st.download_button(label='Download', data=model_data, file_name=model['MLname'] + '.pkl',use_container_width=True)
                except:
                    st.warning('No Model')
                # Check if the post is owned by the user, if it is, show the delete button
                if (model['post_owner'] == st.session_state['username']):
                    st.button('Delete', key=model['MLname'] + '_delete', use_container_width=True)
                    if st.session_state[model['MLname'] + '_delete']:
                        url = 'http://localhost:8000/posts/' + str(model['post_id'])
                        response = requests.delete(url)
                        if response.status_code == 200:
                            # Delete the model file
                            filename = 'postmodel_files/' + (str)(model['post_id']) + '_model.pkl'
                            try:
                                os.remove(filename)
                            except:
                                pass
                            st.rerun()
                        else:
                            st.error(f'Failed to delete model. Please try again later.')
                            # get the response content details only
                            st.error(response.json().get('detail'))

                # Like and Dislike buttons using API: http://localhost:8000/like/{post_id}/{owner_name}/{likeOrDislike}
                likeButton = st.button('Like', key=model['MLname'] + '_like', use_container_width=True)
                if likeButton:
                    url = 'http://localhost:8000/like/' + str(model['post_id']) + '/' + st.session_state['username'] + '/1'
                    response = requests.post(url)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f'Failed to like model. Please try again later.')
                        # get the response content details only
                        st.error(response.json().get('detail'))

                dislikeButton = st.button('Dislike', key=model['MLname'] + '_dislike', use_container_width=True)
                if dislikeButton:
                    url = 'http://localhost:8000/like/' + str(model['post_id']) + '/' + st.session_state['username'] + '/0'
                    response = requests.post(url)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f'Failed to dislike model. Please try again later.')
                        # get the response content details only
                        st.error(response.json().get('detail'))

                        

                


            

