import streamlit as st
import pytesseract
from pytesseract import Output
import PIL.Image
import cv2
import numpy as np

# Function to extract text from image
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, config=r"--psm 6 --oem 3")
    return text

# Streamlit application
def main():
    # Page title and description
    st.set_page_config(page_title="Image Text Extraction Dashboard", page_icon=":camera:", layout="wide")
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .main-title {
            color: #000000;
            font-weight: 600;
            text-align: center;
            margin-bottom: 40px;
        }

        .sidebar .sidebar-content {
            background-color: #F0F2F6;
        }

        .sidebar .sidebar-content h2 {
            color: #FF4B4B;
        }

        .footer {
            background-color: #f1f1f1;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #eaeaea;
            margin-top: 200px;
        }

        .footer p {
            margin: 0;
            color: #240909;
        }

        .footer h4 {
            color: #FF4B4B;
            margin-top: 20px;
        }

        .footer ol {
            text-align: left;
            display: inline-block;
            padding-left: 20px;
        }

        .expander .streamlit-expanderHeader {
            color: #FF4B4B;
        }

        .stButton button {
            background-color: #FF4B4B !important;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        .stButton button:hover {
            background-color: #D94444 !important;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<h1 class="main-title">📸 Image Text Extraction Dashboard</h1>', unsafe_allow_html=True)
    st.write("Upload an image file and extract text using Tesseract OCR.")

    # Sidebar for file upload
    with st.sidebar:
        st.header("Upload Image")
        uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Convert the file to an image
        image = PIL.Image.open(uploaded_file)

        # Display uploaded image in main area
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Extract text from image
        st.write("Extracting text from image...")
        with st.spinner('Processing...'):
            text = extract_text_from_image(image)

        # Display extracted text in an expandable area
        st.subheader("Extracted Text")
        with st.expander("Show Extracted Text"):
            st.text_area("", text, height=200)

        # Option to download the extracted text as a .txt file
        st.download_button(label="Download Extracted Text", data=text, file_name="extracted_text.txt", mime="text/plain")

    # Beautiful footer with About the App section
    st.markdown("""
    <div class="footer">
        <p>Made with ❤ using Streamlit</p>
        <p>&copy; 2024 Image Text Extraction Dashboard</p>
        <div>
            <h4>About the App</h4>
            <p>This Streamlit app allows you to extract text from images using the Tesseract OCR engine. Simply upload an image file, and the app will display the extracted text.</p>
            <p>The app is built using Python, Streamlit, and Tesseract OCR. It provides a user-friendly interface for text extraction and the ability to download the extracted text as a .txt file.</p>
            <h4>How to Use</h4>
            <ol>
                <li>Upload an image file by clicking the 'Choose an image file' button in the sidebar.</li>
                <li>The uploaded image will be displayed in the main area.</li>
                <li>The app will automatically extract the text from the image and display it in an expandable area.</li>
                <li>You can download the extracted text as a .txt file by clicking the 'Download Extracted Text' button.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
