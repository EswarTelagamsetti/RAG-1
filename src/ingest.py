from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os
from dotenv import load_dotenv
from google import genai


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

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="pdf_chunks")

question = "How do I implement browser history navigation?"

question_embedding = model.encode(question)

results = collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=2
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client_gemini = genai.Client(api_key=api_key)

retrieved_chunks = "\n\n".join(results["documents"][0])

prompt = f"""
Answer the user's question using only the context below.

Context:
{retrieved_chunks}

Question:
{question}
"""

response = client_gemini.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n===== ANSWER =====\n")
print(response.text)