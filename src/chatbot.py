import os
from dotenv import load_dotenv
from google import genai


def generate_answer(question, retrieved_chunks, chat_history):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    context = "\n\n".join(retrieved_chunks)
    history_text = ""

    for chat in chat_history:
        history_text += f"User: {chat['question']}\n"
        history_text += f"Bot: {chat['answer']}\n\n"

    prompt = f"""
    Answer the user's question using only the context below and the previous conversation.

    Previous Conversation:
    {history_text}

    Context:
    {context}

    Current Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text