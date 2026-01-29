from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from fastapi.responses import RedirectResponse

from services.pdf_service import process_pdf
from services.excel_service import create_excel

app = FastAPI()   

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/")
def home():
    return {"message": "Generic PDF to Excel API Running"}


@app.post("/process-pdf/")
async def process_pdf_file(file: UploadFile = File(...)):
    pdf_path = os.path.join(TEMP_DIR, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    key_info, tables = process_pdf(pdf_path)

    excel_path = os.path.join(TEMP_DIR, "structured_output.xlsx")
    create_excel(key_info, tables, excel_path)

    return {
        "message": "PDF processed successfully",
        "download_excel": "/download-excel/"
    }


@app.get("/download-excel/")
def download_excel():
    file_path = os.path.join(TEMP_DIR, "structured_output.xlsx")
    return FileResponse(
        file_path,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename="Processed_Output.xlsx"
    )
