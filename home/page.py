import streamlit as st
import plotly.express as px
from movies.service import MovieService


def show_home():
    st.header("Estatísticas", divider='violet')
    movie_service = MovieService()
    movie_stats = movie_service.get_movie_stats()

    st.subheader("Filmes Cadastrados", divider='gray')
    st.write(movie_stats['total_movies'])

    if len(movie_stats['movies_by_genre']) > 0:
        st.subheader("Filmes por Gênero", divider='gray')
        fig = px.pie(
            movie_stats['movies_by_genre'],
            values='count',
            names='genre__name'
        )
        st.plotly_chart(fig)

    for genre in movie_stats['movies_by_genre']:
        st.write(f'{genre['genre__name']}: {genre['count']}')

    st.subheader("Avaliações Cadastradas", divider='gray')
    st.write(movie_stats['total_reviews'])

    st.subheader("Média de Estrelas nas Avaliações", divider='gray')
    st.write(movie_stats['average_stars'])
