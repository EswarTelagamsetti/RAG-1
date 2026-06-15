from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


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


def ingest_pdf(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(extracted_text)
    chunks = chunk_text(cleaned_text)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="pdf_chunks")

    document_name = os.path.basename(pdf_path)
    document_name = document_name.replace(".pdf", "")

    ids = []
    metadatas = []

    for index in range(len(chunks)):
        ids.append(f"{document_name}_chunk_{index}")
        metadatas.append({
            "source": pdf_path,
            "chunk_index": index
        })

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


if __name__ == "__main__":

    pdf_folder = "data/pdfs"

    files = os.listdir(pdf_folder)

    for file in files:

        if file.endswith(".pdf"):

            pdf_path = os.path.join(pdf_folder, file)

            print(f"\nProcessing: {file}")

            ingest_pdf(pdf_path)