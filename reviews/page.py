import pandas as pd
import streamlit as st
from movies.service import MovieService
from reviews.service import ReviewService
from st_aggrid import AgGrid


def show_reviews():
    st.header("Lista de Avaliações", divider='violet')

    review_service = ReviewService()
    reviews = review_service.get_reviews()

    if reviews:
        reviews_df = pd.json_normalize(reviews)

        AgGrid(
            data=reviews_df,
            key='reviews_grid',
            fit_columns_on_grid_load=True,
            theme='streamlit',
        )
    else:
        st.warning("Nenhuma avaliação encontrada!")

    st.header("Nova Avaliação", divider='green')

    movie_service = MovieService()
    movies = movie_service.get_movies()
    movie_titles = {movie['title']: movie['id'] for movie in movies}
    selected_movie_title = st.selectbox('Filme', list(movie_titles.keys()))

    star_rate = [1, 2, 3, 4, 5]
    st.write('Estrelas')
    stars_rated = st.feedback("stars")
    if stars_rated is not None:
        stars = star_rate[stars_rated]

    comment = st.text_area('Comentário')

    if st.button('Cadastrar'):
        new_review = review_service.create_review(
            movie=movie_titles[selected_movie_title],
            stars=stars,
            comment=comment,
        )
        if new_review:
            st.rerun()
        else:
            st.error("Erro ao cadastrar o gênero. Verifique os campos.")
