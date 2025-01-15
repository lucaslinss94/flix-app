import pandas as pd
import streamlit as st
from datetime import datetime
from actors.service import ActorService
from genres.service import GenreService
from st_aggrid import AgGrid
from movies.service import MovieService


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    movies_df = pd.json_normalize(movies)
    movies_df = movies_df.drop(columns=['actors', 'genre.id'])

    st.header("Lista de Filmes", divider='violet')

    if movies:
        AgGrid(
            data=movies_df,
            key='genres_grid',
            fit_columns_on_grid_load=True,
            theme='streamlit',
        )
    else:
        st.warning('Nenhum filme encontrado!')

    st.header("Novo Filme", divider='green')

    title = st.text_input('Título')

    release_date = st.date_input(
        label='Data de Lançamento',
        value=datetime.today(),
        min_value=datetime(1800, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY',
    )

    release_date_f = release_date.strftime("%Y-%m-%d")

    genre_service = GenreService()
    genres = genre_service.get_genres()
    genre_names = {genre['name']: genre['id'] for genre in genres}
    selected_genre_name = st.selectbox('Gênero', list(genre_names.keys()))

    actor_service = ActorService()
    actors = actor_service.get_actors()
    actor_names = {actor['name']: actor['id'] for actor in actors}
    selected_actor_name = st.multiselect('Atores/Atrizes', list(actor_names.keys()))
    selected_actors_ids = [actor_names[name] for name in selected_actor_name]

    resume = st.text_area('Resumo')

    if st.button('Cadastrar'):
        new_movie = movie_service.create_movie(
            title=title,
            release_date=release_date_f,
            genre=genre_names[selected_genre_name],
            actors=selected_actors_ids,
            resume=resume,
        )
        if new_movie:
            st.rerun()
        else:
            st.error("Erro ao cadastrar o gênero. Verifique os campos.")
