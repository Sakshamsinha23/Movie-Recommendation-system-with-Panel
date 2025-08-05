# 🎬 Movie Recommender System

A smart movie recommender app built with Streamlit. Suggests top 5 similar movies using content-based filtering and cosine similarity. Posters are fetched from TMDB.

## 🔧 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

- `app.py` – Streamlit app
- `requirements.txt` – Python dependencies
- `model/movie_list.pkl` – Movie list data
- `model/similarity.pkl` – Cosine similarity matrix
