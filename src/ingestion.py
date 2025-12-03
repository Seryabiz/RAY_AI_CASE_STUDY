import pdfplumber
import fitz
import pytesseract
import pandas as pd
from PIL import Image
import io
import os

def extract_pdf_text(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        print(f"[WARN] Failed to extract text from PDF {path}: {e}")
    return text

def extract_pdf_images(path):
    images_ocr = []
    try:
        pdf = fitz.open(path)
        for page_index, page in enumerate(pdf):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                ocr_text = ocr_image_bytes(image_bytes)
                images_ocr.append(ocr_text)
    except Exception as e:
        print(f"[WARN] Failed to extract images from PDF {path}: {e}")
    return images_ocr

def ocr_image_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)

def extract_tables_csv_or_excel(path):
    tables = []
    try:
        if path.endswith("xlsx"):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        tables.append(df.to_markdown())
    except Exception as e:
        print(f"[WARN] Failed to extract table from {path}: {e}")
    return tables

def ingest_pdf(path):
    return {
        "source": os.path.basename(path),
        "text": extract_pdf_text(path),
        "tables": [],
        "images_ocr": extract_pdf_images(path)
    }

def ingest_image(path):
    ocr_text = ""
    try:
        with open(path, "rb") as f:
            ocr_text = ocr_image_bytes(f.read())
    except Exception as e:
        print(f"[WARN] Failed to OCR image {path}: {e}")
    return {
        "source": os.path.basename(path),
        "text": "",
        "tables": [],
        "images_ocr": [ocr_text]
    }

def ingest_table(path):
    return {
        "source": os.path.basename(path),
        "text": "",
        "tables": extract_tables_csv_or_excel(path),
        "images_ocr": []
    }

def ingest_document_set(pdf_paths=[], image_paths=[], table_paths=[]):
    docs = []

    for p in pdf_paths:
        docs.append(ingest_pdf(p))

    for p in image_paths:
        docs.append(ingest_image(p))

    for p in table_paths:
        docs.append(ingest_table(p))

    return docs