import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
# ----
# Definition and Globals
# ----

# Graph Selector
def select_graph():
    selection = st.selectbox(label='Select: ', options=['Line Graph', 'Pie Chart', 'Bar Graph', 'Scatter Plot'])

    return selection


# Line Graph Editor
def line_graph(df: pd.DataFrame):
    st.write('---')
    st.subheader('Line Graph Editor')
    col_names = df.columns.tolist()
    col_names.append('Auto')
    col1, col2 = st.columns((1,2))
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            X_val = st.selectbox('Select X-axis Variable', col_names)
            col_names2 = [item for item in col_names if item != X_val]
            X_label = st.text_input('Enter X-axis Label', value=X_val)
        with col4:
            Y_val = st.selectbox('Select Y-axis Variable', col_names2)
            Y_label = st.text_input('Enter Y-axis Label', value=Y_val)
        title = st.text_input('Enter Graph Title', value='Graph')
        col5, col6, col7 = st.columns(3)
        with col5:
            line_color = st.color_picker('Line Color', value='#e18a6d')
        with col6:
            label_font_color = st.color_picker('Label Color', value='#FFFFFF')
        with col7:
            tick_font_color = st.color_picker('Tick Color', value='#FFFFFF')
        transparent_bg = st.checkbox('Transparent Background', value=False)

    with col2:
        if X_val != 'Auto' and Y_val != 'Auto':
            fig = px.line(df, x=X_val, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val == 'Auto' and Y_val != 'Auto':
            fig = px.line(df, y=Y_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        elif X_val != 'Auto' and Y_val == 'Auto':
            fig = px.line(df, x=X_val, title=title, labels={X_val: X_label, Y_val: Y_label})
        else:
            st.write("Please select at least one axis variable.")
        
        # Custom color
        fig.update_traces(line=dict(color=line_color))
        if transparent_bg:
            fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        # Custom color for labels
        fig.update_layout(title_font=dict(color=label_font_color))
        fig.update_xaxes(title_text=X_label, title_font=dict(color=label_font_color))
        fig.update_yaxes(title_text=Y_label, title_font=dict(color=label_font_color))
        # Custom color for x and y-axis values
        fig.update_xaxes(tickfont=dict(color=tick_font_color))
        fig.update_yaxes(tickfont=dict(color=tick_font_color))

        st.plotly_chart(fig, use_container_width=True)

    st.write('---')

# TO IMPLEMENT
def pie_chart(df: pd.DataFrame):
    return

def bar_graph(df: pd.DataFrame):
    return

def scatter_plot(df: pd.DataFrame):
    return

# Saved Graph Section Components
def saved_graph():
    return


# Tutorial Section Components
def hide_me():
    selection = st.checkbox('Hide Me', value=False)

    return selection

def tutorial_section():
    st.header('New to Graph?')
    st.write('''
"Welcome to the world of graphs, where numbers come to life in colorful, mesmerizing displays! 🚀✨ If you're scratching your head, wondering what on earth a graph is, fear not! We're here to sprinkle a little graphy magic into your life. No prior graph knowledge needed – just bring your curiosity and data, and we'll transform it into captivating visual stories. Get ready to 'wow' your friends and colleagues with your newfound graph superpowers. Ready? Let's dive in!"
''')
    st.subheader('What would you like your graph to highlight in your data?')
    with st.expander('Visualize Data Changes Over Time ⏳'):
        st.write('''
Ready to turn your data into a time-traveling adventure? Strap in, because we're about to visualize how things evolve over time. Choose a graph that suits your data's journey!
                 
We recommend the following:
1. Line Chart 📈
2. Area Chart 🌄
3. Scatter Plot 🌟
''')
    with st.expander('Compare Categories or Groups 📊'):
        st.write('''
Time to become the detective of data! Uncover hidden insights by comparing different categories or groups within your data. Select the ideal graph to reveal the story of your data.
                 
We recommend the following:
1. Bar Chart 📊
2. Histogram 📚
3. Stacked Column Chart 📉
''')
    with st.expander('Show Proportions or Percentages 📈'):
        st.write('''
Want to slice and dice your data into delicious proportions? Dive into the world of percentages and proportions with these graph options!
                 
We recommend the following:
1. Pie Chart 🥧
2. Donut Chart 🍩
3. 100% Stacked Area Chart 📊
''')

# ----
# Page Config
# ----
st.set_page_config(
    page_title='Make Your Graphs!',
    page_icon='📊',
    layout="wide",
    initial_sidebar_state='auto',
    menu_items=None
)

# ----
# Topbar
# ----

selected = option_menu(
    menu_title= "ML Sandbox",
    options=['Upload', 'Graph Generator', 'Saved Graphs'],
    orientation="horizontal"
)
# ----
# Body
# ----
# 1. Input Section
st.header('Upload File')
input_file = st.file_uploader('Choose a CSV file', type='csv', key='input_file')
df = None

# 2. Graph Section
if input_file is not None:
    st.header('Generate Graph')
    df = pd.read_csv(input_file)
    st.write(df)
    selection = select_graph()
    if(selection == 'Line Graph'):
        line_graph(df)
    elif(selection == 'Pie Chart'):
        pie_chart(df)
    elif(selection == 'Bar Graph'):
        bar_graph(df)
    elif(selection == 'Scatter Plot'):
        scatter_plot(df)

#3. Saved Graph Section
saved_graph()

#4. Tutorial Section
hideCheckBox = hide_me()
if(hideCheckBox == False):
    tutorial_section()
    




# ----
# Sidebar
# ----
#with st.sidebar:
#    st.header('Make Your Graphs!')
#    upload_file_button = st.link_button('1. Upload File', use_container_width=True, url='/#upload-file')
    #if input_file is not None:
    #    generate_graph_button = st.link_button('2. Generate Graph', use_container_width=True, disabled=False, url='#generate-graph')    
    #else:
    #    generate_graph_button = st.link_button('2. Generate Graph', use_container_width=True, disabled=True, url="/#generate-graph")
    #saved_graph_button = st.button('3. Saved Graph', use_container_width=True, disabled=True)


