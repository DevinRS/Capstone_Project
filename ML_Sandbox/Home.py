import streamlit as st
from PIL import Image

img = Image.open("first.png")
with st.sidebar:
  st.image(img)


