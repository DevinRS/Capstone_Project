import streamlit as st
from PIL import Image

img = Image.open('pictures/first.png')
with st.sidebar:
  st.image("first.png")


