<div align="center">

# 🎬 CineAI

### AI-Powered Semantic Movie Discovery

*Find your next film through natural language, mood, and conversation*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-ff4d6d?style=for-the-badge&logo=streamlit&logoColor=white)](https://cinematch-mfdyxepceekreypyp6exjd.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Sarthak1708-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sarthak1708/CineMatch)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## What is CineAI?

CineAI is a full-stack AI movie recommendation system that goes beyond keyword search. Instead of typing a movie title, you describe a vibe — *"slow burn psychological thriller with an unreliable narrator"* — and CineAI finds films that semantically match your intent using vector embeddings and FAISS similarity search.

Built on a multi-layer GenAI pipeline with a real PostgreSQL backend, live TMDB data, and a conversational chat interface powered by LLaMA 3.3 70B.

---

## Features

**Semantic Search**
Describe any movie concept in natural language. The FAISS index finds the closest matches by meaning, not just keywords — across 4,100+ films.

**Mood-Based Filtering**
Tell CineAI how you're feeling. The LLM maps your emotional state to genre tags, tone descriptors, and a refined search query — then retrieves films that match your mood.

**Conversational Chat with Streaming**
Multi-turn chat interface where you can progressively refine recommendations. Responses stream word-by-word in real time via Groq's inference API.

**AI-Generated Explanations**
For every recommendation, CineAI generates a personalized explanation of why you'll enjoy that specific film based on your query.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq — LLaMA 3.3 70B Versatile |
| Vector Search | FAISS (Facebook AI Similarity Search) |
| Embeddings | Sentence Transformers — `all-MiniLM-L6-v2` |
| Movie Data | TMDB API (live, 4100+ movies) |
| Database | Supabase — PostgreSQL |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Architecture
User Query (natural language / mood / chat)
│
▼
┌───────────────┐
│  Mood Mapper  │  ← Groq LLM maps mood to search query
└───────┬───────┘
│
▼
┌───────────────┐
│  FAISS Index  │  ← Semantic similarity search over 4100+ movie embeddings
└───────┬───────┘
│
▼
┌───────────────┐
│  Top-K Movies │  ← Retrieved from Supabase PostgreSQL
└───────┬───────┘
│
▼
┌───────────────┐
│  Groq LLM     │  ← Generates personalized "why you'll love it" explanation
└───────┬───────┘
│
▼
┌───────────────┐
│ Streamlit UI  │  ← Renders movie cards with posters, metadata, explanations
└───────────────┘

---

## Project Structure
CineAI/
├── app.py                  # Streamlit UI — search, mood, chat modes
├── requirements.txt
├── embeddings/
│   ├── faiss_index.bin     # Pre-built FAISS vector index
│   └── movies_data.pkl     # Movie metadata cache
└── modules/
├── config.py           # Secrets management (local + Streamlit Cloud)
├── db.py               # Supabase PostgreSQL connection + table setup
├── fetcher.py          # TMDB API → fetch and store movies
├── embedder.py         # Build FAISS index from DB movies
├── retriever.py        # Semantic search logic
├── mood_mapper.py      # Mood → genre/tone mapping via Groq
└── chatbot.py          # Multi-turn conversation logic

---

## Local Setup

**Clone the repo**
```bash
git clone https://github.com/Sarthak1708/CineMatch.git
cd CineMatch
```

**Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Create `.env` file**
DATABASE_URL=your_supabase_connection_string
TMDB_API_KEY=your_tmdb_api_key
TMDB_ACCESS_TOKEN=your_tmdb_access_token
GROQ_API_KEY=your_groq_api_key

**Set up database and fetch data**
```bash
python modules/db.py
python modules/fetcher.py
python modules/embedder.py
```

**Run the app**
```bash
streamlit run app.py
```

---

## API Keys Required

| Service | Purpose | Free Tier |
|---|---|---|
| [TMDB](https://www.themoviedb.org/settings/api) | Movie data + posters | Yes |
| [Groq](https://console.groq.com) | LLM inference | Yes |
| [Supabase](https://supabase.com) | PostgreSQL database | Yes (500MB) |

---

## Author

**Sarthak Patel**
Final Year B.Tech CSE — Medi-Caps University, Indore

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sarthak%20Patel-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/sarthak-patel-415533250)
[![GitHub](https://img.shields.io/badge/GitHub-Sarthak1708-181717?style=flat&logo=github&logoColor=white)](https://github.com/Sarthak1708)

---

<div align="center">
<sub>Built with Python · Groq · FAISS · Streamlit · Supabase</sub>
</div>
