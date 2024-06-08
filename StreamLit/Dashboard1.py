import streamlit as st
import pandas as pd
# import plotly.express as px 
import os
import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
import numpy as np
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="OCR Converter!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: OCR to Text1")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File uploader for image files
uploaded_file = st.file_uploader(" :file_folder: Upload an image file", type=["png", "jpg", "jpeg", "gif"])

# OCR function
def perform_ocr(image_path):
    myconfig = r"--psm 6 --oem 3"
    text = pytesseract.image_to_string(image_path, config=myconfig)
    return text

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Perform OCR
    text = perform_ocr(uploaded_file.name)
    
    # Display the original image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=False)
    
    # Display OCR results
    st.subheader("OCR Text")
    st.write(text)

else:
    st.write("Please upload an image file to perform OCR.")
