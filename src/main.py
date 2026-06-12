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
        answer = generate_answer(question, retrieved_chunks)

        print("\n===== ANSWER =====\n")
        print(answer)
        print()


if __name__ == "__main__":
    main()