import pickle
import pandas as pd
import streamlit as st
import requests
import os

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Dropbox direct download URLs
DROPBOX_LINKS = {
    "movie_dict.pkl": "https://www.dropbox.com/scl/fi/hmprp1ttbofwdjuowca95/movie_dict.pkl?rlkey=jb4jn0jsk6y935ogqaewdv1y0&st=038jvsk2&dl=1",
    "similarity.pkl": "https://www.dropbox.com/scl/fi/rkae7cqrzf44ax5gsh35e/similarity.pkl?rlkey=2z60rnol2uww40m0hx6s9b9lt&st=retkjr9f&dl=1"
}

def download_file(url, destination):
    response = requests.get(url, stream=True)
    if "text/html" in response.headers.get("Content-Type", ""):
        raise ValueError(f" Download failed: received HTML instead of file from {url}")
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

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
    names, posters = [], []
    for i in distances[1:6]:
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movies.iloc[i[0]].id))
    return names, posters

# STREAMLIT APP 
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 MovieHelper: A Recommender System")

for fname, url in DROPBOX_LINKS.items():
    if not os.path.exists(fname):
        st.info(f"📥 Downloading {fname} from Dropbox...")
        try:
            download_file(url, fname)
        except Exception as e:
            st.error(f"Failed to download {fname}: {e}")
            st.stop()

try:
    movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    movies = pd.DataFrame(movie_dict)
except Exception as e:
    st.error(f"❌ Error loading files: {e}")
    st.stop()

selected_movie = st.selectbox("🎥 Type or select a movie:", movies['title'].values)

if st.button("📽 Show Recommendations"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie)
    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
    else:
        st.warning("No recommendations found.")
