from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import easyocr
import shutil
import os

# Initialize the FastAPI app
app = FastAPI()

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# Create a directory for storing uploaded images
if not os.path.exists('uploaded_images'):
    os.makedirs('uploaded_images')

# Define the upload route
@app.post("/upload", response_class=HTMLResponse)
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join('uploaded_images', file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Use EasyOCR to read text from the image
    result = reader.readtext(file_path)
    extracted_text = " ".join([detection[1] for detection in result])
    
    # Render the result in the template
    return templates.TemplateResponse("result.html", {"request": {}, "extracted_text": extracted_text, "image_path": file_path})

# Define the home route
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# How To Run commands
# cd ".\@Project\Fast API\v1"
# python fileName.py
# http://localhost:8000/