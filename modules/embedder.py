import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from modules.db import get_connection
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "embeddings/faiss_index.bin"
MOVIES_PATH = "embeddings/movies_data.pkl"

def build_index():
    print("📦 Loading movies from DB...")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT tmdb_id, title, overview, genres, keywords, movie_cast, director, release_year, rating, poster_path
        FROM movies
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"✅ {len(rows)} movies loaded.")

    movies = []
    texts = []

    for row in rows:
        tmdb_id, title, overview, genres, keywords, movie_cast, director, release_year, rating, poster_path = row
        text = f"{title}. {genres}. {overview}. Keywords: {keywords}. Cast: {movie_cast}. Director: {director}."
        texts.append(text)
        movies.append({
            "tmdb_id": tmdb_id,
            "title": title,
            "overview": overview,
            "genres": genres,
            "keywords": keywords,
            "movie_cast": movie_cast,
            "director": director,
            "release_year": release_year,
            "rating": rating,
            "poster_path": poster_path
        })

    print("🔢 Generating embeddings...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(MOVIES_PATH, "wb") as f:
        pickle.dump(movies, f)

    print(f"✅ FAISS index built with {index.ntotal} vectors.")
    print(f"✅ Saved to {INDEX_PATH}")

if __name__ == "__main__":
    build_index()