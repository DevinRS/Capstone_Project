import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pycaret.classification as pycaret_classification
import pycaret.regression as pycaret_regression
import pycaret.clustering as pycaret_clustering

# ----
# Definition and Globals
# ----
# Session States
if 'input_dataframe_page2' not in st.session_state:
    st.session_state['input_dataframe_page2'] = pd.DataFrame()

if 'last_input_2' not in st.session_state:
    st.session_state['last_input_2'] = None

if 'profile_report' not in st.session_state:
    st.session_state['profile_report'] = None

# Classification
if 'ml_settings_classification' not in st.session_state:
    st.session_state['ml_settings_classification'] = None
if 'best_model_classification' not in st.session_state:
    st.session_state['best_model_classification'] = None
if 'compare_models_classification' not in st.session_state:
    st.session_state['compare_models_classification'] = None

# Regression
if 'ml_settings_regression' not in st.session_state:
    st.session_state['ml_settings_regression'] = None
if 'best_model_regression' not in st.session_state:
    st.session_state['best_model_regression'] = None
if 'compare_models_regression' not in st.session_state:
    st.session_state['compare_models_regression'] = None


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

# ----
# Train Model Section
# ----
if selected == 'Train Model':
    # 1. Select Problem Type
    st.header('Select Problem Type')
    problem_type = st.radio(
        'What problem are you trying to solve?',
        ('Classification', 'Regression', 'Clustering')
    )

    # 2. Select Auto/Manual Mode
    st.header('Select Mode')
    mode = st.radio(
        'Do you want to use AutoML or Manual Mode?',
        ('AutoML', 'Manual Mode')
    )

    # 3. Input Section
    st.header('Upload File')
    input_file = st.file_uploader('Choose a CSV file', type='csv', key='input_file')
    
    if input_file is not None:
        df = pd.read_csv(input_file)
        st.session_state['input_dataframe_page2'] = df
        st.session_state['last_input_2'] = input_file.name
        st.session_state['profile_report'] = None
        st.session_state['ml_settings_classification'] = None
        st.session_state['best_model_classification'] = None
        st.session_state['compare_models_classification'] = None
        st.session_state['ml_settings_regression'] = None
        st.session_state['best_model_regression'] = None
        st.session_state['compare_models_regression'] = None

    if st.session_state['last_input_2'] is not None:
        st.write('Last Uploaded File:')
        st.info(st.session_state["last_input_2"])

    # 4. Data Profiling and Model Training
    if st.session_state['input_dataframe_page2'].empty == False:
        df = st.session_state['input_dataframe_page2']
        st.write(df)

        st.write('''---''')
        # AutoML
        if mode == 'AutoML':
            st.header('AutoML')
            data_profiling_cb = st.checkbox('Data Profiling', value=False, help='Generate a report on the dataset')
            train_model_cb = st.checkbox('Train Model', value=False, help='Train a model on the dataset')
            if problem_type == 'Classification' or problem_type == 'Regression':
                target = st.selectbox('Select Target Variable', df.columns)
            elif problem_type == 'Clustering':
                target = st.selectbox('Select Clustering Models', ['kmeans', 'ap', 'meanshift', 'sc', 'hclust', 'dbscan', 'optics', 'birch', 'kmodes'], help='kmeans = K-Means Clustering, ap = Affinity Propagation, meanshift = Mean Shift Clustering, sc = Spectral Clustering, hclust = Agglomerative Clustering, dbscan = Density-Based Spatial Clustering, optics = OPTICS Clustering, birch = Birch Clustering, kmodes = K-Modes Clustering')
            if st.button('Run AutoML'):
                if data_profiling_cb:
                    if st.session_state['profile_report'] is None:
                        profile_report = ProfileReport(df)
                        st.session_state['profile_report'] = profile_report
                    else:
                        profile_report = st.session_state['profile_report']
                    st.info('Data Profiling')
                    st_profile_report(profile_report)

                if train_model_cb:
                    if problem_type == 'Classification':
                        with st.spinner('Running AutoML...'):
                            if st.session_state['ml_settings_classification'] is None:
                                pycaret_classification.setup(df, target=target, verbose=False)
                                setup_df = pycaret_classification.pull()
                                st.session_state['ml_settings_classification'] = setup_df
                            else:
                                setup_df = st.session_state['ml_settings_classification']
                            st.info('ML Settings')
                            st.dataframe(setup_df)
                            if st.session_state['best_model_classification'] is None:
                                best_model = pycaret_classification.compare_models()
                                st.session_state['best_model_classification'] = best_model
                            else:
                                best_model = st.session_state['best_model_classification']
                            if st.session_state['compare_models_classification'] is None:
                                compare_models_df = pycaret_classification.pull()
                                st.session_state['compare_models_classification'] = compare_models_df
                            else:
                                compare_models_df = st.session_state['compare_models_classification']
                            st.info('Model Comparison')
                            st.dataframe(compare_models_df)
                            st.info('Model Interpretation')
                            st.write(pycaret_classification.interpret_model(best_model, plot='msa'))
                    elif problem_type == 'Regression':
                        with st.spinner('Running AutoML...'):
                            if st.session_state['ml_settings_regression'] is None:
                                pycaret_regression.setup(df, target=target, verbose=False)
                                setup_df = pycaret_regression.pull()
                                st.session_state['ml_settings_regression'] = setup_df
                            else:
                                setup_df = st.session_state['ml_settings_regression']
                            st.info('ML Settings')
                            st.dataframe(setup_df)
                            if st.session_state['best_model_regression'] is None:
                                best_model = pycaret_regression.compare_models()
                                st.session_state['best_model_regression'] = best_model
                            else:
                                best_model = st.session_state['best_model_regression']
                            if st.session_state['compare_models_regression'] is None:
                                compare_models_df = pycaret_regression.pull()
                                st.session_state['compare_models_regression'] = compare_models_df
                            else:
                                compare_models_df = st.session_state['compare_models_regression']
                            st.info('Model Comparison')
                            st.dataframe(compare_models_df)
                            st.info('Model Interpretation')
                            st.write(pycaret_regression.interpret_model(best_model, plot='msa'))
                    elif problem_type == 'Clustering':
                        with st.spinner('Running AutoML...'):
                            pycaret_clustering.setup(df, verbose=False)
                            setup_df = pycaret_clustering.pull()
                            st.info('ML Settings')
                            st.dataframe(setup_df)
                            best_model = pycaret_clustering.create_model(target)
                            assign_model_df = pycaret_clustering.assign_model(best_model)
                            st.info('Cluster Assignments')
                            st.dataframe(assign_model_df)


if selected == 'Run Model':
    st.header('Run Model')


# ----
# Tutorial Section
# ----
st.write('''---''')
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
    st.subheader('Running a Model')
    st.write('''
After you have trained a model, you can run it on a new dataset to make predictions. You can upload a new dataset or use the one you trained the model on. The model will make predictions on the new dataset and output a CSV file with the predictions. You can download this file and use it for further analysis.
''')

