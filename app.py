import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
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

# Define model paths
model_dir = os.path.join(os.path.dirname(__file__), 'model')
movie_list_path = os.path.join(model_dir, 'movie_list.pkl')
similarity_path = os.path.join(model_dir, 'similarity.pkl')

# Show readable error if loading fails
try:
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError as fnf_err:
    st.error(f"❌ File not found:\n\n{fnf_err}")
    st.stop()
except ModuleNotFoundError as mod_err:
    st.error(f"❌ Module not found during unpickling:\n\n{mod_err}\n\nTry saving the .pkl again using standard pandas/NumPy objects.")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error:\n\n{e}")
    st.stop()

# App UI
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
