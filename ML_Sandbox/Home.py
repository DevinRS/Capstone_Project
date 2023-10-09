import streamlit as st
from PIL import Image

img = Image.open("Capstone_Project/ML_Sandbox/pictures/first.png")
with st.sidebar:
  st.image(image=img)


