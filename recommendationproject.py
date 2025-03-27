import streamlit as st
import pickle
import numpy as np
from scipy.sparse import csr_matrix

st.subheader("SPOTIFY")
st.image("/home/adminuser/spotify-deal-page-467x316.jpg")

# Load data
songs = pickle.load(open("songs.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))  # Keep sparse

# Ensure correct formatting
songs["title"] = songs["title"].str.strip().str.lower()
songs_list = songs["title"].tolist()

st.header("Song Recommendation System")
selectvalue = st.selectbox("Select a song", songs_list)

def recommend(song_name):
    song_name = song_name.strip().lower()

    matching_songs = songs[songs['title'] == song_name]
    if matching_songs.empty:
        return ["Song not found"] * 5  

    index = matching_songs.index[0]

    # 🔥 FIX: Use sparse format without converting to a full array
    if isinstance(similarity, csr_matrix):
        distances = similarity[index].toarray().flatten()  # Convert only the needed row
    else:
        distances = similarity[index]

    distances = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)
    recommended_songs = [songs.iloc[i[0]].title for i in distances[1:6]]

    return recommended_songs

if st.button("Show Recommendations", key="recommend_button"):
    recommendations = recommend(selectvalue)

    # Debugging output
    st.write(f"Selected song: {selectvalue}")
    st.write(f"Recommendations: {recommendations}")

    col1, col2, col3, col4, col5 = st.columns(5)
    for col, song in zip([col1, col2, col3, col4, col5], recommendations):
        with col:
            st.text(song)

