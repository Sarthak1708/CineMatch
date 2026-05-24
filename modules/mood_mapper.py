import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from modules.config import get_secret
client = Groq(api_key=get_secret("GROQ_API_KEY"))

def map_mood_to_query(mood_input):
    prompt = f"""
You are a movie recommendation assistant. A user described their mood or feeling as:
"{mood_input}"

Based on this, generate a natural language movie search query that would find movies matching their emotional state.
Also provide genre tags and tone descriptors.

Respond ONLY in this JSON format with no extra text:
{{
    "search_query": "a descriptive movie search query based on the mood",
    "genres": ["genre1", "genre2"],
    "tone": ["tone1", "tone2"],
    "avoid": ["genre or tone to avoid"]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw = response.choices[0].message.content.strip()

    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return result
    except:
        return {
            "search_query": mood_input,
            "genres": [],
            "tone": [],
            "avoid": []
        }

if __name__ == "__main__":
    mood = "I'm feeling lonely and want something heartwarming"
    result = map_mood_to_query(mood)
    print(result)