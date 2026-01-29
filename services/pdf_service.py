import pdfplumber
from pdf2image import convert_from_path
import re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path):
    text = ""

    # Try normal text extraction
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # If very little text → scanned document → use OCR
    if len(text.strip()) < 50:
        print("Using OCR for scanned PDF...")
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return text


def extract_key_information(text):
    # Extract dates
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)

    # Extract money amounts
    amounts = re.findall(r"(₹|\$|€)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?", text)

    # Extract reference numbers / IDs
    refs = re.findall(r"\b[A-Z0-9]{5,}\b", text)

    # Title (first non-empty line)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    title = lines[0] if lines else "Unknown Document"

    return {
        "title": title,
        "dates_found": ", ".join(dates[:5]),
        "amounts_found": ", ".join([a[0] + a[1] if isinstance(a, tuple) else a for a in amounts[:5]]),
        "reference_numbers": ", ".join(refs[:5]),
        "full_text": text[:1000]  # first 1000 characters
    }


def extract_tables_from_pdf(pdf_path):
    tables_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                tables_data.append(table)

    return tables_data


def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    key_info = extract_key_information(text)
    tables = extract_tables_from_pdf(pdf_path)

    return key_info, tables
