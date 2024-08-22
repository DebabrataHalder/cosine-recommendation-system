import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Fetch the API key from the .env file
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# App title
st.title('🎥 Movie Recommender System')

# Sidebar for movie selection
st.sidebar.header('Select a Movie')
# movies = pickle.load(open('recommendation_system-movies/movie_list.pkl', 'rb'))
# similarity = pickle.load(open('recommendation_system-movies/similarity.pkl', 'rb'))
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.sidebar.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

st.sidebar.markdown("Click the button below to get movie recommendations.")

if st.sidebar.button('Show Recommendation'):
    with st.spinner('Finding the best recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    st.header(f"Movies similar to **{selected_movie}**")
    
    # Custom CSS for better font styling
    st.markdown(
        """
        <style>
        .movie-title {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display recommendations with improved font styling
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        st.image(recommended_movie_posters[0], use_column_width=True)
        st.markdown(f"<div class='movie-title'>{recommended_movie_names[0]}</div>", unsafe_allow_html=True)
    
    with col2:
        st.image(recommended_movie_posters[1], use_column_width=True)
        st.markdown(f"<div class='movie-title'>{recommended_movie_names[1]}</div>", unsafe_allow_html=True)
    
    with col3:
        st.image(recommended_movie_posters[2], use_column_width=True)
        st.markdown(f"<div class='movie-title'>{recommended_movie_names[2]}</div>", unsafe_allow_html=True)
    
    with col4:
        st.image(recommended_movie_posters[3], use_column_width=True)
        st.markdown(f"<div class='movie-title'>{recommended_movie_names[3]}</div>", unsafe_allow_html=True)
    
    with col5:
        st.image(recommended_movie_posters[4], use_column_width=True)
        st.markdown(f"<div class='movie-title'>{recommended_movie_names[4]}</div>", unsafe_allow_html=True)
else:
    st.write("Use the sidebar to select a movie and get recommendations.")