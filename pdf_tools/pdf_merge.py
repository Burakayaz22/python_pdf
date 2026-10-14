import pymupdf

def pdfmerge(pfad,pdf):
    with pymupdf.open(pfad) as dokument:
        pdf.insert_pdf(dokument)

    return pdf