from groq import Groq
from dotenv import load_dotenv
import os

from config import MODEL

load_dotenv()

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def ask_lounes(question, history=None):
    """
    Pose une question à Lounes
    
    Args:
        question (str): La question à poser
        history (list): Historique optionnel de conversation
    
    Returns:
        Stream de réponses
    """
    client = Groq(api_key=os.getenv("GROQ_KEY"))
    
    # Construire le chat_history
    chat_history = [
        {
            "role": "system",
            "content": read_file('context.txt')
        }
    ]
    
    # Ajouter l'historique si fourni
    if history:
        chat_history.extend(history)
    
    # Ajouter la nouvelle question
    chat_history.append({
        "role": "user",
        "content": question
    })

    stream_response = client.chat.completions.create(
        messages=chat_history,
        stream=True,
        model=MODEL
    )

    return stream_response

def read_stream_response(stream_response):
    """Lit et affiche le stream de réponses"""
    full_response = ""
    for chunk in stream_response:
        if chunk.choices[0].delta.content is None:
            continue
        content = chunk.choices[0].delta.content
        print(content, end="")
        full_response += content
    print()
    return full_response

# Test
if __name__ == "__main__":
    # ✅ Maintenant ça marche !
    stream_response = ask_lounes(question="Quel est le meilleur club du monde ?")
    response = read_stream_response(stream_response)