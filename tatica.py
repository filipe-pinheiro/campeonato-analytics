import streamlit as st
import pandas as pd
from functions import *


#formatação dos arquivos
brasileirao_csv = pd.read_csv("campeonato-brasileiro-full.csv")
brasileirao_csv['data'] = pd.to_datetime(brasileirao_csv['data'], format = '%d/%m/%Y')
brasileirao_2017 = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == '2017']
brasileirao_2015_to_2022 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2015-01-01", "2022-12-31"))]
brasileirao_2020 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2020-01-01", "2021-02-26"))]
brasileirao_2021 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2021-05-01", "2021-12-31"))]

#Pegar formação tática e fazer um comparativo com o o aproveitamento/gols no decorrer da temporada

##Plotagem dos resultados
st.title("Comparativo tático")

col1, col2 = st.columns(2)

with col1:
    temporada_ano = st.selectbox(
        'Qual temporada gostaria de analisar?', (pd.unique(brasileirao_2015_to_2022['data'].dt.strftime('%Y'))), key = 'temporada_ano')

rodada = st.slider("Escolha a rodada:", 1, 38, 38, key = 'rodada')

if temporada_ano == '2020':
    brasileirao_ano = brasileirao_2020.sort_values(by = 'ID')
elif temporada_ano == '2021':
    brasileirao_ano = brasileirao_2021.sort_values(by = 'ID')
else:
    brasileirao_ano = brasileirao_2015_to_2022[brasileirao_2015_to_2022['data'].dt.strftime('%Y') == temporada_ano ].sort_values(by = 'ID')

with col2:
    todosClubes = st.selectbox(
        'Selecione o time:', (pd.unique(brasileirao_ano['mandante'])), key = 'todosClubes')

subsetClubeMandante = brasileirao_ano[(brasileirao_ano['mandante'] == todosClubes) & (brasileirao_ano['rodata'] <= rodada)]
subsetClubeVisitante = brasileirao_ano[(brasileirao_ano['visitante'] == todosClubes) & (brasileirao_ano['rodata'] <= rodada)]
subsetMandanteEdited = subsetClubeMandante['formacao_mandante']
subsetVisitanteEdited = subsetClubeVisitante['formacao_visitante']

taticaGeral = pd.DataFrame({
    'coluna1': subsetMandanteEdited,
    'coluna2': subsetVisitanteEdited
})

subsetConcat =  pd.concat([taticaGeral['coluna1'], taticaGeral['coluna2']]).value_counts()

contagemGeral = pd.DataFrame(subsetConcat, columns = ['Quatidades'])

st.table(contagemGeral)
st.write("Na temporada houve " + str(len(contagemGeral)) + " táticas que o(s) treinador(es) puseram")

