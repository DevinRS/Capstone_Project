import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# ----
# Definition and Globals
# ----
# Session States
if 'input_dataframe_page2' not in st.session_state:
    st.session_state['input_dataframe_page2'] = pd.DataFrame()

if 'last_input_2' not in st.session_state:
    st.session_state['last_input_2'] = None



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
    menu_title= "Autodidact",
    options=['Train Model', 'Run Model'],
    orientation="horizontal"
)

# ----
# Body
# ----
# 1. Input Section
if selected == 'Train Model':
    st.header('Upload File')
    input_file = st.file_uploader('Choose a CSV file', type='csv', key='input_file')
    
    if input_file is not None:
        df = pd.read_csv(input_file)
        st.session_state['input_dataframe_page2'] = df
        st.session_state['last_input_2'] = input_file.name

    if st.session_state['last_input_2'] is not None:
        st.write('Last Uploaded File:')
        st.info(st.session_state["last_input_2"])

        df = st.session_state['input_dataframe_page2']
        st.subheader('1. Data Preview')
        st.write(df)

        st.subheader('2. Train Model')
        manual_mode = st.checkbox('Manual Mode')

        st.subheader('3. Download Model')
    

if selected == 'Run Model':
    st.header('Run Model')

# ----
# Tutorial Section
# ----
with st.expander(label='Tutorial'):
    st.header('Not familiar with machine learning?')
    st.write('''
Welcome to the fascinating realm of machine learning, where computers learn and make predictions just like humans, but with a dash of technological wizardry! 🤖🌟 If you find yourself puzzled by the term 'machine learning,' don't worry – we're here to demystify it for you. No prior machine learning knowledge required – just bring your curiosity and data, and we'll guide you through the exciting journey of teaching machines to do incredible things. Get ready to impress your friends and colleagues with your newfound machine learning insights. Are you ready? Let's embark on this exciting adventure!
''')
    st.subheader('Training a Model')
    st.write('''
In ML Sandbox, we have the capability to automate the machine learning process so you don't have to worry about all those machine wizardry! The only thing we ask for you is to ask yourself the following question!
             
''')
    st.subheader('What problem am I trying to solve?')
    st.subheader('Classification 📊')
    st.write('''
Classification is a type of supervised learning where the machine learns from the data input given to it and then uses this learning to classify new observation. This algorithm is used to predict a discrete value. E.g. If an email is spam or not spam; If a tumor is malignant or benign.
             
Some common classification algorithms are:
1. Logistic Regression
2. Decision Tree
3. Random Forest
''')
    st.subheader('Regression 📈')
    st.write('''
Regression is a type of supervised learning where the machine learns from the data input given to it and then uses this learning to predict the value of a continuous variable. E.g. What will be the temperature today?; What is the probability that there will be a snowstorm tomorrow?
             
Some common regression algorithms are:
1. Linear Regression
2. Decision Tree
3. Random Forest
''')
    st.subheader('Clustering 🔍')
    st.write('''
Clustering is a type of unsupervised learning where the machine learns from the data input given to it and then uses this learning to group similar observations together. E.g. Grouping customers by purchasing behavior; Grouping stocks by their price movements.
             
Some common clustering algorithms are:
1. K-Means Clustering
2. Hierarchical Clustering
3. DBSCAN
''')
    st.subheader('Dimensionality Reduction 🧮')  
    st.write('''
Dimensionality reduction is a type of unsupervised learning where the machine learns from the data input given to it and then uses this learning to reduce the number of variables in the data. E.g. Reducing the number of variables in a dataset to make it easier to analyze.
             
Some common dimensionality reduction algorithms are:
1. Principal Component Analysis (PCA)
2. Linear Discriminant Analysis (LDA)
3. t-distributed Stochastic Neighbor Embedding (t-SNE)
''')
    st.subheader('Running a Model')
    st.write('''
After you have trained a model, you can run it on a new dataset to make predictions. You can upload a new dataset or use the one you trained the model on. The model will make predictions on the new dataset and output a CSV file with the predictions. You can download this file and use it for further analysis.
''')

