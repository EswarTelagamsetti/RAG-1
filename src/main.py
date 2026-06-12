from retrieve import retrieve_relevant_chunks
from chatbot import generate_answer


question = "How do I implement browser history navigation?"

retrieved_chunks = retrieve_relevant_chunks(question)

answer = generate_answer(question, retrieved_chunks)

print("\n===== ANSWER =====\n")
print(answer)