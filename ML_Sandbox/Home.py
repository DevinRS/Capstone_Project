import streamlit as st
from PIL import Image

img = Image.open("ML_Sandbox/pictures/first.png")
with st.sidebar:
  st.image(img)


