import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity_matrix = pickle.load(open("similarity_matrix.pkl","rb"))

# To Fetch the poster of movie from API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=334db36a3683594babb178c37b907b08'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

# Function to show top 5 recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse= True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters

# Streamlit
st.title("Movie Recommender System")

select_movies = st.selectbox("Movie Name", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(select_movies)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    for x,y in enumerate([col1, col2, col3, col4, col5]):
        with y:
            st.text(names[x])
            st.image(posters[x])

