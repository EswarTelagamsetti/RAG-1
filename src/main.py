from retrieve import retrieve_relevant_chunks
from chatbot import generate_answer


def main():
    print("RAG Chatbot Started")
    print("Type 'exit' to stop\n")

    while True:
        question = input("Ask question: ")

        if question.lower() == "exit":
            print("Chatbot stopped")
            break

        retrieved_chunks = retrieve_relevant_chunks(question)

        print("\n===== RETRIEVED CHUNKS =====")
        for chunk in retrieved_chunks:
            print(f"ID: {chunk['id']}")
            print(f"Source: {chunk['source']}")
            print(f"Chunk Index: {chunk['chunk_index']}")
            print(f"Distance: {chunk['distance']}")
            print()

        chunk_texts = []

        for chunk in retrieved_chunks:
            chunk_texts.append(chunk["text"])

        answer = generate_answer(question, chunk_texts)

        print("\n===== ANSWER =====")
        print(answer)

        print("\n===== SOURCES =====")
        for chunk in retrieved_chunks:
            print(f"{chunk['source']} (chunk {chunk['chunk_index']})")
        print()


if __name__ == "__main__":
    main()