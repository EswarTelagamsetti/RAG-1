from google import genai
from dotenv import load_dotenv
import os


def rewrite_question(question, chat_history):
    return question