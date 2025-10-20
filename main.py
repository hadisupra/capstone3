import os
import langgraph
from openai import api_key
import st
from streamlit import text_input
import tiktoken
from dotenv import load_dotenv
from embedder import get_embedder
from utils import load_and_chunk_csv
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType

texts = load_and_chunk_csv("RESUME.csv", chunk_size=100)

load_dotenv()

# texts = batch_by_token(texts, 280000)
embedding_model = get_embedder()

qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
if not qdrant_client.collection_exists("resume_collection"):
    qdrant_client.recreate_collection(
        collection_name="resume_collection",
        vectors_config=VectorParams(size=len(embedding_model.embed_query("test")), distance=Distance.COSINE)
    )

vector_store = Qdrant(
    client=qdrant_client,
    collection_name="resume_collection",
    embeddings=embedding_model
)
from tiktoken import get_encoding

def batch_texts_by_token(texts, max_tokens=1000):
    enc = get_encoding("cl100k_base")
    batch, token_count = [], 0
    for text in texts:
        tokens = len(enc.encode(text))
        if token_count + tokens > max_tokens:
            yield batch
            batch, token_count = [text], tokens
        else:
            batch.append(text)
            token_count += tokens
    if batch:
        yield batch

for batch in batch_texts_by_token(texts):
    vector_store.add_texts(batch)


llm = OpenAI(model="gpt-5-nano", temperature=0.7, max_tokens=4096)
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

def chat_with_bot(question):
    return qa_chain.run(question)

# from langchain_core.tools import tool

@tool
def search_resume(query: str) -> str:
    """Search resume database for relevant info."""
    results = vector_store.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in results])

@tool
def current_datetime(_: str = "") -> str:
    """Get current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def post_resume_summary(_: str = "") -> str:
    """Simulate posting resume summary."""
    return "✅ Resume summary posted to dashboard!"
from langchain.agents import initialize_agent, AgentType

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage


resume_agent = create_react_agent(
    model="openai:gpt-5-nano",
    tools=[search_resume, current_datetime, post_resume_summary],
    prompt=SystemMessage(content="You are a resume assistant. Help users explore, summarize, and post resume insights.")
)
def interact_with_agent(user_input):
    return resume_agent.invoke(user_input)



import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("💬 Resume Advisor Chatbot")
st.image("https://img.freepik.com/free-vector/gradient-technology-background_23-2149436181.jpg?w=1380&t=st=1701628471~exp=1701629071~hmac=3b1f0e2a5a4f3f4e3")

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg.type):
        st.write(msg.content)

# Input box
user_input = st.chat_input("Type your message (or 'exit' to quit):")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Exit condition
    if user_input.lower() == "exit":
        st.stop()

    # Append user message
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Invoke agent
    response = resume_agent.invoke({"messages": st.session_state.messages})

    # Extract assistant reply
    assistant_msg = response["messages"][-1]
    st.session_state.messages.append(assistant_msg)

    # Show assistant message
    with st.chat_message("assistant"):
        st.write(assistant_msg.content)


