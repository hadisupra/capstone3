import streamlit as st
from main import interact_with_agent, chat_with_bot             
def set_page_config():
     st.set_page_config(
         page_title="Chatbot Sederhana",
         page_icon="🤖"
     )
     st.title("🧠 Resume Chatbot")
     st.write("Ask me anything about your resume!")

query = st.text_input("Your question:")
if query:
    with st.spinner("Thinking..."):
        response = interact_with_agent(query)
    st.success(response)
