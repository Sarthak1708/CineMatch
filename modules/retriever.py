import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "embeddings/faiss_index.bin"
MOVIES_PATH = "embeddings/movies_data.pkl"

model = SentenceTransformer(MODEL_NAME)

def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(MOVIES_PATH, "rb") as f:
        movies = pickle.load(f)
    return index, movies

def search(query, top_k=10):
    index, movies = load_index()

    query_vec = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        movie = movies[idx]
        movie["score"] = float(scores[0][i])
        results.append(movie)

    return results

if __name__ == "__main__":
    results = search("mind bending thriller with a twist ending")
    for r in results:
        print(f"{r['title']} ({r['release_year']}) — Score: {r['score']:.4f}")