import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hydralit_components as hc
import pickle
import io

# ----
# Page Config
# ----
st.set_page_config(
    page_title='Train a Model!',
    page_icon='🚀',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

with hc.HyLoader('Loading Autodidact',hc.Loaders.standard_loaders,index=5):
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

if 'overall_settings' not in st.session_state:
    st.session_state['overall_settings'] = None

if 'train_model_accessed' not in st.session_state:
    st.session_state['train_model_accessed'] = False

# Classification
if 'classification_setup' not in st.session_state:
    st.session_state['classification_setup'] = None

if 'classification_comparison_df' not in st.session_state:
    st.session_state['classification_comparison_df'] = None

if 'classification_models' not in st.session_state:
    st.session_state['classification_models'] = None

# Regression
if 'regression_setup' not in st.session_state:
    st.session_state['regression_setup'] = None

if 'regression_comparison_df' not in st.session_state:
    st.session_state['regression_comparison_df'] = None

if 'regression_models' not in st.session_state:
    st.session_state['regression_models'] = None

# Clustering
if 'clustering_setup' not in st.session_state:
    st.session_state['clustering_setup'] = None

if 'clustering_comparison_df' not in st.session_state:
    st.session_state['clustering_comparison_df'] = None

if 'clustering_models' not in st.session_state:
    st.session_state['clustering_models'] = None


# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "Autodidact",
    options=['Upload' , 'Data Preprocessing', 'Train Model', 'Run Model'],
    orientation="horizontal",
    menu_icon="robot",
)

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
# Body
# ----
# 1. Input Section
# - This section is used to upload a CSV file
# - The uploaded file is stored in the session state
# - The name of the last uploaded file is also stored in the session state
if(selected == 'Upload'):
    st.header('Upload File')
    input_file = st.file_uploader('Choose a CSV file', type='csv', key='input_file')

    if input_file is not None:
        df = pd.read_csv(input_file)
        st.session_state['input_dataframe_page2'] = df
        st.session_state['last_input_2'] = input_file.name

    if st.session_state['last_input_2'] is not None:
        st.write('Last Uploaded File:')
        st.info(st.session_state["last_input_2"])

# 2. Data Preprocessing Section
# - This section is split into 5 major parts (Data Preparation, Scale and Transform, Feature Engineering, Feature Selection, and Model Selection)
# - Data Preparation: The user can select the data preparation steps (missing values imputation, One-Hot Encoding, Ordinal Encoding, Target Imbalance Correction, Outlier Removal)
# - Scale and Transform: The user can select the scaling and transformation steps (Normalization, Feature Transformation, Target Transformation(only for regression))
# - Feature Engineering: The user can select the feature engineering steps (Polynomial Features, Group Features, Bin Numeric Features)
# - Feature Selection: The user can select the feature selection steps (Feature Selection, Remove Multicollinearity, PCA, Ignore Low Variance, Ignore Features)
# - Model Selection: The user can select the model selection steps (Training Size, Shuffle, Stratification, Fold Strategy, Number of Fold)
if selected == 'Data Preprocessing':
    if(st.session_state['input_dataframe_page2'].empty == True):
        st.error('Error: Input file not found!')
    else:
        # Display Input Dataframe
        st.header('Data Preprocessing')
        df = st.session_state['input_dataframe_page2']
        st.dataframe(df, use_container_width=True)

        # If train_model_accessed is True, then the user has already accessed the Train Model section
        if st.session_state['train_model_accessed'] == True:
            st.warning('Warning: Settings have been reset!')

        # Data Preparation
        st.subheader('Data Preparation')

        # This block of code will run if initialize_settings is False
        # -- Missing Values Imputation --
        # create a 2 column 
        with st.container(border=True):
            st.subheader('Missing Values Imputation')
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox('Imputation Type', ['simple', 'iterative', None], help='Simple imputation uses the mean for numerical features and the mode for categorical features. Iterative imputation uses the KNN algorithm to impute missing values.', key='imputation_type')
                # numeric_imputation selectbox (drop, mean, median, mode, knn)
                if st.session_state['imputation_type'] == None:
                    st.selectbox('Numeric Imputation', ['drop', 'mean', 'median', 'mode', 'knn'], help='Imputation technique for numeric features', key='numeric_imputation', disabled=True)
                    # categorical_imputation selectbox (drop, mode)
                    st.selectbox('Categorical Imputation', ['drop', 'mode'], help='Imputation technique for categorical features', key='categorical_imputation', disabled=True)
                    # iterative_imputation_iters slider (int)
                    st.slider('Iterative Imputation Iterations', min_value=1, max_value=10, value=5, step=1, help='Number of iterations to perform when using iterative imputation', key='iterative_imputation_iters', disabled=True)                
                else:
                    st.selectbox('Numeric Imputation', ['mean' , 'drop', 'median', 'mode', 'knn'], help='Imputation technique for numeric features', key='numeric_imputation')
                    # categorical_imputation selectbox (drop, mode)
                    st.selectbox('Categorical Imputation', ['mode', 'drop'], help='Imputation technique for categorical features', key='categorical_imputation')
                    if st.session_state['imputation_type'] == 'iterative':
                        # iterative_imputation_iters slider (int)
                        st.slider('Iterative Imputation Iterations', min_value=1, max_value=10, value=5, step=1, help='Number of iterations to perform when using iterative imputation', key='iterative_imputation_iters')
                    else:
                        st.slider('Iterative Imputation Iterations', min_value=1, max_value=10, value=5, step=1, help='Number of iterations to perform when using iterative imputation', key='iterative_imputation_iters', disabled=True)
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for missing values imputation
                missing_values_imputation_df = pd.DataFrame({
                    'Imputation Type': [st.session_state['imputation_type']],
                    'Numeric Imputation': [st.session_state['numeric_imputation']],
                    'Categorical Imputation': [st.session_state['categorical_imputation']],
                    'Iterative Imputation Iterations': [st.session_state['iterative_imputation_iters']]
                })
                # transpose the dataframe
                missing_values_imputation_df = missing_values_imputation_df.T
                # display the dataframe
                st.dataframe(missing_values_imputation_df, use_container_width=True)


        # -- Target Imbalance and Outlier --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Target Imbalance and Outlier')
            col1, col2 = st.columns(2)
            with col1:
                # fix_imbalance selectbox (True, False)
                st.selectbox('Fix Imbalance', ['False', 'True'], help='Fix imbalance in the target variable', key='fix_imbalance')
                # fix_imbalance_method selectbox (SMOTE, Random Oversampling, Random Undersampling)
                if st.session_state['fix_imbalance'] == 'True':
                    st.selectbox('Fix Imbalance Method', ['smote', 'randomoversampler', 'randomundersampler'], help='Method to fix imbalance in the target variable', key='fix_imbalance_method')
                else:
                    st.selectbox('Fix Imbalance Method', ['smote', 'randomoversampler', 'randomundersampler'], help='Method to fix imbalance in the target variable', key='fix_imbalance_method', disabled=True)
                # outlier_removal selectbox (True, False)
                st.selectbox('Remove Outliers', ['False', 'True'], help='Remove outliers from the dataset', key='remove_outliers')
                # outlier_removal_method selectbox (iforest, ee, lof)
                if st.session_state['remove_outliers'] == 'True':
                    st.selectbox('Outlier Removal Method', ['iforest', 'ee', 'lof'], help='Method to remove outliers from the dataset', key='outliers_method')
                    st.slider('Outlier Removal Threshold', min_value=0.0, max_value=1.0, value=0.05, step=0.05, help='Threshold to remove outliers from the dataset', key='outliers_threshold')
                else:
                    st.selectbox('Outlier Removal Method', ['iforest', 'ee', 'lof'], help='Method to remove outliers from the dataset', key='outliers_method', disabled=True)
                    st.slider('Outlier Removal Threshold', min_value=0.0, max_value=1.0, value=0.05, step=0.05, help='Threshold to remove outliers from the dataset', key='outliers_threshold', disabled=True)
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for target imbalance and outlier removal
                target_imbalance_outlier_df = pd.DataFrame({
                    'Fix Imbalance': [st.session_state['fix_imbalance']],
                    'Fix Imbalance Method': [st.session_state['fix_imbalance_method']],
                    'Remove Outliers': [st.session_state['remove_outliers']],
                    'Outlier Removal Method': [st.session_state['outliers_method']],
                    'Outlier Removal Threshold': [st.session_state['outliers_threshold']]
                })
                # transpose the dataframe
                target_imbalance_outlier_df = target_imbalance_outlier_df.T
                # display the dataframe
                st.dataframe(target_imbalance_outlier_df, use_container_width=True)
                


        # Scale and Transform
        st.write('---')
        st.subheader('Scale and Transform')
        # -- Normalization --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Normalization')
            col1, col2 = st.columns(2)
            with col1:
                # normalize selectbox (True, False)
                st.selectbox('Normalize', ['False', 'True'], help='Normalize the dataset', key='normalize')
                # normalize_method selectbox (minmax, zscore, maxabs, robust)
                if st.session_state['normalize'] == 'True':
                    st.selectbox('Normalize Method', ['zscore', 'minmax','maxabs', 'robust'], help='Method to normalize the dataset', key='normalize_method')
                else:
                    st.selectbox('Normalize Method', ['zscore', 'minmax','maxabs', 'robust'], help='Method to normalize the dataset', key='normalize_method', disabled=True)
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for normalization
                normalization_df = pd.DataFrame({
                    'Normalize': [st.session_state['normalize']],
                    'Normalize Method': [st.session_state['normalize_method']]
                })
                # transpose the dataframe
                normalization_df = normalization_df.T
                # display the dataframe
                st.dataframe(normalization_df, use_container_width=True)


        # -- Transformation --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Transformation')
            col1, col2 = st.columns(2)
            with col1:
                # transformation Selectbox (False, True)
                st.selectbox('Feature Transform', ['False', 'True'], help='Transform features using a power transformation method', key='transformation')
                # transformation_method selectbox (yeo-johnson, quantile)
                if st.session_state['transformation'] == 'True':
                    st.selectbox('Feature Transform Method', ['yeo-johnson', 'quantile'], help='Method to transform features', key='transformation_method')
                else:
                    st.selectbox('Feature Transform Method', ['yeo-johnson', 'quantile'], help='Method to transform features', key='transformation_method', disabled=True)
                # transform_target Transform Selectbox (False, True)
                st.selectbox('Target Transform', ['False', 'True'], help='Transform target using a power transformation method', key='transform_target')
                # transform_target_method selectbox (yeo-johnson, quantile)
                if st.session_state['transform_target'] == 'True':
                    st.selectbox('Target Transform Method', ['yeo-johnson', 'quantile'], help='Method to transform target', key='transform_target_method')
                else:
                    st.selectbox('Target Transform Method', ['yeo-johnson', 'quantile'], help='Method to transform target', key='transform_target_method', disabled=True)
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for transformation
                transformation_df = pd.DataFrame({
                    'Feature Transform': [st.session_state['transformation']],
                    'Feature Transform Method': [st.session_state['transformation_method']],
                    'Target Transform': [st.session_state['transform_target']],
                    'Target Transform Method': [st.session_state['transform_target_method']]
                })
                # transpose the dataframe
                transformation_df = transformation_df.T
                # display the dataframe
                st.dataframe(transformation_df, use_container_width=True)


        # Feature Engineering
        st.write('---')
        st.subheader('Feature Engineering')
        # -- Feature Grouping --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Feature Grouping')
            col1, col2 = st.columns(2)
            with col1:
                # polynomial_features selectbox (False, True)
                st.selectbox('Polynomial Features', ['False', 'True'], help='Create polynomial features', key='polynomial_features')
                # polynomial_degree slider (int)
                if st.session_state['polynomial_features'] == 'True':
                    st.slider('Polynomial Degree', min_value=2, max_value=5, value=2, step=1, help='Degree of polynomial features', key='polynomial_degree')
                else:
                    st.slider('Polynomial Degree', min_value=2, max_value=5, value=2, step=1, help='Degree of polynomial features', key='polynomial_degree', disabled=True)

                # Group Features multi-select (dataframe columns, cannot be target variable, default is None)
                st.multiselect('Group Features', df.columns, help='Group features into a higher-level feature using mean, median, variance, and std', key='group_features')

                # bin_numeric_features multi-select (dataframe columns, cannot be target variable, default is None, must be numeric features)
                st.multiselect('Bin Numeric Features', df.columns, help='Bin numeric features into categorical features', key='bin_numeric_features')
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for feature grouping
                feature_grouping_df = pd.DataFrame({
                    'Polynomial Features': [st.session_state['polynomial_features']],
                    'Polynomial Degree': [st.session_state['polynomial_degree']],
                    'Group Features': [st.session_state['group_features']],
                    'Bin Numeric Features': [st.session_state['bin_numeric_features']]
                })
                # transpose the dataframe
                feature_grouping_df = feature_grouping_df.T
                # display the dataframe
                st.dataframe(feature_grouping_df, use_container_width=True)


        # Feature Selection
        st.write('---')
        st.subheader('Feature Selection')
        # -- Feature Selection --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Feature Importance Selection')
            col1, col2 = st.columns(2)
            with col1:
                # feature_selection selectbox (False, True)
                st.selectbox('Feature Selection', ['False', 'True'], help='Perform feature selection', key='feature_selection')
                # feature_selection_method selectbox (classic, univariate, sequential)
                if st.session_state['feature_selection'] == 'True':
                    st.selectbox('Feature Selection Method', ['classic', 'univariate', 'sequential'], help='Method to perform feature selection', key='feature_selection_method')
                else:
                    st.selectbox('Feature Selection Method', ['classic', 'univariate', 'sequential'], help='Method to perform feature selection', key='feature_selection_method', disabled=True)
                # n_features_to_select slider (int or float) default = 0.2
                if st.session_state['feature_selection'] == 'True':
                    st.slider('Number of Features to Select', min_value=0.1, max_value=1.0, value=0.2, step=0.1, help='Number of features to select', key='n_features_to_select')
                else:
                    st.slider('Number of Features to Select', min_value=0.1, max_value=1.0, value=0.2, step=0.1, help='Number of features to select', key='n_features_to_select', disabled=True)
                with col2:
                    st.info('Current Settings')
                    # create a dataframe that contain the settings for feature selection
                    feature_selection_df = pd.DataFrame({
                        'Feature Selection': [st.session_state['feature_selection']],
                        'Feature Selection Method': [st.session_state['feature_selection_method']],
                        'Number of Features to Select': [st.session_state['n_features_to_select']]
                    })
                    # transpose the dataframe
                    feature_selection_df = feature_selection_df.T
                    # display the dataframe
                    st.dataframe(feature_selection_df, use_container_width=True)


        # -- Remove Multicollinearity and Ignore Low Variance --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Remove Multicollinearity and Ignore Low Variance')
            col1, col2 = st.columns(2)
            with col1:
                # remove_multicollinearity selectbox (False, True)
                st.selectbox('Remove Multicollinearity', ['False', 'True'], help='Remove multicollinearity from the dataset', key='remove_multicollinearity')
                # multicollinearity_threshold slider (int or float) default = 0.9
                if st.session_state['remove_multicollinearity'] == 'True':
                    st.slider('Multicollinearity Threshold', min_value=0.1, max_value=1.0, value=0.9, step=0.1, help='Threshold to remove multicollinearity', key='multicollinearity_threshold')
                else:
                    st.slider('Multicollinearity Threshold', min_value=0.1, max_value=1.0, value=0.9, step=0.1, help='Threshold to remove multicollinearity', key='multicollinearity_threshold', disabled=True)
                # low_variance_threshold slider (int or float) default = 0
                st.slider('Low Variance Threshold', min_value=0.0, max_value=1.0, value=0.0, step=0.1, help='Threshold to remove low variance features', key='low_variance_threshold')
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for multicollinearity and low variance
                multicollinearity_low_variance_df = pd.DataFrame({
                    'Remove Multicollinearity': [st.session_state['remove_multicollinearity']],
                    'Multicollinearity Threshold': [st.session_state['multicollinearity_threshold']],
                    'Low Variance Threshold': [st.session_state['low_variance_threshold']]
                })
                # transpose the dataframe
                multicollinearity_low_variance_df = multicollinearity_low_variance_df.T
                # display the dataframe
                st.dataframe(multicollinearity_low_variance_df, use_container_width=True)


        # -- PCA --
        # create a 2 column
        with st.container(border=True):
            st.subheader('PCA')
            col1, col2 = st.columns(2)
            with col1:
                # pca selectbox (False, True)
                st.selectbox('PCA', ['False', 'True'], help='Perform PCA', key='pca')
                # pca_method selectbox (linear, kernel, incremental)
                if st.session_state['pca'] == 'True':
                    st.selectbox('PCA Method', ['linear', 'kernel', 'incremental'], help='Method to perform PCA', key='pca_method')
                else:
                    st.selectbox('PCA Method', ['linear', 'kernel', 'incremental'], help='Method to perform PCA', key='pca_method', disabled=True)
                # pca_components slider (int or float) default = 0.99
                if st.session_state['pca'] == 'True':
                    st.slider('PCA Components', min_value=0.1, max_value=1.0, value=0.99, step=0.1, help='Number of components to keep', key='pca_components')
                else:
                    st.slider('PCA Components', min_value=0.1, max_value=1.0, value=0.99, step=0.1, help='Number of components to keep', key='pca_components', disabled=True)
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for PCA
                pca_df = pd.DataFrame({
                    'PCA': [st.session_state['pca']],
                    'PCA Method': [st.session_state['pca_method']],
                    'PCA Components': [st.session_state['pca_components']]
                })
                # transpose the dataframe
                pca_df = pca_df.T
                # display the dataframe
                st.dataframe(pca_df, use_container_width=True)


        # -- Ignore Features --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Ignore Features')
            col1, col2 = st.columns(2)
            with col1:
                # ignore_features multi-select (dataframe columns, cannot be target variable, default is None)
                st.multiselect('Ignore Features', df.columns, help='Ignore features during preprocessing and training', key='ignore_features')
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for ignore features
                ignore_features_df = pd.DataFrame({
                    'Ignore Features': [st.session_state['ignore_features']]
                })
                # transpose the dataframe
                ignore_features_df = ignore_features_df.T
                # display the dataframe
                st.dataframe(ignore_features_df, use_container_width=True)


        # Model Selection
        st.write('---')
        st.subheader('Model Selection')
        # -- Train Test Split --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Train Test Split')
            col1, col2 = st.columns(2)
            with col1:
                # train_size slider (int or float) default = 0.7
                st.slider('Train Size', min_value=0.1, max_value=0.9, value=0.7, step=0.1, help='Percentage of data to use for training', key='train_size')
                # data_split_shuffle selectbox (True, False)
                st.selectbox('Data Split Shuffle', ['True', 'False'], help='Shuffle the dataset before splitting', key='data_split_shuffle')
                # data_split_stratify selectbox (True, False)
                st.selectbox('Data Split Stratify', ['True', 'False'], help='Stratify the dataset before splitting', key='data_split_stratify')
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for train test split
                train_test_split_df = pd.DataFrame({
                    'Train Size': [st.session_state['train_size']],
                    'Data Split Shuffle': [st.session_state['data_split_shuffle']],
                    'Data Split Stratify': [st.session_state['data_split_stratify']]
                })
                # transpose the dataframe
                train_test_split_df = train_test_split_df.T
                # display the dataframe
                st.dataframe(train_test_split_df, use_container_width=True)


        # -- Fold Strategy --
        # create a 2 column
        with st.container(border=True):
            st.subheader('Fold Strategy')
            col1, col2 = st.columns(2)
            with col1:
                # fold_strategy selectbox (stratifiedkfold, kfold)
                st.selectbox('Fold Strategy', ['stratifiedkfold', 'kfold'], help='Method to split the dataset into folds', key='fold_strategy')
                # fold selectbox (int) default = 10
                st.slider('Number of Folds', min_value=2, max_value=10, value=10, step=1, help='Number of folds to create', key='fold')
                # fold_shuffle selectbox (True, False)
                st.selectbox('Fold Shuffle', ['False', 'True'], help='Shuffle the dataset before splitting', key='fold_shuffle')
            with col2:
                st.info('Current Settings')
                # create a dataframe that contain the settings for fold strategy
                fold_strategy_df = pd.DataFrame({
                    'Fold Strategy': [st.session_state['fold_strategy']],
                    'Number of Folds': [st.session_state['fold']],
                    'Fold Shuffle': [st.session_state['fold_shuffle']]
                })
                # transpose the dataframe
                fold_strategy_df = fold_strategy_df.T
                # display the dataframe
                st.dataframe(fold_strategy_df, use_container_width=True)


        # Overall Settings
        st.write('---')
        st.subheader('Overall Settings')
        # Combine all the settings into a single dataframe, separating each section with a column of NaN
        overall_settings_df = pd.concat([missing_values_imputation_df, target_imbalance_outlier_df, normalization_df, transformation_df, feature_grouping_df, feature_selection_df, multicollinearity_low_variance_df, pca_df, ignore_features_df, train_test_split_df, fold_strategy_df])
        st.session_state['overall_settings'] = overall_settings_df
        # display the dataframe
        st.dataframe(st.session_state['overall_settings'], use_container_width=True)


# 3. Model Training Section
# - This section is used to train a model
# - The user can select the problem type (classification, regression, clustering)
# - The user can select the mode (AutoML, Manual Mode)
# - The user can select the target variable
# - The user can run AutoML
# - The user can view the ML settings, model comparison, and model interpretation
if selected == 'Train Model':
    if(st.session_state['input_dataframe_page2'].empty == True):
        st.error('Error: Input file not found!')
    elif(st.session_state['overall_settings'] is None):
        st.error('Error: Data Preprocessing has not been done! Go to Data Preprocessing to initialize the settings.')
    else:
        st.session_state['train_model_accessed'] = True
        # Display Input Dataframe
        st.header('Train a Model')
        df = st.session_state['input_dataframe_page2']
        st.dataframe(df, use_container_width=True)

        # Display Overall Settings
        st.subheader('Overall Settings')
        st.dataframe(st.session_state['overall_settings'], use_container_width=True)

        # Select Problem Type
        problem_type = st.selectbox('Select Problem Type', ['Classification', 'Regression', 'Clustering'])
        st.write('''---''')

        if problem_type == 'Classification':
            st.header('Classification')
            # -- Problem Definition --
            # create a 2 column
            with st.container(border=True):
                st.subheader('Problem Definition')
                col1, col2 = st.columns(2)
                with col1:
                    # target_variable selectbox (dataframe columns, cannot be index)
                    st.selectbox('Target Variable', df.columns, help='Target variable to predict', key='target')
                with col2:
                    # create a dataframe that contain the settings for problem definition
                    problem_definition_df = pd.DataFrame({
                        'Target Variable': [st.session_state['target']]
                    })
                    # transpose the dataframe
                    problem_definition_df = problem_definition_df.T
                    # display the dataframe
                    st.dataframe(problem_definition_df, use_container_width=True)
                    # button to run setup with all data preprocessing settings
                    if st.button('Run Setup'):
                        with st.spinner('Running Setup...'):
                            # create a new dataframe that uses the key name as columns for the settings
                            classification_settings_df = pd.DataFrame({
                                'preprocess': True,
                                'imputation_type': [st.session_state['overall_settings'][0][0]],
                                'numeric_imputation': [st.session_state['overall_settings'][0][1]],
                                'categorical_imputation': [st.session_state['overall_settings'][0][2]],
                                'iterative_imputation_iters': [st.session_state['overall_settings'][0][3]],
                                'fix_imbalance': [st.session_state['overall_settings'][0][4]],
                                'fix_imbalance_method': [st.session_state['overall_settings'][0][5]],
                                'remove_outliers': [st.session_state['overall_settings'][0][6]],
                                'outliers_method': [st.session_state['overall_settings'][0][7]],
                                'outliers_threshold': [st.session_state['overall_settings'][0][8]],
                                'normalize': [st.session_state['overall_settings'][0][9]],
                                'normalize_method': [st.session_state['overall_settings'][0][10]],
                                'transformation': [st.session_state['overall_settings'][0][11]],
                                'transformation_method': [st.session_state['overall_settings'][0][12]],
                                'polynomial_features': [st.session_state['overall_settings'][0][15]],
                                'polynomial_degree': [st.session_state['overall_settings'][0][16]],
                                'group_features': [st.session_state['overall_settings'][0][17]],
                                'bin_numeric_features': [st.session_state['overall_settings'][0][18]],
                                'feature_selection': [st.session_state['overall_settings'][0][19]],
                                'feature_selection_method': [st.session_state['overall_settings'][0][20]],
                                'n_features_to_select': [st.session_state['overall_settings'][0][21]],
                                'remove_multicollinearity': [st.session_state['overall_settings'][0][22]],
                                'multicollinearity_threshold': [st.session_state['overall_settings'][0][23]],
                                'low_variance_threshold': [st.session_state['overall_settings'][0][24]],
                                'pca': [st.session_state['overall_settings'][0][25]],
                                'pca_method': [st.session_state['overall_settings'][0][26]],
                                'pca_components': [st.session_state['overall_settings'][0][27]],
                                'ignore_features': [st.session_state['overall_settings'][0][28]],
                                'train_size': [st.session_state['overall_settings'][0][29]],
                                'data_split_shuffle': [st.session_state['overall_settings'][0][30]],
                                'data_split_stratify': [st.session_state['overall_settings'][0][31]],
                                'fold_strategy': [st.session_state['overall_settings'][0][32]],
                                'fold': [st.session_state['overall_settings'][0][33]],
                            })

                            # Run setup and store the output from terminal to a variable
                            pycaret_classification.setup(data=df, target=st.session_state['target'], **classification_settings_df.to_dict('records')[0])
                            setup_df = pycaret_classification.pull()
                            st.success('Setup Complete!')
                            st.session_state['classification_setup'] = setup_df
                    # print out the clf configuration
                    if st.session_state['classification_setup'] is not None:
                        st.dataframe(st.session_state['classification_setup'], use_container_width=True)

            
            # -- Model Training --
            if st.session_state['classification_setup'] is not None:
                # create a 2 column
                with st.container(border=True):
                    st.subheader('Model Training')
                    with st.expander(label='Available Models', expanded=False):
                        st.write(pycaret_classification.models())
                    col1, col2 = st.columns(2)
                    with col1:
                        # include multiselect (models to include, default is all models)
                        st.multiselect('Included Models', pycaret_classification.models().index.tolist(), help='Models to include in training', key='include_models', max_selections=5, default=None)
                        # n_select slider (int) default = 1
                        st.slider('Number of Models to Select', min_value=1, max_value=5, value=1, step=1, help='Number of models to select and train', key='n_select')
                    with col2:
                        # create a dataframe that contain the settings for model training
                        model_training_df = pd.DataFrame({
                            'Included Models': [st.session_state['include_models']],
                            'Number of Models to Select': [st.session_state['n_select']]
                        })
                        # transpose the dataframe
                        model_training_df = model_training_df.T
                        # display the dataframe
                        st.dataframe(model_training_df, use_container_width=True)
                        # button to run compare_models
                        if st.button('Run Training'):
                            with st.spinner('Training...'):
                                classification_models = pycaret_classification.compare_models(include=st.session_state['include_models'], n_select=st.session_state['n_select'])
                                st.success('Training Complete!')
                                # print out the comparison 
                                comparison_df = pycaret_classification.pull()
                                st.session_state['classification_comparison_df'] = comparison_df
                                st.session_state['classification_models'] = classification_models

                        if st.session_state['classification_comparison_df'] is not None:
                            st.dataframe(st.session_state['classification_comparison_df'], use_container_width=True)
                                

        
            # -- Model Download --
            if st.session_state['classification_models'] is not None:
                with st.container(border=True):
                    st.subheader('Model Download')
                    # loop through the models and display the hyperparameter tuning settings
                    # check if the model is a list or not
                    if type(st.session_state['classification_models']) == list:
                        i = 0
                        for model in st.session_state['classification_models']:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f'Model {i}: {model}')
                            with col2:
                                if st.button('Generate Download Link', key=f'download_link_{i}'):
                                    file_name = 'temp_files/' + st.session_state['username'] + '_model_' + str(i)
                                    # create a temporary file to store the model
                                    pycaret_classification.save_model(model, file_name)
                                    with open(file_name + '.pkl', 'rb') as f:
                                        model_data = io.BytesIO(f.read())
                                    # download the model for the user
                                    st.download_button(label='Download Model', data=model_data, file_name='model.pkl')
                            i += 1
                    else:
                        model = st.session_state['classification_models']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f'Model 0: {model}')
                        with col2:
                            if st.button('Generate Download Link', key=f'download_link_0'):
                                file_name = 'temp_files/' + st.session_state['username'] + '_model_0'
                                # create a temporary file to store the model
                                pycaret_classification.save_model(model, file_name)
                                with open(file_name + '.pkl', 'rb') as f:
                                    model_data = io.BytesIO(f.read())
                                # download the model for the user
                                st.download_button(label='Download Model', data=model_data, file_name='model.pkl')

        
        if problem_type == 'Regression':
            st.header('Regression')
            # -- Problem Definition --
            # create a 2 column
            with st.container(border=True):
                st.subheader('Problem Definition')
                col1, col2 = st.columns(2)
                with col1:
                    # target_variable selectbox (dataframe columns, cannot be index)
                    st.selectbox('Target Variable', df.columns, help='Target variable to predict', key='target')
                with col2:
                    # create a dataframe that contain the settings for problem definition
                    problem_definition_df = pd.DataFrame({
                        'Target Variable': [st.session_state['target']]
                    })
                    # transpose the dataframe
                    problem_definition_df = problem_definition_df.T
                    # display the dataframe
                    st.dataframe(problem_definition_df, use_container_width=True)
                    # button to run setup with all data preprocessing settings
                    if st.button('Run Setup'):
                        with st.spinner('Running Setup...'):
                            # create a new dataframe that uses the key name as columns for the settings
                            regression_settings_df = pd.DataFrame({
                                'preprocess': True,
                                'imputation_type': [st.session_state['overall_settings'][0][0]],
                                'numeric_imputation': [st.session_state['overall_settings'][0][1]],
                                'categorical_imputation': [st.session_state['overall_settings'][0][2]],
                                'iterative_imputation_iters': [st.session_state['overall_settings'][0][3]],
                                'remove_outliers': [st.session_state['overall_settings'][0][6]],
                                'outliers_method': [st.session_state['overall_settings'][0][7]],
                                'outliers_threshold': [st.session_state['overall_settings'][0][8]],
                                'normalize': [st.session_state['overall_settings'][0][9]],
                                'normalize_method': [st.session_state['overall_settings'][0][10]],
                                'transformation': [st.session_state['overall_settings'][0][11]],
                                'transformation_method': [st.session_state['overall_settings'][0][12]],
                                'transform_target': [st.session_state['overall_settings'][0][13]],
                                'transform_target_method': [st.session_state['overall_settings'][0][14]],
                                'polynomial_features': [st.session_state['overall_settings'][0][15]],
                                'polynomial_degree': [st.session_state['overall_settings'][0][16]],
                                'group_features': [st.session_state['overall_settings'][0][17]],
                                'bin_numeric_features': [st.session_state['overall_settings'][0][18]],
                                'feature_selection': [st.session_state['overall_settings'][0][19]],
                                'feature_selection_method': [st.session_state['overall_settings'][0][20]],
                                'n_features_to_select': [st.session_state['overall_settings'][0][21]],
                                'remove_multicollinearity': [st.session_state['overall_settings'][0][22]],
                                'multicollinearity_threshold': [st.session_state['overall_settings'][0][23]],
                                'low_variance_threshold': [st.session_state['overall_settings'][0][24]],
                                'pca': [st.session_state['overall_settings'][0][25]],
                                'pca_method': [st.session_state['overall_settings'][0][26]],
                                'pca_components': [st.session_state['overall_settings'][0][27]],
                                'ignore_features': [st.session_state['overall_settings'][0][28]],
                                'train_size': [st.session_state['overall_settings'][0][29]],
                                'data_split_shuffle': [st.session_state['overall_settings'][0][30]],
                                'data_split_stratify': [st.session_state['overall_settings'][0][31]],
                                'fold_strategy': [st.session_state['overall_settings'][0][32]],
                                'fold': [st.session_state['overall_settings'][0][33]],
                            })

                            # Run setup and store the output from terminal to a variable
                            pycaret_regression.setup(data=df, target=st.session_state['target'], **regression_settings_df.to_dict('records')[0])
                            setup_df = pycaret_regression.pull()
                            st.success('Setup Complete!')
                            st.session_state['regression_setup'] = setup_df
                    # print out the clf configuration
                    if st.session_state['regression_setup'] is not None:
                        st.dataframe(st.session_state['regression_setup'], use_container_width=True)

            
            # -- Model Training --
            if st.session_state['regression_setup'] is not None:
                # create a 2 column
                with st.container(border=True):
                    st.subheader('Model Training')
                    with st.expander(label='Available Models', expanded=False):
                        st.write(pycaret_regression.models())
                    col1, col2 = st.columns(2)
                    with col1:
                        # include multiselect (models to include, default is all models)
                        st.multiselect('Included Models', pycaret_regression.models().index.tolist(), help='Models to include in training', key='regression_include_models', max_selections=5, default=None)
                        # n_select slider (int) default = 1
                        st.slider('Number of Models to Select', min_value=1, max_value=5, value=1, step=1, help='Number of models to select and train', key='regression_n_select')
                    with col2:
                        # create a dataframe that contain the settings for model training
                        model_training_df = pd.DataFrame({
                            'Included Models': [st.session_state['regression_include_models']],
                            'Number of Models to Select': [st.session_state['regression_n_select']]
                        })
                        # transpose the dataframe
                        model_training_df = model_training_df.T
                        # display the dataframe
                        st.dataframe(model_training_df, use_container_width=True)
                        # button to run compare_models
                        if st.button('Run Training'):
                            with st.spinner('Training...'):
                                classification_models = pycaret_regression.compare_models(include=st.session_state['regression_include_models'], n_select=st.session_state['regression_n_select'])
                                st.success('Training Complete!')
                                # print out the comparison 
                                comparison_df = pycaret_regression.pull()
                                st.session_state['regression_comparison_df'] = comparison_df
                                st.session_state['regression_models'] = classification_models

                        if st.session_state['regression_comparison_df'] is not None:
                            st.dataframe(st.session_state['regression_comparison_df'], use_container_width=True)
                                

        
            # -- Model Download --
            if st.session_state['regression_models'] is not None:
                with st.container(border=True):
                    st.subheader('Model Download')
                    # loop through the models and display the hyperparameter tuning settings
                    # check if the model is a list or not
                    if type(st.session_state['regression_models']) == list:
                        i = 0
                        for model in st.session_state['regression_models']:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f'Model {i}: {model}')
                            with col2:
                                if st.button('Generate Download Link', key=f'download_link_{i}'):
                                    file_name = 'temp_files/' + st.session_state['username'] + '_model_' + str(i)
                                    # create a temporary file to store the model
                                    pycaret_regression.save_model(model, file_name)
                                    with open(file_name + '.pkl', 'rb') as f:
                                        model_data = io.BytesIO(f.read())
                                    # download the model for the user
                                    st.download_button(label='Download Model', data=model_data, file_name='model.pkl')
                            i += 1
                    else:
                        model = st.session_state['regression_models']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f'Model 0: {model}')
                        with col2:
                            if st.button('Generate Download Link', key=f'download_link_0'):
                                file_name = 'temp_files/' + st.session_state['username'] + '_model_' + str(i)
                                # create a temporary file to store the model
                                pycaret_regression.save_model(model, file_name)
                                with open(file_name + '.pkl', 'rb') as f:
                                        model_data = io.BytesIO(f.read())
                                # download the model for the user
                                st.download_button(label='Download Model', data=model_data, file_name='model.pkl')


        if problem_type == 'Clustering':
            st.header('Clustering')
            # -- Problem Definition --
            # create a 2 column
            with st.container(border=True):
                st.subheader('Problem Definition')
                col1, col2 = st.columns(2)
                with col1:
                    # target_variable selectbox (dataframe columns, cannot be index)
                    st.selectbox('Target Variable', df.columns, help='Target variable to predict', key='target', disabled=True)
                with col2:
                    # Info about clustering
                    st.info('Clustering does not require a target variable.')
                    
                    # button to run setup with all data preprocessing settings
                    if st.button('Run Setup'):
                        with st.spinner('Running Setup...'):
                            # create a new dataframe that uses the key name as columns for the settings
                            clustering_settings_df = pd.DataFrame({
                                'preprocess': True,
                                'imputation_type': [st.session_state['overall_settings'][0][0]],
                                'numeric_imputation': [st.session_state['overall_settings'][0][1]],
                                'categorical_imputation': [st.session_state['overall_settings'][0][2]],
                                'remove_outliers': [st.session_state['overall_settings'][0][6]],
                                'outliers_method': [st.session_state['overall_settings'][0][7]],
                                'outliers_threshold': [st.session_state['overall_settings'][0][8]],
                                'normalize': [st.session_state['overall_settings'][0][9]],
                                'normalize_method': [st.session_state['overall_settings'][0][10]],
                                'transformation': [st.session_state['overall_settings'][0][11]],
                                'transformation_method': [st.session_state['overall_settings'][0][12]],
                                'polynomial_features': [st.session_state['overall_settings'][0][15]],
                                'polynomial_degree': [st.session_state['overall_settings'][0][16]],
                                'bin_numeric_features': [st.session_state['overall_settings'][0][18]],
                                'remove_multicollinearity': [st.session_state['overall_settings'][0][22]],
                                'multicollinearity_threshold': [st.session_state['overall_settings'][0][23]],
                                'low_variance_threshold': [st.session_state['overall_settings'][0][24]],
                                'pca': [st.session_state['overall_settings'][0][25]],
                                'pca_method': [st.session_state['overall_settings'][0][26]],
                                'pca_components': [st.session_state['overall_settings'][0][27]],
                                'ignore_features': [st.session_state['overall_settings'][0][28]],
                            })

                            # Run setup and store the output from terminal to a variable
                            pycaret_clustering.setup(data=df)
                            setup_df = pycaret_clustering.pull()
                            st.success('Setup Complete!')
                            st.session_state['clustering_setup'] = setup_df
                    # print out the clf configuration
                    if st.session_state['clustering_setup'] is not None:
                        st.dataframe(st.session_state['clustering_setup'], use_container_width=True)


            # -- Model Training --
            if st.session_state['clustering_setup'] is not None:
                # create a 2 column
                with st.container(border=True):
                    st.subheader('Model Training')
                    with st.expander(label='Available Models', expanded=False):
                        st.write(pycaret_clustering.models())
                    col1, col2 = st.columns(2)
                    with col1:
                        # include multiselect (models to include, default is all models)
                        st.multiselect('Included Models', pycaret_clustering.models().index.tolist(), help='Models to include in training', key='clustering_include_models', max_selections=1, default=None)
                        # n_select slider (int) default = 1
                        st.slider('Number of Models to Select', min_value=1, max_value=5, value=1, step=1, help='Number of models to select and train', key='clustering_n_select', disabled=True)
                        if st.session_state['clustering_include_models'] == ['kmeans']:
                            # slider for k (int) default = 4
                            st.slider('Number of Clusters', min_value=2, max_value=10, value=4, step=1, help='Number of clusters to create', key='k')
                    with col2:
                        # create a dataframe that contain the settings for model 
                        if st.session_state['clustering_include_models'] == ['kmeans']:
                            model_training_df = pd.DataFrame({
                                'Included Models': [st.session_state['clustering_include_models']],
                                'Number of Models to Select': [st.session_state['clustering_n_select']],
                                'Number of Clusters': [st.session_state['k']]
                            })
                        else:
                            model_training_df = pd.DataFrame({
                                'Included Models': [st.session_state['clustering_include_models']],
                                'Number of Models to Select': [st.session_state['clustering_n_select']]
                            })
                        # transpose the dataframe
                        model_training_df = model_training_df.T
                        # display the dataframe
                        st.dataframe(model_training_df, use_container_width=True)
                        # button to run compare_models
                        if st.button('Run Training'):
                            with st.spinner('Training...'):
                                if st.session_state['clustering_include_models'] == ['kmeans']:
                                    classification_models = pycaret_clustering.create_model(st.session_state['clustering_include_models'][0], num_clusters=st.session_state['k'])
                                else:
                                    classification_models = pycaret_clustering.create_model(st.session_state['clustering_include_models'][0])
                                st.success('Training Complete!')
                                # print out the comparison
                                comparison_df = pycaret_clustering.pull()
                                st.session_state['clustering_comparison_df'] = comparison_df
                                st.session_state['clustering_models'] = classification_models

                        if st.session_state['clustering_comparison_df'] is not None:
                            st.dataframe(st.session_state['clustering_comparison_df'], use_container_width=True)


            # -- Model Overview --
            if st.session_state['clustering_models'] is not None:
                with st.container(border=True):
                    st.subheader('Model Overview')
                    st.write(f'Model: {st.session_state["clustering_models"]}')
                    st.dataframe(pycaret_clustering.assign_model(st.session_state['clustering_models']))
                    #extract the first 6 letters of the model name
                    clustering_model_name = f'{st.session_state["clustering_models"]}'
                    clustering_model_name = clustering_model_name[:6]
                    if clustering_model_name == 'KMeans':
                        elbow_plot = pycaret_clustering.plot_model(st.session_state['clustering_models'], plot='elbow', display_format='streamlit', save=True)
                        st.image(elbow_plot)


            # -- Model Download --
            if st.session_state['clustering_models'] is not None:
                with st.container(border=True):
                    st.subheader('Model Download')
                    model = st.session_state['clustering_models']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f'Model 0: {model}')
                    with col2:
                        if st.button('Generate Download Link', key=f'download_link_0'):
                            file_name = 'temp_files/' + st.session_state['username'] + '_model_0'
                            # create a temporary file to store the model
                            pycaret_clustering.save_model(model, file_name)
                            with open(file_name + '.pkl', 'rb') as f:
                                model_data = io.BytesIO(f.read())
                            # download the model for the user
                            st.download_button(label='Download Model', data=model_data, file_name='model.pkl')




if selected == 'Run Model':
    st.header('Run Model')
    inference_type = st.selectbox('Select Inference Type', ['Classification', 'Regression', 'Clustering'])
    inference_model = st.file_uploader('Choose a .pkl model', type=['pkl'])
    inference_input = st.file_uploader('Choose a .csv file', type=['csv'])

    if inference_model is not None and inference_input is not None:
        file_name = 'temp_files/' + st.session_state['username'] + '_model'
        # save the model to a temporary file
        with open(file_name + '.pkl', 'wb') as f:      
            f.write(inference_model.getvalue())

        input_df = pd.read_csv(inference_input)
        if inference_type == 'Classification':
            model = pycaret_classification.load_model(file_name)
            # make predictions
            predictions = pycaret_classification.predict_model(model, data=input_df)
            # display the predictions
            st.dataframe(predictions, use_container_width=True)
        elif inference_type == 'Regression':
            model = pycaret_classification.load_model(file_name)
            # make predictions
            predictions = pycaret_regression.predict_model(model, data=input_df)
            # display the predictions
            st.dataframe(predictions, use_container_width=True)
        elif inference_type == 'Clustering':
            model = pycaret_classification.load_model(file_name)
            try:
                predictions = pycaret_clustering.predict_model(model, data=input_df)
            except:
                predictions = pycaret_clustering.assign_model(model)
            # display the predictions
            st.dataframe(predictions, use_container_width=True)


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

