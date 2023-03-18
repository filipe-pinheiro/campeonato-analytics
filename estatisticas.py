import streamlit as st
import pandas as pd
import numpy as np
from functions import *

#Read csv
brasileirao_csv = pd.read_csv("campeonato-brasileiro-full.csv")
brasileirao_csv['data'] = pd.to_datetime(brasileirao_csv['data'], format = '%d/%m/%Y')
brasileirao_2020 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2020-01-01", "2021-02-26"))]
brasileirao_2021 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2021-05-01", "2021-12-31"))]
brasileirao_2015_to_2022 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2015-01-01", "2022-12-31"))]
estatisticas_csv = pd.read_csv("campeonato-brasileiro-estatisticas-full.csv")

#Streamlit
temporada_ano = st.selectbox(
    'Qual temporada gostaria de analisar?', (pd.unique(brasileirao_2015_to_2022['data'].dt.strftime('%Y'))), key = 'temporada_ano')

if temporada_ano == '2020':
    brasileirao_ano = brasileirao_2020.sort_values(by = 'ID')
elif temporada_ano == '2021':
    brasileirao_ano = brasileirao_2021.sort_values(by = 'ID')
else:
    brasileirao_ano = brasileirao_2015_to_2022[brasileirao_2015_to_2022['data'].dt.strftime('%Y') == temporada_ano ].sort_values(by = 'ID')


#Filtrar estatísticas de um time 
def statsTable(table, time):

    subSetTime = table[(table['visitante'] == time) | (table['mandante'] == time)].sort_values(by = 'ID').reset_index()

    data = []

    for x in range(len(subSetTime)):
       df2 = estatisticas_csv[(estatisticas_csv['partida_id'].isin([subSetTime['ID'][x]])) & (estatisticas_csv['clube'] == time)]
       data.append(df2)

    return pd.concat(data).reset_index()

time = 'Sao Paulo'
timeStats = statsTable(brasileirao_ano, time)

#Relacionar Posse de bola, precisão e chute a gols
timeStats['posse_de_bola'] = timeStats['posse_de_bola'].str[:-1]
timeStats['posse_de_bola'] = pd.to_numeric(timeStats['posse_de_bola'], errors='coerce')
timeStats['posse_de_bola'] = timeStats['posse_de_bola'].fillna(0).astype(int)
st.write("O tem uma média de poss de bola de ", str(round(timeStats['posse_de_bola'].mean(), 2)))
st.write("O time passou ", str(len(timeStats[timeStats['posse_de_bola'] >= 50])), "jogos acima dos 50%")

def precisaoTime(table):

    arrPrecisao = []
    clubes = table['mandante'].unique()
    dataPrecisao = []
    
    for y in range(len(clubes)):
        arrPrecisao = []
        clubeStats = statsTable(table, clubes[y])

        for x in range(len(clubeStats)):
            media = (clubeStats['chutes_no_alvo'][x] * 100)/clubeStats['chutes'][x]
            arrPrecisao.append(media)

        numArr = np.array(arrPrecisao)
        precisaoDf = pd.DataFrame([np.mean(numArr)], index=[clubes[y]])
        dataPrecisao.append(precisaoDf)    
    
    return pd.concat(dataPrecisao).sort_values(by=0)

st.title("Precisão entre chutes e chutes ao gol:")
st.table(precisaoTime(brasileirao_ano))

#Ver média de gols por partida
#TImes.unique() e adicionar num array

def golsProContra (table):
    mandantePro = table.groupby('mandante').agg({'mandante_Placar': ['sum', 'mean']})
    visitantePro = table.groupby('visitante').agg({'visitante_Placar': ['sum', 'mean']})
    mandanteContra = table.groupby('mandante').agg({'visitante_Placar': ['sum', 'mean']})
    visitanteContra = table.groupby('visitante').agg({'mandante_Placar': ['sum', 'mean']})
    dfPro = mandantePro.join(visitantePro).set_axis(['soma_mandante', 'media_mandante','soma_visitante','media_visitante'], axis=1, inplace=False)
    dfContra = mandanteContra.join(visitanteContra).set_axis(['soma_mandante', 'media_mandante','soma_visitante','media_visitante'], axis=1, inplace=False)
    somaPro = dfPro['soma_mandante'] + dfPro['soma_visitante']
    mediaPro = (dfPro['soma_mandante'] + dfPro['soma_visitante'])/38
    somaContra = dfContra['soma_mandante'] + dfContra['soma_visitante']
    mediaContra = (dfContra['soma_mandante'] + dfContra['soma_visitante'])/38
    df_novo = pd.DataFrame({'gols_pro': somaPro, 'media_pro': mediaPro, 'gols_contra': somaContra, 'media_contra': mediaContra})
    #df = df.assign(nova_coluna=nova_coluna)
    

    return df_novo.sort_values(by='gols_pro', ascending=False)
    
st.title("Soma e média de gols pró e gols contra:")
st.table(golsProContra(brasileirao_ano))