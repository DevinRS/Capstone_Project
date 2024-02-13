import string
import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
import yaml
from yaml.loader import SafeLoader
import requests


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

# ----
# Defining the database objects
# ----
Base = declarative_base()
class Models(Base):
    #set table name and columns
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    __tablename__ = "posts"
    MLname = Column("name", String)
    post_owner = Column("owner", String)
    description = Column("description", String)
    longDescription = Column("longDesc", String)
    item = Column("item", PickleType)
    numLikes = Column("likes", Integer)
    numDislikes = Column("dislikes", Integer)
    uploadTime = Column("date", String)

    def __init__ (self, MLname, post_owner, description, longDescription, item, numLikes, numDislikes, uploadTime):
        self.MLname = MLname
        self.post_owner = post_owner
        self.description = description
        self.longDescription = longDescription
        self.item = item
        self.numLikes = numLikes
        self.numDislikes = numDislikes
        self.uploadTime = uploadTime
    
    def __repr__ (self):   
            return f"{self.MLname}, {self.description}, {self.longDescription}, {self.item}, {self.numLikes}, {self.numDislikes}, {self.uploadTime}"


engine = create_engine("sqlite:///file_uploads.db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


# ----
# Title of the Page
# ----

title_css = """
<style>
    .page-title {
        font-size: 50px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-top: 20px;
    }
</style>
"""


st.markdown(title_css, unsafe_allow_html=True)


st.markdown('<p class="page-title">Community Cloud</p>', unsafe_allow_html=True)
st.divider()
st.header('Create a Post', anchor=None)

# Create a post
with st.form(key="uploadModelForm", clear_on_submit=True):
    post_owner = st.session_state['username']
    
    modelName = st.text_input(label='Model Name:')
    modelDescription = st.text_area(label='Short Description of Model', 
                                    placeholder='e.g.  probabilistic machine learning algorithm')
    modelLongDesc = st.text_area(label='Detailed Description of Model', 
                                placeholder='e.g. Naïve Bayes is a probabilistic machine learning algorithm used for many classification functions and is based on the Bayes theorem. Gaussian Naïve Bayes is the extension of naïve Bayes. While other functions are used to estimate data distribution, Gaussian or normal distribution is the simplest to implement as you will need to calculate the mean and standard deviation for the training data.')
    modelItem = st.file_uploader(label='Upload Model', type = ['pkl', 'pickle'], key = 'model_file')
    modelNumLikes = 0
    modelNumDislikes = 0
    uploadButton = st.form_submit_button(label='Upload Your Post')
    modelTime = datetime.datetime.now().strftime('%m/%d/%Y')
    if (uploadButton == True):
        if (len(modelName) == 0):
            st.warning('Please enter a model name')
        else:
            existing_model = session.query(Models).filter(Models.MLname == modelName).first()

            if existing_model:
                st.warning(f'Model name "{modelName}" already exists. Please choose a different name')
            else:
                if modelItem == None:
                    st.warning('Please upload a file for your model.')
                else:
                    # model = Models(modelName, post_owner, modelDescription, modelLongDesc, modelItem, modelNumLikes, modelNumDislikes, modelTime) 
                    # session.add(model)
                    # session.commit()
                    
                    # st.success(f'Model "{modelItem.name}" has been successfully uploaded!')
                    # st.rerun()

                    # Send a request to the API instead of directly adding to the database. API is hosted locally on port 8000. Ignore file upload for now
                    url = 'http://localhost:8000/posts/'
                    data = {
                        "MLname": modelName,
                        "post_owner": post_owner,
                        "description": modelDescription,
                        "longDescription": modelLongDesc,
                        "numLikes": modelNumLikes,
                        "numDislikes": modelNumDislikes,
                        "uploadTime": modelTime
                    }
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        st.success(f'Model "{modelName}" has been successfully uploaded!')
                        st.rerun()
                    else:
                        st.error(f'Failed to upload model. Please try again later.')

        
    
    
#clears all ML models
clearModels = st.button('clear Models', key='clearModels', type='primary')
if (clearModels):
    session.query(Models).delete()
    session.commit()
    st.success('All models have been deleted')


# def display_models():
    # models = session.query(Models).all()

    # if not models:
    #     st.info("No Models bitch")
    
    # else:
    #     for model in models:
    #         st.subheader(model.MLname)
    #         st.write(f"Post id: {model.post_id}")
    #         st.write(f"Uploaded by: {model.post_owner}")
    #         st.write(f"Description: {model.description}")
    #         st.write(f"Detailed Description: {model.longDescription}")
    #         st.write(f"Number of Likes: {model.numLikes}")
    #         st.write(f"Number of Dislikes: {model.numDislikes}")
    #         st.write(f"Upload Time: {model.uploadTime}")
    #         st.markdown("---")

    # Use API calls instead
    


#get all ML models
getModels = st.button('Get Models', key='getModels', type='primary')
if (getModels):
    url = 'http://localhost:8000/posts/'
    response = requests.get(url)
    st.write(response)

