import streamlit as st
import pandas as pd
import numpy as np


st.title("Comparativo de aproveitamento do Brasileirão")

#Formatação do arquivo
brasileirao_csv = pd.read_csv("campeonato-brasileiro-full.csv")
brasileirao_csv['data'] = pd.to_datetime(brasileirao_csv['data'], format = '%d/%m/%Y')
brasileirao_2003_to_2019 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2003-01-01", "2019-12-31"))]
brasileirao_2020 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2020-01-01", "2021-02-26"))]
brasileirao_2021 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2021-05-01", "2021-12-31"))]


##Função para cálculo de aproveitamento
def calularAproveitamento(totalJogos, vitorias, empates ):
    pontosAtingidos = (vitorias * 3) + empates
    pontosPossiveis = totalJogos * 3
    aproveitamento = int((pontosAtingidos * 100) / pontosPossiveis)
    return aproveitamento

##Aproveitamento por rodadas
def aprovPorRodada (subset, time, partidas):
    arr_aprov = []
    vitoria = 0
    empate = 0
    editedSub = subset[(subset['visitante'] == time) | (subset['mandante'] == time)].sort_values(by = 'ID').reset_index()

    for x in range(partidas):
        total = x + 1
        if editedSub['vencedor'][x] == time:
            vitoria += 1
        elif editedSub['vencedor'][x] == '-':
            empate += 1
        arr_aprov.append(calularAproveitamento(total, vitoria, empate))

    return arr_aprov

##Exbição dos dados
temporada_ano = st.selectbox(
    'Qual temporada gostaria de analisar?',
    (pd.unique(brasileirao_csv['data'].dt.strftime('%Y'))), key = 'temporada_ano')

if temporada_ano == '2020':
    brasileirao_ano = brasileirao_2020.sort_values(by = 'ID').reset_index()
elif temporada_ano == '2021':
    brasileirao_ano = brasileirao_2021.sort_values(by = 'ID').reset_index()
else:
    brasileirao_ano = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == temporada_ano ].sort_values(by = 'ID').reset_index()

clubes = pd.unique(brasileirao_ano['visitante'])

rodada = st.slider("Escolha a rodada:", 1, 38, 38, key = 'rodada')

col1, col2, col3= st.columns(3)

with col1:
    time1 = st.selectbox(
    'Qual o primeiro clube a comparar?',
    (clubes), key = 'time1')

with col2:
   time2 = st.selectbox(
   'Qual o segundo clube a comparar?',
   (clubes), key = 'time2')

with col3:
   time3 = st.selectbox(
   'Qual o terceiro clube a comparar?',
   (clubes), key = 'time3')

brasileirao_2017 = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == '2017' ].sort_values(by = 'ID').reset_index()

primeiroTime= aprovPorRodada(brasileirao_ano, time1, rodada)
segundoTime = aprovPorRodada(brasileirao_ano, time2, rodada)
terceiroTime = aprovPorRodada(brasileirao_ano, time3, rodada)

chart_aprov = pd.DataFrame({
    "Primeiro": primeiroTime,
    "Segundo": segundoTime,
    "Terceiro": terceiroTime,
    })

st.line_chart(chart_aprov)
