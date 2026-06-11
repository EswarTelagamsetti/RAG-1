from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text



def chunk_text(text, chunk_size=80, overlap=20):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start = start + chunk_size - overlap

    return chunks


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


pdf_path = "data/pdfs/sample.pdf"

extracted_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(extracted_text)

chunks = chunk_text(cleaned_text)

print(f"Total Chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index + 1} ---")
    print(chunk)