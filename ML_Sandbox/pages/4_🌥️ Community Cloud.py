import string
import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc

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

# ----
# Defining the database objects
# ----
Base = declarative_base()
class Models(Base):
    #set table name and columns
    __tablename__ = "models"
    MLname = Column("name", String, primary_key=True)
    description = Column("description", String)
    longDescription = Column("longDesc", String)
    # downloads = Column("downloads", Integer)
    item = Column("item", PickleType)
    rating = Column("rating", Integer)
    uploadTime = Column("date", String)

    def __init__ (self, MLname, description, longDescription, item, rating, uploadTime): #, rating, downloads, uploadTime):
        self.MLname = MLname
        self.description = description
        self.longDescription = longDescription
        # self.downloads = downloads
        self.item = item
        self.rating = rating
        self.uploadTime = uploadTime
    
    def __repr__ (self):
        return f"{self.MLname}, {self.description}, {self.longDescription}, {self.item.name}, {self.rating}, {self.uploadTime}"


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



# change rating from ints to stars
def ratingToStars(rating):
    stars = "⭐" * rating
    return stars


# ----
# Create Post
# ----
with st.form(key="uploadModelForm", clear_on_submit=True):
    modelName = st.text_input(label='Model Name:')
    modelDescription = st.text_area(label='Short Description of Model', 
                                    placeholder='e.g.  probabilistic machine learning algorithm')
    modelLongDesc = st.text_area(label='Detailed Description of Model', 
                                placeholder='e.g. Naïve Bayes is a probabilistic machine learning algorithm used for many classification functions and is based on the Bayes theorem. Gaussian Naïve Bayes is the extension of naïve Bayes. While other functions are used to estimate data distribution, Gaussian or normal distribution is the simplest to implement as you will need to calculate the mean and standard deviation for the training data.')
    modelItem = st.file_uploader(label='Upload Model 😊', type = ['pkl', 'pickle'], key = 'model_file')
    modelRating = 4
    uploadButton = st.form_submit_button(label='Upload Your Post')
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

                    modelTime = datetime.datetime.now().strftime('%m/%d/%Y')
                    
                    model = Models(modelName, modelDescription, modelLongDesc, modelItem, modelRating, modelTime) 
                    session.add(model)
                    session.commit()

                    

                    st.success(f'Model "{modelItem.name}" has been successfully uploaded!')
                    st.rerun()


#creates random ML models
from faker import Faker
import os
fake = Faker()

os.makedirs('pickle_files', exist_ok=True)
os.makedirs('json_files', exist_ok=True)
generated_names = set()
createRandomMls = st.button('create random MLs', type='primary')
if (createRandomMls):
    for i in range(10):
        while True:
            randomName = fake.first_name()

            if randomName not in generated_names:
                generated_names.add(randomName)
                break

        randomDesc = fake.text()
        randomLongDesc = fake.text()
        randomRating = fake.random_int(min=1, max=5)
        randomUploadTime = fake.date_time_this_decade().strftime('%m/%d/%Y')

        random_data = {
            'name': randomName,
            'desc': randomDesc,
            'rating': randomRating
        }

        #Save pickle file
        pickle_filename = f'pickle_files/random_data{i}.pkl'
        with open(pickle_filename, 'wb') as file:
            pickle.dump(random_data, file)
        
        #save json file
        json_filename = f'json_files/random_data{i}.json'
        with open(json_filename, 'w') as file:
            json.dump(random_data, file, indent=2)

        randomModel = Models(
            MLname=random_data['name'],
            description=random_data['desc'],
            longDescription=randomLongDesc,
            item=random_data,
            rating=random_data['rating'],
            uploadTime=randomUploadTime
        )

        session.add(randomModel)
        session.commit()
    st.success('Created 10 random models')

#clears all ML models
clearModels = st.button('clear Models', key='clearModels', type='primary')
if (clearModels):
    session.query(Models).delete()
    session.commit()
    st.success('All models have been deleted')



# ----
# Filter displays
# ----
st.header('Community Posts')


# ----
# Display Models Def
# ----
def display_models():
    st.subheader(model.MLname, anchor=False, divider=False)
    st.write(model.description)
    MLlongDesc = model.longDescription
    st.expander('Read More').write(MLlongDesc)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.caption(model.uploadTime)
    with col2:
        st.caption(ratingToStars(model.rating))
    
    with col5:
        # Download button for pickle format
        download_button_label = f"{model.MLname}.pkl"
        file_name = f"{model.MLname}.pkl"
        binaryData = pickle.dumps(model.item)
        binaryDataBytes = bytes(binaryData)

        
        button_html = f'''
            <style>
                .download-button {{
                    text-decoration: none;
                    padding: 5px 10px;
                    border-radius: 50px;
                    text-align: center;
                    color: white;
                    background-color: #ff6e1c;
                    border: solid 1px #ffda89;
                    font-family: 'Roboto', sans-serif;
                    transition: 0.3s;
                }}
                .download-button:hover {{
                    background-color: #ffd884;
                    color: #ff6e1c;
                    border: solid 1px #ff6e1c;
                }}
            </style>
            <a href="data:application/octet-stream;base64,{base64.b64encode(binaryDataBytes).decode()}"
            download="{file_name}" class="download-button">
                {download_button_label}
            </a>
        '''
        components.html(button_html, height=50)

        # Download Button for JSON format
        obj_pkl = model.item
        json_obj = json.loads(json.dumps(obj_pkl, default=str))

        post_data = {
            "type": "post",
            "id": model.MLname,
            "model": [
                {"modelName": model.MLname},
                {"modelDescription": model.description},
                {"modelLongDescription": model.longDescription},
                {"modelRating": model.rating},
                {"modelUploadTime": model.uploadTime},
                {"modelItem": json_obj}
            ]
        }

        download_button_label_json = f"{model.MLname}.json"
        file_name_json = f"{model.MLname}.json"
        json_data = json.dumps(post_data, indent=2).encode('utf-8')
        binaryDataBytes_json = bytes(json_data)
        

        button_html_json = f'''
            <style>
                .download-button {{
                    text-decoration: none;
                    padding: 5px 10px;
                    border-radius: 50px;
                    text-align: center;
                    color: white;
                    background-color: #2ecc71; /* Change color for JSON button */
                    border: solid 1px #27ae60; /* Change border color for JSON button */
                    font-family: 'Roboto', sans-serif;
                    transition: 0.3s;
                }}
                .download-button:hover {{
                    background-color: #2ecc71; /* Change hover background color for JSON button */
                    color: #27ae60; /* Change hover color for JSON button */
                    border: solid 1px #27ae60; /* Change hover border color for JSON button */
                }}
            </style>
            <a href="data:application/octet-stream;base64,{base64.b64encode(binaryDataBytes_json).decode()}"
            download="{file_name_json}" class="download-button">
                {download_button_label_json}
            </a>
        '''
        components.html(button_html_json, height=50)
    
    st.divider()




# ----
# Search Bar
# ----
with st.form(key='searchForm', clear_on_submit=True):

    searchQuery = st.text_input(' Search Posts', '', placeholder='🔍 Search Community Posts', )

    results = session.query(Models).all()
    filteredResults = [model for model in results if searchQuery.lower() in model.MLname.lower()]
    searchButton = st.form_submit_button(label='search')

    if (searchQuery):
        if (not filteredResults):
            st.warning('No matching results found.')
        else:
            for model in filteredResults:
                display_models()



# ----
# Filtered Results
# ----
with st.container():
    tab1, tab2, tab3 = st.tabs(['Alphabetical', 'Newest', 'Rating'])
    with tab1:
        results = session.query(Models).order_by(Models.MLname).all()
        for model in results:
            display_models()

    with tab2:
        results = session.query(Models).order_by(Models.uploadTime.desc()).all()
        for model in results:
            display_models()
            
    with tab3:
        results = session.query(Models).order_by(Models.rating.desc()).all()
        for model in results:
            display_models()
        
