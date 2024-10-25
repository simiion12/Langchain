from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="vars/.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

