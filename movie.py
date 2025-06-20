import pickle
import pandas as pd
import streamlit as st # type: ignore
import requests

# TMDB API Key

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"  

# Cached Helper Function to Fetch Poster

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return "https://via.placeholder.com/300x450.png?text=API+Error"

        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for {movie_id}: {e}")
        return "https://via.placeholder.com/300x450.png?text=Error"


def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# Load Data

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 MovieHelper: A Recommender System")

try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
except FileNotFoundError:
    st.error("Required files not found. Please make sure `movie_dict.pkl` and `similarity.pkl` are in the same folder.")
    st.stop()


selected_movie = st.selectbox(
    "🎥 Type or select a movie:",
    movies['title'].values
)

if st.button('📽 Show Recommendations'):
    with st.spinner("Fetching recommendations and posters..."):
        names, posters = recommend(selected_movie)

    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                # fallback if poster is unavailable
                if posters[i].endswith("Error") or posters[i].endswith("No+Image"):
                    st.image("https://via.placeholder.com/300x450.png?text=Poster+Unavailable")
                else:
                    st.image(posters[i])
                st.caption(names[i])
    else:
        st.warning("No recommendations found. Try selecting another movie.")
