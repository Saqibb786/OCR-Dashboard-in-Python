from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import easyocr
import shutil
import os
import docx
import pandas as pd

# Initialize the FastAPI app
app = FastAPI()

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en', 'es', 'fr', 'de', 'it'])  # Add more languages as needed

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# Create a directory for storing uploaded and processed files
if not os.path.exists('uploaded_images'):
    os.makedirs('uploaded_images')
if not os.path.exists('output_files'):
    os.makedirs('output_files')

# Define the upload route
@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...), language: str = Form(...), output_format: str = Form(...)):
    # Save the uploaded file
    file_path = os.path.join('uploaded_images', file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Use EasyOCR to read text from the image
    reader.lang_list = [language]
    result = reader.readtext(file_path)
    extracted_text = " ".join([detection[1] for detection in result])
    
    # Prepare the output file
    output_file_path = os.path.join('output_files', f"{os.path.splitext(file.filename)[0]}.{output_format}")
    if output_format == 'txt':
        with open(output_file_path, "w") as f:
            f.write(extracted_text)
    elif output_format == 'docx':
        doc = docx.Document()
        doc.add_paragraph(extracted_text)
        doc.save(output_file_path)
    elif output_format == 'xlsx':
        df = pd.DataFrame([extracted_text])
        df.to_excel(output_file_path, index=False, header=False)
    
    # Render the result in the template
    return templates.TemplateResponse("result.html", {
        "request": request,
        "extracted_text": extracted_text,
        "image_path": file_path,
        "output_file_path": f"/download/{os.path.basename(output_file_path)}"
    })

# Define the download route
@app.get("/download/{file_name}", response_class=FileResponse)
async def download_file(file_name: str):
    file_path = os.path.join('output_files', file_name)
    return FileResponse(path=file_path, filename=file_name)

# Define the home route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
