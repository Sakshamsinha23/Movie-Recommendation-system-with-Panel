import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    api_key = st.secrets.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

model_dir = os.path.join(os.path.dirname(__file__), 'model')
movie_list_path = os.path.join(model_dir, 'movie_list.pkl')
similarity_path = os.path.join(model_dir, 'similarity.pkl')

if not os.path.exists(movie_list_path) or not os.path.exists(similarity_path):
    st.error("Model files not found. Please ensure 'movie_list.pkl' and 'similarity.pkl' exist in the 'model' folder.")
    st.stop()

movies = pickle.load(open(movie_list_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
