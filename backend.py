from groq import Groq
from dotenv import load_dotenv
import os

from config import MODEL

load_dotenv()

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def ask_lounes(chat_history):
    """
    Envoie l'historique de conversation à Groq
    
    Args:
        chat_history (list): Liste de messages avec role et content
    
    Returns:
        Stream de réponses
    """
    client = Groq(api_key=os.getenv("GROQ_KEY"))

    stream_response = client.chat.completions.create(
        messages=chat_history,
        stream=True,
        model=MODEL
    )

    return stream_response

def read_stream_response(stream_response):
    """Lit et affiche le stream de réponses"""
    for chunk in stream_response:
        if chunk.choices[0].delta.content is None:
            continue
        print(chunk.choices[0].delta.content, end="")
    print()  # Retour à la ligne final

# Test
if __name__ == "__main__":
    # ✅ CORRECTION : Créer un chat_history au bon format
    chat_history = [
        {
            "role": "system",
            "content": read_file('context.txt')
        },
        {
            "role": "user",
            "content": "Quel est le meilleur club du monde ?"
        }
    ]
    
    stream_response = ask_lounes(chat_history=chat_history)
    read_stream_response(stream_response)