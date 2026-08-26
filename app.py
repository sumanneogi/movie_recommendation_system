import streamlit as st
import pickle 
import requests    # To hit the API and fetch data
# from dotenv import load_dotenv
# import os


# """ Local development:
# The API key can be stored in a .env file and loaded using python-dotenv.
# These lines are kept commented out because the deployed Streamlit app retrieves the API key from Streamlit Secrets."""

# load_dotenv()     # Load the .env file
# OMDB_API_KEY = os.getenv("OMDB_API_KEY")   # Retrieve the API key securely


# In the deployed Streamlit app, the API key is retrieved from Streamlit Secrets.
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]


# Load movie dataset
movies_df = pickle.load(open('Dataset/movies.pkl','rb'))
movies_list = movies_df['title'].values

# Load similarity matrix
similarity = pickle.load(open('Dataset/similarity.pkl','rb'))


def fetch_poster(movie_name):
    response = requests.get('https://www.omdbapi.com/?t={}&apikey={}'.format(movie_name, OMDB_API_KEY))
    data = response.json()
    return data['Poster']


def recommend(movie):
    # Find the index of the movie whose title matches 'movie'
    movie_index = movies_df[movies_df['title'] == movie].index[0]        

    # Get similarity scores for the selected movie
    distances = similarity[movie_index]

    # Sort movies by similarity and take the top 5 similar movies
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6] 

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch movie poster from API
        recommended_movies_posters.append(fetch_poster(movies_df.iloc[i[0]].title))
    return recommended_movies, recommended_movies_posters

    

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies_list,
)


st.markdown("""
<style>
.movie-title { height: 50px; }
</style>
""", unsafe_allow_html=True)


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="movie-title">{names[0]}</div>', unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f'<div class="movie-title">{names[1]}</div>', unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f'<div class="movie-title">{names[2]}</div>', unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f'<div class="movie-title">{names[3]}</div>', unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f'<div class="movie-title">{names[4]}</div>', unsafe_allow_html=True)
        st.image(posters[4])



# Project information

st.markdown("<br> <br>", unsafe_allow_html=True)


with st.container(border=True):
    st.markdown(
        """
        ##### 🧭 About the Project
        This web application recommends the top 5 movies similar to a movie selected by the user when they click the \"Recommend\" button.
        
        ##### 💻 Source Code
        Please explore the complete project implementation and source code on [GitHub](https://github.com/sumanneogi/movie_recommendation_system).
        
        ##### ❤️ Thank You
        """,
        unsafe_allow_html=False
    )