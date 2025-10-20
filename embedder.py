import os
from dotenv import load_dotenv
load_dotenv()

def get_embedder():
    backend = os.getenv("EMBEDDING_BACKEND", "openai")
    if backend == "openai":
        from langchain_community.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)
    elif backend == "fastembed":
        from fastembed import TextEmbedding
        return TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    else:
        raise ValueError("Unsupported embedding backend")
