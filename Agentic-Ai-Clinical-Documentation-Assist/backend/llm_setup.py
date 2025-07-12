from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    api_key = os.getenv("groq_api_key")
    if not api_key:
        raise ValueError("groq_api_key not found in environment variables.")
    # Using 'llama3-70b-8192' as the recommended Groq model
    return ChatGroq(
        model_name="llama3-70b-8192",
        groq_api_key=api_key
    )
