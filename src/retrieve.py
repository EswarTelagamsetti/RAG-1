import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_relevant_chunks(question, n_results=2):
    question_embedding = model.encode(question)

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(
        name="pdf_chunks"
    )

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=n_results
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    for i in range(len(documents)):
        retrieved_chunks.append({
            "id": ids[i],
            "text": documents[i],
            "source": metadatas[i]["source"],
            "chunk_index": metadatas[i]["chunk_index"],
            "distance": distances[i]
        })

    return retrieved_chunks