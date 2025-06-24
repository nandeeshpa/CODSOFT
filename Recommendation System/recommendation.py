import streamlit as st
import pandas as pd

# Load movie data
movies = pd.read_csv("movies.csv")

# Collect all unique genres
all_genres = set()
for g in movies['genres']:
    for genre in g.split('|'):
        all_genres.add(genre.strip())
sorted_genres = sorted(all_genres)

# Page config and style
st.set_page_config(page_title="Movie Genie 🎬", layout="centered")

# Custom CSS for background and styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .stApp {
        background: linear-gradient(to right, #f9f9f9, #f0f2f6);
    }
    .title {
        font-size: 40px;
        text-align: center;
        color: #222222;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .movie-box {
        background-color: white;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 10px;
        box-shadow: 1px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<div class="title">🎥 Movie Genie</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find your favorite movies by genre!</div>', unsafe_allow_html=True)

# Genre Selection
genre_selected = st.selectbox("🎯 Choose a genre to explore:", ["-- Select Genre --"] + sorted_genres)

# Show movies only after a valid selection
if genre_selected != "-- Select Genre --":
    matching_movies = movies[movies['genres'].str.contains(genre_selected, case=False, na=False)]

    if not matching_movies.empty:
        st.write(f"🔎 Showing movies under genre: `{genre_selected}`")
        for movie in matching_movies['title']:
            st.markdown(f"<div class='movie-box'>🎬 {movie}</div>", unsafe_allow_html=True)
    else:
        st.warning("No movies found for this genre 😕")
else:
    st.info("Please select a genre from the dropdown above to get movie recommendations.")
