import pickle
import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv
from requests.exceptions import RequestException

# Load environment variables from .env file
load_dotenv()
tmdb_api_key = os.getenv("TMDB_API_KEY")

# --- Helper Functions ---
def fetch_poster(movie_id):
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
    placeholder = "https://via.placeholder.com/500x750.png?text=No+Poster+Available"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
            return placeholder
        except (RequestException, KeyError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            st.error(f"Failed to fetch poster for movie ID {movie_id}: {str(e)}")
            return placeholder

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        return [
            (movies.iloc[i[0]].title, movies.iloc[i[0]].movie_id)
            for i in distances[1:6]
        ]
    except Exception as e:
        st.error(f"Recommendation error: {str(e)}")
        return []

# --- App Configuration & Styling ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for uniform movie cards
st.markdown(
    """
    <style>
    .movie-card {
        width: 220px;
        height: 350px;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin: 10px auto;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .movie-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 5px;
    }
    .movie-title {
        font-size: 16px;
        font-weight: 600;
        margin-top: 8px;
        color: #333333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    body {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for Navigation ---
st.sidebar.header("Movie Selection")
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.sidebar.selectbox("Choose a movie", movies['title'].values)

if st.sidebar.button("Show Recommendations"):
    recommendations = recommend(selected_movie)
    if not recommendations:
        st.sidebar.warning("Could not generate recommendations.")
    else:
        st.subheader("Recommended Movies")
        # Create a 5-column layout for recommendations
        cols = st.columns(5)
        for idx, (col, (title, movie_id)) in enumerate(zip(cols, recommendations)):
            with col:
                poster_url = fetch_poster(movie_id)
                # Use custom HTML to display each movie card
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster_url}" alt="Poster">
                    <div class="movie-title">{title}</div>
                </div>
                """, unsafe_allow_html=True)
