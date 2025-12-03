import pdfplumber
import fitz
import pytesseract
import pandas as pd
from PIL import Image
import io
import os

def extract_pdf_text(path):
    try:
        with pdfplumber.open(path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        print(f"[WARN] Failed to extract text from PDF {path}: {e}")
        return ""

def ocr_image_bytes(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return pytesseract.image_to_string(image)
    except:
        return ""

def extract_pdf_images(path):
    ocr_list = []
    try:
        pdf = fitz.open(path)
        for page in pdf:
            for img in page.get_images(full=True):
                xref = img[0]
                base = pdf.extract_image(xref)
                ocr_list.append(ocr_image_bytes(base["image"]))
    except Exception as e:
        print(f"[WARN] Image extraction failed: {e}")
    return ocr_list

def extract_tables_csv_or_excel(path):
    try:
        if path.lower().endswith("xlsx"):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        return [df.to_markdown(index=False)]
    except:
        return []

def ingest_pdf(path):
    return {
        "source": os.path.basename(path),
        "text": extract_pdf_text(path),
        "tables": extract_tables_csv_or_excel(path),
        "images_ocr": extract_pdf_images(path)
    }

def ingest_image(path):
    try:
        ocr = ocr_image_bytes(open(path,"rb").read())
    except:
        ocr = ""
    return {"source": os.path.basename(path),"text":"", "tables":[], "images_ocr":[ocr]}

def ingest_table(path):
    return {"source": os.path.basename(path),"text":"", "tables":extract_tables_csv_or_excel(path),"images_ocr":[]}

def ingest_document_set(pdf_paths=[], image_paths=[], table_paths=[]):
    docs = []
    for p in pdf_paths: docs.append(ingest_pdf(p))
    for p in image_paths: docs.append(ingest_image(p))
    for p in table_paths: docs.append(ingest_table(p))
    return docs