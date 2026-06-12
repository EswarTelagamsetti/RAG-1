import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(question, n_results=2):

    question_embedding = model.encode(question)

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(name="pdf_chunks")

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=n_results
    )

    return results["documents"][0]