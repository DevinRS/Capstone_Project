import streamlit as st
from PIL import Image

img = Image.open("/ML_Sandbox/first.png")
with st.sidebar:
  st.image(image=img)


