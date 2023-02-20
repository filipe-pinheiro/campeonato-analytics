import streamlit as st
import pandas as pd
from functions import *

st.title("Aproveitamento como mandante:")

#Formatação do arquivo
brasileirao_csv = pd.read_csv("campeonato-brasileiro-full.csv")
brasileirao_csv['data'] = pd.to_datetime(brasileirao_csv['data'], format = '%d/%m/%Y')
brasileirao_2017 = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == '2017']
rasileirao_2003_to_2019 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2003-01-01", "2019-12-31"))]
brasileirao_2020 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2020-01-01", "2021-02-26"))]
brasileirao_2021 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2021-05-01", "2021-12-31"))]

 ##Cálculo do aproveitamento e mando de campo
#st.dataframe(brasileirao_2017)

#print(aprovPorRodada(brasileirao_2017, 'Sao Paulo', 11))

def aprovPorMandante(subset, time, rodada):
    vitoria = 0
    empate = 0
    editedByRodata = subset[subset['rodata'] <= rodada].sort_values(by = 'ID').reset_index()
    mandanteSubset = editedByRodata[editedByRodata['mandante'] == time].sort_values(by = 'ID').reset_index()
    totalJogosMandante = len(mandanteSubset)

    for x in range(totalJogosMandante):
        if mandanteSubset['vencedor'][x] == time:
            vitoria += 1
        elif mandanteSubset['vencedor'][x] == '-':
            empate += 1

    return calularAproveitamento(totalJogosMandante, vitoria, empate)

def aprovPorVisitante(subset, time, rodada):
    vitoria = 0
    empate = 0
    editedByRodata = subset[subset['rodata'] <= rodada].sort_values(by = 'ID').reset_index()
    visitanteSubset = editedByRodata[editedByRodata['visitante'] == time].sort_values(by = 'ID').reset_index()
    totalJogosVisitante = len(visitanteSubset)

    for x in range(totalJogosVisitante):
        if visitanteSubset['vencedor'][x] == time:
            vitoria += 1
        elif visitanteSubset['vencedor'][x] == '-':
            empate += 1

    return calularAproveitamento(totalJogosVisitante, vitoria, empate)

##Plot dos resultados
temporada_ano = st.selectbox(
    'Qual temporada gostaria de analisar?',
    (pd.unique(brasileirao_csv['data'].dt.strftime('%Y'))), key = 'temporada_ano')

if temporada_ano == '2020':
    brasileirao_ano = brasileirao_2020.sort_values(by = 'ID')
elif temporada_ano == '2021':
    brasileirao_ano = brasileirao_2021.sort_values(by = 'ID')
else:
    brasileirao_ano = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == temporada_ano ].sort_values(by = 'ID')

todosClubes = pd.unique(brasileirao_ano['mandante'])

def aprovTodosClubes():
    arr_values = []

    for x in range (len(todosClubes)):
        arr_values.append([todosClubes[x]])
        arr_values[x].extend((aprovPorRodada(brasileirao_ano, todosClubes[x], 38 )[0][-1], aprovPorMandante(brasileirao_ano, todosClubes[x], 38), aprovPorVisitante(brasileirao_ano, todosClubes[x], 38)))


    return arr_values

df = pd.DataFrame(aprovTodosClubes(),columns=['Time', 'Aprov. Geral(%)', 'Aprov. Casa(%)', 'Aprov. Fora(%)'])

st.table(df.sort_values(by = ['Aprov. Geral(%)'], ascending=False).reset_index(drop = True))
#print(aprovTodosClubes())
#print(brasileirao_ano)
