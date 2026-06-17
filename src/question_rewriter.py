import os
from dotenv import load_dotenv
from google import genai


def rewrite_question(question, chat_history):
    if len(chat_history) == 0:
        return question

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    history_text = ""

    for chat in chat_history:
        history_text += f"User: {chat['question']}\n"
        history_text += f"Bot: {chat['answer']}\n\n"

    prompt = f"""
Rewrite the current user question into a complete standalone question.

Use the previous conversation only to resolve words like:
it, this, that, they, explain more, give example.

Do not answer the question.
Only return the rewritten question.

Previous Conversation:
{history_text}

Current Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()