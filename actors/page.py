import pandas as pd
import streamlit as st
from datetime import datetime
from st_aggrid import AgGrid
from actors.service import ActorService


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()

    st.header("Lista de Atores/Atrizes", divider='violet')

    actors_df = pd.json_normalize(actors)
    if actors:
        AgGrid(
            data=actors_df,
            key='genres_grid',
            fit_columns_on_grid_load=True,
            theme='streamlit',
        )
    else:
        st.warning('Nenhum ator/atriz encontrado!')

    st.header("Novo(a) Ator/Atriz", divider='green')
    name = st.text_input('Nome do Ator/Atriz')
    birthday = st.date_input(
        label='Data de Nascimento',
        value=datetime.today(),
        min_value=datetime(1800, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY',
    )
    nationality_dropdown = ['BRAZIL', 'USA']
    nationality = st.selectbox(
        label='Nacionalidade',
        options=nationality_dropdown,
    )
    if st.button('Cadastrar'):
        new_actor = actor_service.create_actor(
            name=name,
            birthday=birthday,
            nationality=nationality
        )
        if new_actor:
            st.rerun()
        else:
            st.error('Erro ao cadastrar o(a) Ator/Atriz. Verifique os campos.')
