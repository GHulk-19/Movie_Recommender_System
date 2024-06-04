import requests
import streamlit as st
import pickle
import pandas as pd

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style', unsafe_allow_html=True)

page_bg= """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://e1.pxfuel.com/desktop-wallpaper/544/126/desktop-wallpaper-related-keywords-suggestions-for-movie-theater-backgrounds-1215x734-for-your-mobile-tablet-movie-screen.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown("""
<style>
.title, h1 {
    color: white;
    text-align: center;
    font-size: 3em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}
.white-text{
    color: white;
    font-size: 1.2em;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}
.stSelectbox > div > div {
    color: red;
    font-size: 1.2em;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}

.stSelectbox label {
    color: white;
    font-size: 1.2em;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}
.stButton>button {
    color: white;
    background-color: #007BFF;
    border: none;
    padding: 0.5em 1em;
    font-size: 1.2em;
    border-radius: 0.3em;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #0056b3;
    color:white;
}
</style>
""", unsafe_allow_html=True)


st.title("Movie Recommender System")


movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name= st.selectbox("Enter your Choice",movies['title'].values,placeholder="Select...")

def fetch_poster(movie_id):
    url='https://api.themoviedb.org/3/movie/{}?api_key=4dad15e7d607734bfef81e0ddebc32b6&language=en-US'.format(movie_id)
    data=requests.get(url)
    data=data.json()

    poster_path=data['poster_path']
    print(poster_path)
    full_path="https://image.tmdb.org/t/p/w500/"+ poster_path
    print(full_path)
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:

        #fetch the movie titles
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch the poster from API
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


if st.button('Recommend'):
    names, posters =recommend(selected_movie_name)
    num_columns= len(names)

    columns= st.columns(num_columns)

    for i in range(num_columns):
        with columns[i]:
            # st.write(names[i])
            st.image(posters[i])
            st.markdown(f'<div class="white-text">{names[i]}</div>', unsafe_allow_html=True)




