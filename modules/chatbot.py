import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from groq import Groq
from modules.retriever import search
from modules.mood_mapper import map_mood_to_query
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(movie, user_query):
    prompt = f"""
You are a movie recommendation assistant. Explain in 2-3 sentences why someone who asked for "{user_query}" would enjoy this movie:

Title: {movie['title']}
Year: {movie['release_year']}
Genres: {movie['genres']}
Overview: {movie['overview']}
Cast: {movie['movie_cast']}
Director: {movie['director']}

Be specific, enthusiastic and mention something unique about the movie. No generic responses.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def stream_chat(user_message, history=[]):
    history.append({"role": "user", "content": user_message})

    system_prompt = """
You are CineAI, a smart movie recommendation chatbot.
Your job is to understand what the user wants and extract a clear movie search query from the conversation.
Consider the full conversation history when refining recommendations.
Respond ONLY in this JSON format:
{
    "search_query": "refined movie search query based on full conversation",
    "response": "your conversational response to the user"
}
"""

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + history,
        temperature=0.7,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full_response += delta
        yield delta, None, None

    try:
        clean = full_response.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        search_query = result.get("search_query", user_message)
        bot_response = result.get("response", "Here are some recommendations!")
    except:
        search_query = user_message
        bot_response = full_response

    movies = search(search_query, top_k=5)
    history.append({"role": "assistant", "content": full_response})

    yield None, bot_response, movies, history


def chat(user_message, history=[]):
    history.append({"role": "user", "content": user_message})

    system_prompt = """
You are CineAI, a smart movie recommendation chatbot.
Your job is to understand what the user wants and extract a clear movie search query from the conversation.
Consider the full conversation history when refining recommendations.
Respond ONLY in this JSON format:
{
    "search_query": "refined movie search query based on full conversation",
    "response": "your conversational response to the user"
}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + history,
        temperature=0.7
    )

    raw = response.choices[0].message.content.strip()

    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        search_query = result.get("search_query", user_message)
        bot_response = result.get("response", "Here are some recommendations!")
    except:
        search_query = user_message
        bot_response = "Here are some recommendations based on what you said!"

    movies = search(search_query, top_k=5)
    history.append({"role": "assistant", "content": raw})

    return bot_response, movies, history