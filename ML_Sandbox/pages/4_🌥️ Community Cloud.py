from fileinput import filename
import string
from tkinter.font import BOLD
from turtle import down
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import PickleType
import datetime

# ----
# Defining the database objects
# ----
Base = declarative_base()
class Models(Base):
    __tablename__ = "models"
    MLname = Column("name", String, primary_key=True)
    description = Column("description", String)
    # rating = Column("rating", Integer)
    # downloads = Column("downloads", Integer)
    item = Column("item", PickleType)
    # uploadTime = Column("time", DateTime, default=datetime.datetime.utcnow)

    def __init__ (self, MLname, description, item): #, rating, downloads, uploadTime):
        self.MLname = MLname
        self.description = description
        # self.rating = rating
        # self.downloads = downloads
        self.item = item
        # self.uploadTime = uploadTime
    
    def __repr__ (self):
        return f"{self.MLname}, {self.description}, {self.item.name}"


engine = create_engine("sqlite:///file_uploads.db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


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
    with st.form(key="uploadModelForm", clear_on_submit=True):
        modelName = st.text_input(label='Enter the machine learning model name')
        modelDescription = st.text_area(label='Post Body')
        modelItem = st.file_uploader(label='Have a Model? Upload It Here 😊', type = ['pkl', 'pickle'], key = 'model_file')
        uploadButton = st.form_submit_button(label='Upload Your Post')
        # modelTime = datetime.datetime.utcnow
        if (uploadButton == True):
            model = Models(modelName, modelDescription, modelItem) #modelTime) 
            session.add(model)
            session.commit()
            st.success(f'Model "{modelItem.name}" has been successfully uploaded!')
            st.rerun()

        results = session.query(Models).all()
    st.write(results)
    

if(selected == 'Rating'):
    st.header('This will be the area where user see other\'s post, sorted by rating')

if(selected == 'Used'):
    st.header('This will be the area where user see other\'s post, sorted by used')
 
if(selected == 'Trending'):
    st.header('This will be the area where user see other\'s post, sorted by Trending')

if(selected == 'Alphabetical'):
    st.header('This will be the area where user see other\'s post, sorted by Alphabetical')


