from pypdf import PdfReader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "testpdf" / "pdflatex-4-pages.pdf"

reader = PdfReader(pdf_path)
print(len(reader.pages))

metadata = reader.metadata
print(metadata)

page = reader.pages[0]
text = page.extract_text()

print(text)