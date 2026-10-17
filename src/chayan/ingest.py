import logging

from pypdf import PdfReader

from chayan.config import first_page, last_page, pdf_path

logging.getLogger("pypdf").setLevel(logging.ERROR)

def read_pages():
    pages = PdfReader(pdf_path).pages[first_page - 1:last_page]
    return [{"page": n, "text": p.extract_text() or ""} for n, p in enumerate(pages, first_page)]
