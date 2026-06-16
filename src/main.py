from retrieve import retrieve_relevant_chunks
from chatbot import generate_answer
import os

def main():
    print("RAG Chatbot Started")
    print("Type 'exit' to stop\n")

    print("Select document:")
    

    pdf_files = []

    for file in os.listdir("data/pdfs"):
        if file.endswith(".pdf"):
            pdf_files.append(file)

    print("\nSelect document:")
    print("1. all")

    for i in range(len(pdf_files)):
        print(f"{i+2}. {pdf_files[i].replace('.pdf','')}")

    choice = input("Enter choice: ")

    document_name = None

    if choice == "1":
        document_name = None
        print("\nSelected document: all")

    else:
        index = int(choice) - 2

    if 0 <= index < len(pdf_files):
        document_name = f"data/pdfs\\{pdf_files[index]}"
        print(f"\nSelected document: {document_name}")

    while True:
        question = input("Ask question: ")

        if question.lower() == "exit":
            print("Chatbot stopped")
            break

        retrieved_chunks = retrieve_relevant_chunks(
            question,
            document_name=document_name
        )

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