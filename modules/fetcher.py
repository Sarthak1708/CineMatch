import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import os
import time
from dotenv import load_dotenv
from modules.db import get_connection

load_dotenv()

from modules.config import get_secret
ACCESS_TOKEN = get_secret("TMDB_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}

BASE_URL = "https://api.themoviedb.org/3"


def get_genres():
    url = f"{BASE_URL}/genre/movie/list"
    res = requests.get(url, headers=HEADERS)
    genres = res.json().get("genres", [])
    return {g["id"]: g["name"] for g in genres}


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?append_to_response=credits,keywords"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def fetch_and_store_movies(total_pages=100):
    genre_map = get_genres()
    conn = get_connection()
    cur = conn.cursor()
    stored = 0

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}/discover/movie?sort_by=popularity.desc&page={page}&vote_count.gte=100"
        res = requests.get(url, headers=HEADERS)
        movies = res.json().get("results", [])

        for movie in movies:
            try:
                details = get_movie_details(movie["id"])

                title = details.get("title", "")
                overview = details.get("overview", "")
                rating = details.get("vote_average", 0.0)
                popularity = details.get("popularity", 0.0)
                poster_path = details.get("poster_path", "")

                release_year = None
                release_date = details.get("release_date", "")
                if release_date:
                    release_year = int(release_date[:4])

                genres = ", ".join([
                    genre_map.get(g["id"], "") 
                    for g in details.get("genres", [])
                ])

                keywords = ", ".join([
                    kw["name"] 
                    for kw in details.get("keywords", {}).get("keywords", [])[:10]
                ])

                credits = details.get("credits", {})
                movie_cast = ", ".join([
                    c["name"] 
                    for c in credits.get("cast", [])[:5]
                ])

                director = ""
                for crew in credits.get("crew", []):
                    if crew["job"] == "Director":
                        director = crew["name"]
                        break

                cur.execute("""
                    INSERT INTO movies (tmdb_id, title, overview, genres, keywords, movie_cast, director, release_year, rating, poster_path, popularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (tmdb_id) DO NOTHING;
                """, (
                    details["id"], title, overview, genres, keywords,
                    movie_cast, director, release_year, rating, poster_path, popularity
                ))

                stored += 1

            except Exception as e:
                print(f"⚠️ Skipped movie: {e}")
                continue

        conn.commit()
        print(f"✅ Page {page}/{total_pages} done — {stored} movies stored so far")
        time.sleep(0.3)

    cur.close()
    conn.close()
    print(f"\n🎬 Done! Total movies stored: {stored}")


if __name__ == "__main__":
    fetch_and_store_movies(total_pages=250)