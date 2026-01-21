
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

print("Listando modelos disponibles...")
try:
    # Listar modelos que soportan generateContent
    for model in client.models.list(config={'page_size': 100}):
        print(f"- {model.name}")
except Exception as e:
    print(f"Error al listar modelos: {e}")
