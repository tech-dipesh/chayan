import logging
from pypdf import PdfReader
from src.config import pdf_path, first_page, last_page

logging.getLogger("pypdf").setLevel(logging.ERROR)

def read_pages():
    pages = PdfReader(pdf_path).pages[first_page - 1:last_page]
    return [{"page": n, "text": p.extract_text() or ""} for n, p in enumerate(pages, first_page)]
