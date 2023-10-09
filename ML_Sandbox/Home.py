import streamlit as st
from PIL import Images

img = Image.open("/pictures/first.png")
with st.sidebar:
  st.image(img)


