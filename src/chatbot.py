import os
from dotenv import load_dotenv
from google import genai


def generate_answer(question, retrieved_chunks):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
Answer the user's question using only the context below.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text