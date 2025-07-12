import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("gemini_api_key")

if not api_key:
    print("ERROR: gemini_api_key not found in environment variables.")
    exit(1)
else:
    print(f"Loaded API key: {api_key[:4]}...{'*' * (len(api_key)-8)}...{api_key[-4:]}")

genai.configure(api_key=api_key)

print("Available Gemini models for your API key:")
try:
    for m in genai.list_models():
        print(m.name)
except Exception as e:
    print(f"Error listing models: {e}") 