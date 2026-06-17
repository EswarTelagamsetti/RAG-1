from retrieve import retrieve_relevant_chunks
from chatbot import generate_answer
import os
from question_rewriter import rewrite_question

def main():
    print("RAG Chatbot Started")
    print("Type 'exit' to stop\n")

    pdf_files = []

    for file in os.listdir("data/pdfs"):
        if file.endswith(".pdf"):
            pdf_files.append(file)

    print("Select document:")
    print("1. all")

    for i in range(len(pdf_files)):
        print(f"{i + 2}. {pdf_files[i].replace('.pdf', '')}")

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
        else:
            print("Invalid choice. Using all documents.")
            document_name = None

    chat_history = []

    while True:
        question = input("Ask question: ")

        if question.lower() == "exit":
            print("Chatbot stopped")
            break
        enhanced_question = rewrite_question(question, chat_history)
        print(f"\nRewritten Question: {enhanced_question}")

        retrieved_chunks = retrieve_relevant_chunks(
            enhanced_question,
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

        answer = generate_answer(question, chunk_texts, chat_history)

        chat_history.append({
            "question": question,
            "answer": answer
        })
        if len(chat_history) > 5:
            chat_history.pop(0)

        print("\n===== ANSWER =====")
        print(answer)

        print("\n===== SOURCES =====")
        for chunk in retrieved_chunks:
            print(f"{chunk['source']} (chunk {chunk['chunk_index']})")

        print()


if __name__ == "__main__":
    main()