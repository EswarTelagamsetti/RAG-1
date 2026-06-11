from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


pdf_path = "data/pdfs/sample.pdf"

extracted_text = extract_text_from_pdf(pdf_path)

print(extracted_text)