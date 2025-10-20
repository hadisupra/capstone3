import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env into environment

# Access variables
openai_key = os.getenv("OPENAI_API_KEY")
backend = os.getenv("EMBEDDING_BACKEND")

print(f"Using backend: {backend}")
print(f"using AI key : {openai_key}")

from embedder import get_embedder
embedder = get_embedder()
print(embedder)
print(embedder.embed_query("This is a test query."))
print(embedder.embed_documents(["This is the first document.", "This is the second document."]))    