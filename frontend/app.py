"""
MediQuery-X — Streamlit frontend
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/chat/"

st.set_page_config(page_title="MediQuery-X", page_icon="🏥", layout="centered")
st.title("🏥 MediQuery-X")
st.caption("Healthcare FAQ assistant powered by LangGraph + RAG. Not a substitute for medical advice.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if query := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                resp = requests.post(API_URL, json={
                    "query": query,
                    "conversation_history": st.session_state.messages[:-1],
                }, timeout=30)
                data = resp.json()
                answer = data.get("answer", "Sorry, something went wrong.")
                sources = data.get("sources_used", 0)
            except Exception as e:
                answer = f"Connection error: {e}"
                sources = 0

        st.write(answer)
        st.caption(f"Sources retrieved: {sources}")

    st.session_state.messages.append({"role": "assistant", "content": answer})
