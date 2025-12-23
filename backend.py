from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st
from config import MODEL

load_dotenv()

def ask_lounes(chat_history):
    api_key = (
        st.secrets.get("GROQ_API_KEY")
        if hasattr(st, "secrets")
        else os.getenv("GROQ_API_KEY")
    )

    client = Groq(api_key=api_key)

    return client.chat.completions.create(
        model=MODEL,
        messages=chat_history,
        stream=True,
    )
