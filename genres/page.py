import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from genres.service import GenreService


def show_genres():
    genre_service = GenreService()
    genres = genre_service.get_genres()

    if genres:
        st.header("Lista de Gêneros", divider='violet')
        genres_df = pd.json_normalize(genres)
        AgGrid(
            data=genres_df,
            key='genres_grid',
            fit_columns_on_grid_load=True,
            theme='streamlit',
        )
    else:
        st.warning('Nenhum gênero encontrado!')

    st.header("Novo Gênero", divider='green')
    name = st.text_input('Nome do Gênero', value=None)
    if st.button('Cadastrar'):
        new_genre = genre_service.create_genres(
            name=name,
        )
        if new_genre:
            st.rerun()
        else:
            st.error("Erro ao cadastrar o gênero. Verifique os campos.")
