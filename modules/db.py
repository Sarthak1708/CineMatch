import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

from modules.config import get_secret
DATABASE_URL = get_secret("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def setup_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            tmdb_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            overview TEXT,
            genres TEXT,
            keywords TEXT,
            movie_cast TEXT,
            director TEXT,
            release_year INTEGER,
            rating FLOAT,
            poster_path TEXT,
            popularity FLOAT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            mode TEXT,
            results TEXT,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    setup_tables()