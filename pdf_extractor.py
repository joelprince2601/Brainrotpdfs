import pdfplumber
from typing import Dict

class PDFExtractor:
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF file page by page"""
        page_texts = {}
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    page_texts[page_num] = text.strip()
        
        return page_texts 