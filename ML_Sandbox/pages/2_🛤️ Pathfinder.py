import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
# ----
# Definition and Globals
# ----
# 1. Session States
# - input_dataframe_page1 is the dataframe that is uploaded by the user
# - last_input is the name of the last uploaded file
if 'input_dataframe_page1' not in st.session_state:
    st.session_state['input_dataframe_page1'] = pd.DataFrame()

if 'last_input' not in st.session_state:
    st.session_state['last_input'] = None


# 2. Graph Selector
# - This function is used to select the type of graph that the user wants to generate
def select_graph():
    selection = st.selectbox(label='Select: ', options=['Line Graph', 'Histogram', 'Bar Graph', 'Scatter Plot'])

    return selection


# 3. Line Graph Editor
# - This function is used to generate a line graph
# - The user can select the x-axis and y-axis variables
# - The user can also customize the graph by changing the title, labels, and colors
def line_graph(df: pd.DataFrame):
    # Add a horizontal line and a subheader in the Streamlit app
    st.write('---')
    st.subheader('Line Graph Editor')

    # Get a list of the column names in the DataFrame
    col_names = df.columns.tolist()
    col_names.append('Auto')

    # Create a 2-column layout
    col1, col2 = st.columns((1,2))

    # In the first column...
    with col1:
        # Create a 2-column layout
        col3, col4 = st.columns(2)
        # In the first column...
        with col3:
            # Create a dropdown menu for the x-axis variable
            X_val = st.selectbox('Select X-axis Variable', col_names)
            col_names2 = [item for item in col_names if item != X_val]
            X_label = st.text_input('Enter X-axis Label', value=X_val)
        # In the second column...
        with col4:
            # Create a dropdown menu for the y-axis variable
            Y_val = st.selectbox('Select Y-axis Variable', col_names2)
            Y_label = st.text_input('Enter Y-axis Label', value=Y_val)

        # Create a text input for the graph title
        title = st.text_input('Enter Graph Title', value='Graph')

        # Create 3 columns for the color pickers
        col5, col6, col7 = st.columns(3)
        with col5:
            line_color = st.color_picker('Line Color', value='#e18a6d')
        with col6:
            label_font_color = st.color_picker('Label Color', value='#FFFFFF')
        with col7:
            tick_font_color = st.color_picker('Tick Color', value='#FFFFFF')

        # Create a checkbox for the transparent background
        transparent_bg = st.checkbox('Transparent Background', value=False)

    # In the second column...
    with col2:
        # Create a line graph using Plotly Express
        if X_val != 'Auto' and Y_val != 'Auto':
            fig = px.line(df, x=X_val, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val == 'Auto' and Y_val != 'Auto':
            fig = px.line(df, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val != 'Auto' and Y_val == 'Auto':
            fig = px.line(df, x=X_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        else:
            st.write("Please select at least one axis variable.")
        
        # Custom color for the line
        fig.update_traces(line=dict(color=line_color))

        # Custom color for the background
        if transparent_bg:
            fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

        # Custom color for labels
        fig.update_layout(title_font=dict(color=label_font_color))
        fig.update_xaxes(title_text=X_label, title_font=dict(color=label_font_color))
        fig.update_yaxes(title_text=Y_label, title_font=dict(color=label_font_color))

        # Custom color for x and y-axis values
        fig.update_xaxes(tickfont=dict(color=tick_font_color))
        fig.update_yaxes(tickfont=dict(color=tick_font_color))

        # Display the graph in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)

    # Add a horizontal line in the Streamlit app
    st.write('---')

# 4. Histogram Editor
def histogram(df: pd.DataFrame):
    # Add a horizontal line and a subheader in the Streamlit app
    st.write('---')
    st.subheader('Histogram Editor')

    # Get a list of the column names in the DataFrame
    col_names = df.columns.tolist()
    col_names.append('Auto')

    # Create a 2-column layout
    col1, col2 = st.columns((1,2))

    # In the first column...
    with col1:
        # Select the variable
        X_val = st.selectbox('Select Variable', col_names)
        X_label = st.text_input('Enter Variable Label', value=X_val)

        # Create a text input for the graph title
        title = st.text_input('Enter Graph Title', value='Graph')

        # Create 3 columns for the color pickers
        col5, col6, col7 = st.columns(3)
        with col5:
            plot_color = st.color_picker('Plot Color', value='#e18a6d')
        with col6:
            label_font_color = st.color_picker('Label Color', value='#FFFFFF')
        with col7:
            tick_font_color = st.color_picker('Tick Color', value='#FFFFFF')

        # Create a checkbox for the transparent background
        transparent_bg = st.checkbox('Transparent Background', value=False)

    # In the second column...
    with col2:
        # Create a histogram using Plotly Express
        if X_val != 'Auto':
            fig = px.histogram(df, x=X_val, title=title, labels={X_val: X_label}, color_discrete_sequence=[plot_color])
        else:
            st.write("Please select at least one axis variable.")
        
        # Custom color for the background
        if transparent_bg:
            fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

        # Custom color for labels
        fig.update_layout(title_font=dict(color=label_font_color))
        fig.update_xaxes(title_text=X_label, title_font=dict(color=label_font_color))
        fig.update_yaxes(title_font=dict(color=label_font_color))

        # Custom color for x and y-axis values
        fig.update_xaxes(tickfont=dict(color=tick_font_color))
        fig.update_yaxes(tickfont=dict(color=tick_font_color))

        # Display the graph in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)
    

# 5. Bar Graph Editor
# - This function is used to generate a bar graph
# - The user can select the x-axis and y-axis variables
# - The user can also customize the graph by changing the title, labels, and colors
def bar_graph(df: pd.DataFrame):
    # Add a horizontal line and a subheader in the Streamlit app
    st.write('---')
    st.subheader('Bar Graph Editor')

    # Get a list of the column names in the DataFrame
    col_names = df.columns.tolist()
    col_names.append('Auto')

    # Create a 2-column layout
    col1, col2 = st.columns((1,2))

    # In the first column...
    with col1:
        # Create a 2-column layout
        col3, col4 = st.columns(2)
        # In the first column...
        with col3:
            # Create a dropdown menu for the x-axis variable
            X_val = st.selectbox('Select X-axis Variable', col_names)
            col_names2 = [item for item in col_names if item != X_val]
            X_label = st.text_input('Enter X-axis Label', value=X_val)
        # In the second column...
        with col4:
            # Create a dropdown menu for the y-axis variable
            Y_val = st.selectbox('Select Y-axis Variable', col_names2)
            Y_label = st.text_input('Enter Y-axis Label', value=Y_val)

        # Create a text input for the graph title
        title = st.text_input('Enter Graph Title', value='Graph')

        # Create 3 columns for the color pickers
        col5, col6, col7 = st.columns(3)
        with col5:
            bar_color = st.color_picker('Bar Color', value='#e18a6d')
        with col6:
            label_font_color = st.color_picker('Label Color', value='#FFFFFF')
        with col7:
            tick_font_color = st.color_picker('Tick Color', value='#FFFFFF')
        transparent_bg = st.checkbox('Transparent Background', value=False)

    # In the second column...
    with col2:
        # Create a bar graph using Plotly Express
        if X_val != 'Auto' and Y_val != 'Auto':
            fig = px.bar(df, x=X_val, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val == 'Auto' and Y_val != 'Auto':
            fig = px.bar(df, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val != 'Auto' and Y_val == 'Auto':
            fig = px.bar(df, x=X_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        else:
            st.write("Please select at least one axis variable.")

        # Custom color for the bars
        fig.update_traces(marker=dict(color=bar_color),
                  selector=dict(type="bar"))
        
        # Custom color for the background
        if transparent_bg:
            fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

        # Custom color for labels
        fig.update_layout(title_font=dict(color=label_font_color))
        fig.update_xaxes(title_text=X_label, title_font=dict(color=label_font_color))
        fig.update_yaxes(title_text=Y_label, title_font=dict(color=label_font_color))

        # Custom color for x and y-axis values
        fig.update_xaxes(tickfont=dict(color=tick_font_color))
        fig.update_yaxes(tickfont=dict(color=tick_font_color))

        # Display the graph in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)

    # Add a horizontal line in the Streamlit app
    st.write('---')

# 6. Scatter Plot Editor
# - This function is used to generate a scatter plot
# - The user can select the x-axis and y-axis variables
# - The user can also customize the graph by changing the title, labels, and colors
def scatter_plot(df: pd.DataFrame):
    # Add a horizontal line and a subheader in the Streamlit app
    st.write('---')
    st.subheader('Scatter Plot Editor')

    # Get a list of the column names in the DataFrame
    col_names = df.columns.tolist()
    col_names.append('Auto')

    # Create a 2-column layout
    col1, col2 = st.columns((1,2))

    # In the first column...
    with col1:
        # Create a 2-column layout
        col3, col4 = st.columns(2)
        # In the first column...
        with col3:
            # Create a dropdown menu for the x-axis variable
            X_val = st.selectbox('Select X-axis Variable', col_names)
            col_names2 = [item for item in col_names if item != X_val]
            X_label = st.text_input('Enter X-axis Label', value=X_val)
        # In the second column...
        with col4:
            # Create a dropdown menu for the y-axis variable
            Y_val = st.selectbox('Select Y-axis Variable', col_names2)
            Y_label = st.text_input('Enter Y-axis Label', value=Y_val)

        # Create a text input for the graph title
        title = st.text_input('Enter Graph Title', value='Graph')

        # Create 3 columns for the color pickers
        col5, col6, col7 = st.columns(3)
        with col5:
            plot_color = st.color_picker('Plot Color', value='#e18a6d')
        with col6:
            label_font_color = st.color_picker('Label Color', value='#FFFFFF')
        with col7:
            tick_font_color = st.color_picker('Tick Color', value='#FFFFFF')
        transparent_bg = st.checkbox('Transparent Background', value=False)

    # In the second column...
    with col2:
        # Create a scatter plot using Plotly Express
        if X_val != 'Auto' and Y_val != 'Auto':
            fig = px.scatter(df, x=X_val, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val == 'Auto' and Y_val != 'Auto':
            fig = px.scatter(df, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val != 'Auto' and Y_val == 'Auto':
            fig = px.scatter(df, x=X_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        else:
            st.write("Please select at least one axis variable.")
        
        # Custom color for the plot
        fig.update_traces(marker=dict(color=plot_color),
                  selector=dict(type="scatter"))
        
        # Custom color for the background
        if transparent_bg:
            fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

        # Custom color for labels
        fig.update_layout(title_font=dict(color=label_font_color))
        fig.update_xaxes(title_text=X_label, title_font=dict(color=label_font_color))
        fig.update_yaxes(title_text=Y_label, title_font=dict(color=label_font_color))

        # Custom color for x and y-axis values
        fig.update_xaxes(tickfont=dict(color=tick_font_color))
        fig.update_yaxes(tickfont=dict(color=tick_font_color))

        # Display the graph in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)

    # Add a horizontal line in the Streamlit app
    st.write('---')


# 7. Download Section
def download():
    st.subheader('Downloading Figures')
    st.write('''
1. Data Table can be downloaded as .csv file by clicking on the download button on the top right corner of the table.
2. Graphs can also be downloaded as .png files by clicking on the camera icon on the top right corner of the graph. This applies to all graph generated on this page.
''')
    st.subheader('Downloading Reports')
    st.write('''
1. To download the report from the Data Explorer, you can click on the hamburger icon on the top right corner of the page and click print. This will allow you to save the whole page as a pdf file.
''')


# 8. Tutorial Section
def tutorial_section():
    with st.expander('Tutorial'):
        st.markdown("""
    # Pathfinder Tutorial

    ## Overview
    Pathfinder is a tool for visualizing and analyzing your data. It provides several types of graphs, including line graphs, pie charts, bar graphs, and scatter plots.

    ## How to Use

    1. **Select a Graph Type**: Use the dropdown menu to select the type of graph you want to create. The options are 'Line Graph', 'Pie Chart', 'Bar Graph', and 'Scatter Plot'.

    2. **Select Axis Variables**: Depending on the type of graph, you may need to select one or more variables for the x and/or y axes. If you don't select any variables, you'll see a message asking you to select at least one.

    3. **Customize Your Graph**: You can customize the background color, label color, and tick color of your graph. If you want a transparent background, check the 'Transparent Background' box.

    4. **Generate Your Graph**: Click the 'Generate Graph' button to create your graph. The graph will appear below the button.

    ## Tips
    - If you're not sure which variables to select for your graph, try different combinations to see what gives you the most insight into your data.
    - If you don't want to manually select variables, you can use our Data Explorer tool to automatically generate useful graphs and statistics for your data.

    Happy data exploring!
    """)
        

# ----
# Page Config
# ----
st.set_page_config(
    page_title='Make Your Graphs!',
    page_icon='🚀',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

# ----
# Topbar
# ----
selected = option_menu(
    menu_title= "Pathfinder",
    options=['Upload', 'Graph Generator', 'Data Explorer','Download'],
    orientation="horizontal",
    menu_icon="compass",
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
        st.session_state['input_dataframe_page1'] = df
        st.session_state['last_input'] = input_file.name

    if st.session_state['last_input'] is not None:
        st.write('Last Uploaded File:')
        st.info(st.session_state["last_input"])

# 2. Graph Section
# - This section is used to generate a graph
# - The user can select the type of graph that they want to generate
# - The user can also customize the graph by changing the title, labels, and colors
if(selected == 'Graph Generator'):
    if(st.session_state['input_dataframe_page1'].empty == True):
        st.error('Error: Input file not found!')
    else:
        st.header('Generate Graph')
        df = st.session_state['input_dataframe_page1']
        st.dataframe(df, use_container_width=True)
        selection = select_graph()
        if(selection == 'Line Graph'):
            line_graph(df)
        elif(selection == 'Histogram'):
            histogram(df)
        elif(selection == 'Bar Graph'):
            bar_graph(df)
        elif(selection == 'Scatter Plot'):
            scatter_plot(df)

# 3. Data Explorer Section
# - This section is used to explore the data
# - The user can view the data in a table
# - The user can also view the statistics and graphs for each column
if(selected == 'Data Explorer'):
    if(st.session_state['input_dataframe_page1'].empty == True):
        st.error('Error: Input file not found!')
    else:
        # Main Code for Data Explorer Starts Here...
        # Add a header and load the dataframe
        st.header('Explore Data')
        df = st.session_state['input_dataframe_page1']

        # Display the dataframe
        st.dataframe(df, use_container_width=True)

        with st.spinner('Generating Data Report...'):
            # -- Overview Section --
            # Add a horizontal line and a subheader in the Streamlit app
            st.write('---')
            st.subheader('Overview')
            
            # create a 2-column layout
            col1, col2 = st.columns(2)

            # in the first column...
            with col1:
                st.write('Statistics')
                # create a dataframe with the statistics: # of variables, # of observations, # of missing cells, # of duplicate rows
                stats_df = pd.DataFrame({'# of Variables': [df.shape[1]], '# of Observations': [df.shape[0]], '# of Missing Cells': [df.isnull().sum().sum()], '# of Duplicate Rows': [df.duplicated().sum()]})
                # flip the dataframe so it display vertically
                stats_df = stats_df.T
                # Change index name
                stats_df.index.name = 'Statistics'
                st.dataframe(stats_df, use_container_width=True)

            # in the second column...
            with col2:
                st.write('Variable Types')
                # Count the number of variables for each type: numerical, categorical, other
                # if the variable contains numbers, check if it has <10 unique values, if yes then it is categorical
                # if the variable contains numbers, check if it has >10 unique values, if yes then it is numerical
                # if the variable contains string and it has <10 unique values, then it is categorical
                # if the variable contains string and it has >10 unique values, then it is other
                num = 0
                cat = 0
                other = 0

                for col in df.columns:
                    if df[col].dtype == 'object':
                        if df[col].nunique() < 10:
                            cat += 1
                        else:
                            other += 1
                    else:
                        if df[col].nunique() < 10:
                            cat += 1
                        else:
                            num += 1

                # create a dataframe with the statistics: # of numerical variables, # of categorical variables, # of other variables
                types_df = pd.DataFrame({'# of Numerical Variables': [num], '# of Categorical Variables': [cat], '# of Other Variables': [other]})
                # flip the dataframe so it display vertically
                types_df = types_df.T
                # Change index name
                types_df.index.name = 'Variable Types'
                st.dataframe(types_df, use_container_width=True)

            
            # -- Variables Section --
            st.write('---')
            st.subheader('Variables')
            # loop over each column in the dataframe
            for col in df.columns:
                # create a container for each column
                with st.container():
                    # make 2 columns, one for the statistics and one for the graphs
                    col1, col2 = st.columns(2)
                    with col1:
                        # column name and type, whether its numerical or categorical or other
                        st.write(col)
                        data_type = ''
                        if df[col].dtype == 'object':
                            if df[col].nunique() < 10:
                                data_type = 'Categorical'
                            else:
                                data_type = 'Other'
                        else:
                            if df[col].nunique() < 10:
                                data_type = 'Categorical'
                            else:
                                data_type = 'Numerical'
                        # create a dataframe with the statistics: variable type, # of unique values, # of missing values, mean, median, min, max
                        if(data_type == 'Numerical'):
                            stats_df = pd.DataFrame({'Variable Type': [data_type], '# of Unique Values': [df[col].nunique()], '# of Missing Values': [df[col].isnull().sum()], 'Mean': [round(df[col].mean(),3)], 'Median': [df[col].median()], 'Min': [df[col].min()], 'Max': [df[col].max()]})
                        elif(data_type == 'Categorical'):
                            stats_df = pd.DataFrame({'Variable Type': [data_type], '# of Unique Values': [df[col].nunique()], '# of Missing Values': [df[col].isnull().sum()]})
                        else:
                            stats_df = pd.DataFrame({'Variable Type': [data_type], '# of Unique Values': [df[col].nunique()], '# of Missing Values': [df[col].isnull().sum()]})
                        # flip the dataframe so it display vertically
                        stats_df = stats_df.T
                        # Change index name
                        stats_df.index.name = 'Statistics'
                        # display the dataframe
                        st.dataframe(stats_df, use_container_width=True)
                    with col2:
                        # create a graph for each column forcing the height to be the same as the height of the statistics
                        # use default color: #E18A6D for the chart
                        if(data_type == 'Numerical'):
                            fig = px.histogram(df, x=col, title=col, labels={col: 'Values'}, color_discrete_sequence=['#E18A6D'])
                            st.plotly_chart(fig, use_container_width=True)
                        # for categorical use horizontal bar chart where the y-axis is the label and the x-axis is the count and add a label that shows the total count
                        elif(data_type == 'Categorical'):
                            fig = px.histogram(df, y=col, title=col, labels={col: 'Values'}, color_discrete_sequence=['#E18A6D'])
                            fig.update_layout(bargap=0.30)
                            st.plotly_chart(fig, use_container_width=True) 
                        else:
                            st.warning('Graph not available for this variable type.')
                    st.write('---')


            # -- Correlations Section --
            st.subheader('Correlations')
            # loop through each columns and delete the columns that are . If the column is categorical, label encode it
            df_copy = df.copy()
            for col in df.columns:
                if df[col].dtype == 'object':
                    df_copy[col] = df_copy[col].astype('category').cat.codes
            # create a correlation matrix
            corr_matrix = df_copy.corr()
            # create a heatmap using the correlation matrix
            fig = px.imshow(corr_matrix)
            st.plotly_chart(fig, use_container_width=True)


            # -- Missing Values Section --
            st.write('---')
            st.subheader('Missing Values')
            # create a bar chart that shows the number of missing values for each column
            fig = px.bar(df.isnull().sum(), title='Missing Values', labels={'value': '# of Missing Values'})
            st.plotly_chart(fig, use_container_width=True)
        


#4. Download Section
# - This section serves as a guide for downloading the figures and reports
if(selected == 'Download'):
    download()
            

#5. Tutorial Section
tutorial_section()


