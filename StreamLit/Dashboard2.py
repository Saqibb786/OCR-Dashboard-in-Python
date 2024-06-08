import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
import pytesseract
from pytesseract import Output
import PIL.Image
import cv2

warnings.filterwarnings('ignore')
st.set_page_config(page_title="OCR to Text2", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: OCR to Text")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(" :file_folder: Upload a file", type=["png", "jpg", "jpeg", "GIF"])

if fl is not None:
    filename = fl.name
    st.write(filename)

    # Perform OCR on the uploaded image
    myconfig = r"--psm 6 --oem 3"
    img = PIL.Image.open(fl)
    text = pytesseract.image_to_string(img, config=myconfig)
    st.markdown(f"**Extracted Text:**")
    st.write(text)
