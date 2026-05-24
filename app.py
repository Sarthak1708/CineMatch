import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import json
from modules.retriever import search
from modules.mood_mapper import map_mood_to_query
from modules.chatbot import chat, stream_chat, generate_explanation
from modules.db import get_connection
from groq import Groq
from modules.config import get_secret
client = Groq(api_key=get_secret("GROQ_API_KEY"))

st.set_page_config(
    page_title="CineAI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #080810 !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #0d0d18 !important;
    border-right: 1px solid #1e1e30 !important;
}

[data-testid="stSidebar"] * { color: #c8c6d8 !important; }

.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1200px !important;
}

.cine-header {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}

.cine-logo {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #ff4d6d 0%, #ff8fa3 50%, #ffb3c1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.cine-tagline {
    font-size: 0.95rem;
    color: #6b6880;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 400;
}

.divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #ff4d6d, transparent);
    margin: 1.5rem auto;
}

.mode-pill {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: #1a1a28;
    border: 1px solid #2a2a3d;
    color: #ff4d6d;
    margin-bottom: 1.5rem;
}

.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.25rem;
    margin-top: 1.5rem;
}

.movie-card {
    background: #0f0f1e;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: border-color 0.2s, transform 0.2s;
}

.movie-card:hover {
    border-color: #ff4d6d40;
    transform: translateY(-2px);
}

.card-inner {
    display: flex;
    gap: 0;
    flex: 1;
}

.card-poster {
    width: 110px;
    min-width: 110px;
    background: #1a1a28;
    position: relative;
    overflow: hidden;
}

.card-poster img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.card-poster-placeholder {
    width: 100%;
    height: 100%;
    min-height: 165px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    background: #1a1a28;
    color: #2a2a3d;
}

.card-body {
    padding: 1rem 1rem 0.75rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #f0eef8;
    line-height: 1.3;
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.meta-year {
    font-size: 0.75rem;
    color: #6b6880;
}

.meta-rating {
    font-size: 0.72rem;
    font-weight: 600;
    color: #ff8fa3;
    background: #ff4d6d18;
    border: 1px solid #ff4d6d30;
    padding: 0.15rem 0.5rem;
    border-radius: 100px;
}

.meta-director {
    font-size: 0.72rem;
    color: #6b6880;
    font-style: italic;
}

.card-genres {
    font-size: 0.72rem;
    color: #9b98b0;
    line-height: 1.4;
}

.card-overview {
    font-size: 0.78rem;
    color: #7a7890;
    line-height: 1.5;
    flex: 1;
}

.card-explanation {
    margin-top: 0.75rem;
    padding: 0.75rem 1rem;
    background: #13131f;
    border-top: 1px solid #1e1e30;
    border-left: 3px solid #ff4d6d;
    font-size: 0.8rem;
    color: #c0bdd0;
    line-height: 1.6;
}

.ai-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #ff4d6d;
    margin-bottom: 0.3rem;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0eef8;
    margin-bottom: 0.25rem;
}

.section-sub {
    font-size: 0.82rem;
    color: #6b6880;
    margin-bottom: 1.25rem;
}

.mood-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
    margin: 1rem 0;
}

.mood-chip {
    padding: 0.65rem 1rem;
    background: #0f0f1e;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    font-size: 0.82rem;
    color: #c0bdd0;
    cursor: pointer;
    text-align: center;
    transition: all 0.15s;
}

.mood-chip:hover, .mood-chip.selected {
    border-color: #ff4d6d;
    color: #ff8fa3;
    background: #ff4d6d0d;
}

.chat-wrap {
    background: #0d0d18;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 1.25rem;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.chat-msg-user {
    align-self: flex-end;
    background: #1a1a30;
    border: 1px solid #2a2a40;
    border-radius: 12px 12px 2px 12px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #e8e6f0;
    max-width: 75%;
}

.chat-msg-bot {
    align-self: flex-start;
    background: #ff4d6d12;
    border: 1px solid #ff4d6d25;
    border-radius: 2px 12px 12px 12px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #e8e6f0;
    max-width: 75%;
}

.chat-sender {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

.user-sender { color: #6b6880; }
.bot-sender { color: #ff4d6d; }

.result-count {
    font-size: 0.8rem;
    color: #6b6880;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1e1e30;
}

.result-count span { color: #ff8fa3; font-weight: 600; }

.stat-box {
    background: #0f0f1e;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}

.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #ff8fa3;
}

.stat-label {
    font-size: 0.7rem;
    color: #6b6880;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 900;
    color: #ff4d6d !important;
    margin-bottom: 0.25rem;
}

.sidebar-tagline {
    font-size: 0.72rem;
    color: #3d3d55 !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.5rem;
}

.mood-insight {
    background: #0f0f1e;
    border: 1px solid #1e1e30;
    border-left: 3px solid #ff4d6d;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1rem;
    margin-bottom: 1.25rem;
    font-size: 0.82rem;
    color: #9b98b0;
    line-height: 1.6;
}

.mood-insight strong { color: #ff8fa3; font-weight: 500; }

div[data-testid="stTextInput"] input {
    background-color: #0f0f1e !important;
    color: #e8e6f0 !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 10px !important;
    padding: 0.65rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #ff4d6d !important;
    box-shadow: 0 0 0 3px #ff4d6d15 !important;
}

div[data-testid="stTextInput"] input::placeholder { color: #3d3d55 !important; }

.stButton > button {
    background: linear-gradient(135deg, #ff4d6d, #ff1744) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    transition: opacity 0.15s !important;
    width: 100% !important;
}

.stButton > button:hover { opacity: 0.88 !important; }

div[data-testid="stSelectbox"] > div > div {
    background-color: #0f0f1e !important;
    color: #e8e6f0 !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 10px !important;
}

.stSpinner > div { border-top-color: #ff4d6d !important; }

hr { border-color: #1e1e30 !important; }

p, div, span, label { font-family: 'DM Sans', sans-serif !important; }

[data-testid="stMarkdownContainer"] p { color: #9b98b0; }

.stSelectbox label, .stTextInput label {
    color: #6b6880 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w300"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_movies" not in st.session_state:
    st.session_state.chat_movies = []
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

def save_search(query, mode, results):
    try:
        conn = get_connection()
        cur = conn.cursor()
        titles = json.dumps([r["title"] for r in results])
        cur.execute(
            "INSERT INTO search_history (query, mode, results) VALUES (%s, %s, %s)",
            (query, mode, titles)
        )
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass

def render_movie_card(movie, query, show_explanation=True):
    poster_html = ""
    if movie.get("poster_path"):
        poster_html = f'<img src="{TMDB_IMAGE_BASE}{movie["poster_path"]}" alt="{movie["title"]}">'
    else:
        poster_html = '<div class="card-poster-placeholder">🎬</div>'

    overview = movie.get("overview", "")
    if overview and len(overview) > 120:
        overview = overview[:120] + "..."

    rating = movie.get("rating", 0)
    rating_display = f"★ {round(rating, 1)}" if rating else ""

    director_html = f"<span class='meta-director'>dir. {movie.get('director', '')}</span>" if movie.get("director") else ""
    rating_html = f"<span class='meta-rating'>{rating_display}</span>" if rating_display else ""
    overview_html = f"<div class='card-overview'>{overview}</div>" if overview else ""

    st.markdown(f"""
    <div class="movie-card">
        <div class="card-inner">
            <div class="card-poster">{poster_html}</div>
            <div class="card-body">
                <div class="card-title">{movie.get("title", "Unknown")}</div>
                <div class="card-meta">
                    <span class="meta-year">{movie.get("release_year", "")}</span>
                    {rating_html}
                    {director_html}
                </div>
                <div class="card-genres">{movie.get("genres", "")}</div>
                {overview_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_explanation:
        with st.spinner("✦ Generating explanation..."):
            explanation = generate_explanation(movie, query)
        st.markdown(f"""
        <div style="margin-top:-1rem;margin-bottom:1.25rem;padding:0.75rem 1rem;
        background:#13131f;border:1px solid #1e1e30;border-left:3px solid #ff4d6d;
        border-radius:0 0 16px 16px;font-size:0.8rem;color:#c0bdd0;line-height:1.6;">
            <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;
            text-transform:uppercase;color:#ff4d6d;margin-bottom:0.3rem;">✦ Why you'll love it</div>
            {explanation}
        </div>
        """, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>CineAI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-tagline'>AI-powered discovery</div>", unsafe_allow_html=True)

    mode = st.selectbox(
        "Navigation",
        ["🔍 Search", "😊 Mood", "💬 Chat"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#3d3d55;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>Database</div>", unsafe_allow_html=True)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM movies")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM search_history")
        searches = cur.fetchone()[0]
        cur.close()
        conn.close()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='stat-box'><div class='stat-num'>{total:,}</div><div class='stat-label'>Movies</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-box'><div class='stat-num'>{searches}</div><div class='stat-label'>Searches</div></div>", unsafe_allow_html=True)
    except:
        pass

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#3d3d55;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Stack</div>", unsafe_allow_html=True)
    for item in ["FAISS · Semantic Search", "Groq · LLaMA 3.3 70B", "TMDB · Movie Data", "Supabase · PostgreSQL"]:
        st.markdown(f"<div style='font-size:0.75rem;color:#3d3d55;padding:0.25rem 0;'>→ {item}</div>", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="cine-header">
    <div class="cine-logo">CineAI</div>
    <div class="divider"></div>
    <div class="cine-tagline">Semantic movie discovery · Powered by LLaMA 3.3</div>
</div>
""", unsafe_allow_html=True)

# ── Search Mode ──────────────────────────────────────────────
if mode == "🔍 Search":
    st.markdown("<div class='mode-pill'>Semantic Search</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Find your next film</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Describe a vibe, a story, a feeling — not just a title</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input("", placeholder="e.g. slow burn psychological thriller with unreliable narrator...", label_visibility="collapsed")
    with col2:
        top_k = st.selectbox("", [5, 10, 15], label_visibility="collapsed")

    search_btn = st.button("Search →")

    if search_btn and query:
        with st.spinner("Searching through the index..."):
            results = search(query, top_k=top_k)
            save_search(query, "search", results)

        st.markdown(f"<div class='result-count'>Showing <span>{len(results)}</span> results for &ldquo;{query}&rdquo;</div>", unsafe_allow_html=True)

        for movie in results:
            render_movie_card(movie, query)

# ── Mood Mode ────────────────────────────────────────────────
elif mode == "😊 Mood":
    st.markdown("<div class='mode-pill'>Mood Filter</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>What's the vibe tonight?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Your mood shapes the recommendation</div>", unsafe_allow_html=True)

    moods = [
        ("🎉", "Celebratory", "I'm feeling happy and want something uplifting and fun"),
        ("😢", "Melancholic", "I'm sad and need something comforting and emotional"),
        ("🚀", "Adventurous", "I want high energy action and excitement"),
        ("❤️", "Romantic", "I'm in the mood for love and romance"),
        ("🤯", "Mind-bending", "I want something that will blow my mind"),
        ("😰", "Escapist", "I'm stressed and want to completely escape reality"),
        ("🌅", "Nostalgic", "I want something warm and nostalgic from the past"),
        ("😱", "Thrilled", "I want to be on the edge of my seat with suspense"),
    ]

    cols = st.columns(4)
    selected_preset = None
    for i, (emoji, label, query_text) in enumerate(moods):
        with cols[i % 4]:
            if st.button(f"{emoji} {label}", key=f"mood_{i}"):
                selected_preset = query_text
                st.session_state.selected_mood = query_text

    st.markdown("<div style='margin:1rem 0 0.5rem;font-size:0.78rem;color:#6b6880;text-transform:uppercase;letter-spacing:0.08em;'>Or describe your own mood</div>", unsafe_allow_html=True)
    custom_mood = st.text_input("", placeholder="e.g. I just got out of a long relationship and need catharsis...", label_visibility="collapsed", key="custom_mood")

    mood_to_use = custom_mood if custom_mood else st.session_state.get("selected_mood")

    if mood_to_use:
        if st.button("Find movies for this mood →"):
            with st.spinner("Reading your mood..."):
                mood_result = map_mood_to_query(mood_to_use)
                search_query = mood_result.get("search_query", mood_to_use)
                genres = mood_result.get("genres", [])
                tone = mood_result.get("tone", [])
                avoid = mood_result.get("avoid", [])

            insight = f"<strong>Searching for:</strong> {search_query}<br>"
            if genres:
                insight += f"<strong>Genres:</strong> {', '.join(genres)}&nbsp;&nbsp;"
            if tone:
                insight += f"<strong>Tone:</strong> {', '.join(tone)}"
            st.markdown(f"<div class='mood-insight'>{insight}</div>", unsafe_allow_html=True)

            with st.spinner("Finding the right films..."):
                results = search(search_query, top_k=6)
                save_search(mood_to_use, "mood", results)

            st.markdown(f"<div class='result-count'><span>{len(results)}</span> films matched your mood</div>", unsafe_allow_html=True)
            for movie in results:
                render_movie_card(movie, search_query)

# ── Chat Mode ────────────────────────────────────────────────elif mode == "💬 Chat":
elif mode == "💬 Chat":
    st.markdown("<div class='mode-pill'>Conversational AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Talk to CineAI</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Refine your picks through conversation</div>", unsafe_allow_html=True)

    # Render chat history
    chat_container = '<div class="chat-wrap">'
    if not st.session_state.chat_history:
        chat_container += '<div style="text-align:center;padding:2rem;font-size:0.82rem;color:#3d3d55;">Start a conversation — try "I want something like Parasite but funnier"</div>'
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_container += f'<div class="chat-msg-user"><div class="chat-sender user-sender">You</div>{msg["content"]}</div>'
            else:
                try:
                    content = json.loads(msg["content"])
                    display = content.get("response", msg["content"])
                except:
                    display = msg["content"]
                chat_container += f'<div class="chat-msg-bot"><div class="chat-sender bot-sender">CineAI</div>{display}</div>'
    chat_container += '</div>'
    st.markdown(chat_container, unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="e.g. something like that but with more comedy...", label_visibility="collapsed", key="chat_input")
    with col2:
        send = st.button("Send →")

    col3, col4 = st.columns([1, 5])
    with col3:
        clear = st.button("Clear")

    if send and user_input:
        # Show streaming response
        stream_placeholder = st.empty()
        full_raw = ""

        groq_stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": """You are CineAI, a smart movie recommendation chatbot.
Respond ONLY in this JSON format:
{
    "search_query": "refined movie search query",
    "response": "your conversational response to the user"
}"""}
            ] + st.session_state.chat_history + [{"role": "user", "content": user_input}],
            temperature=0.7,
            stream=True
        )

        for chunk in groq_stream:
            delta = chunk.choices[0].delta.content or ""
            full_raw += delta
            try:
                clean = full_raw.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean)
                display_text = parsed.get("response", "")
            except:
                display_text = full_raw
            stream_placeholder.markdown(
                f"<div class='chat-msg-bot'><div class='chat-sender bot-sender'>CineAI</div>{display_text}▌</div>",
                unsafe_allow_html=True
            )

        # Final parse
        try:
            clean = full_raw.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean)
            search_query = result.get("search_query", user_input)
            final_response = result.get("response", "Here are my recommendations!")
        except:
            search_query = user_input
            final_response = full_raw

        stream_placeholder.markdown(
            f"<div class='chat-msg-bot'><div class='chat-sender bot-sender'>CineAI</div>{final_response}</div>",
            unsafe_allow_html=True
        )

        # Update history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": full_raw})

        # Get movies
        with st.spinner("Finding movies..."):
            movies = search(search_query, top_k=5)
            st.session_state.chat_movies = movies
            save_search(user_input, "chat", movies)

    if clear:
        st.session_state.chat_history = []
        st.session_state.chat_movies = []
        st.rerun()

    if st.session_state.chat_movies:
        st.markdown("---")
        st.markdown(f"<div class='result-count'><span>{len(st.session_state.chat_movies)}</span> recommendations based on your conversation</div>", unsafe_allow_html=True)
        for movie in st.session_state.chat_movies:
            render_movie_card(movie, "chat", show_explanation=False)