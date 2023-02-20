import streamlit as st
import pandas as pd
import numpy as np

st.title("Dados do Brasileirão 2017/2022")
#brasileirao_csv = pd.read_csv("campeonato-brasileiro-full.csv")
#st.write(brasileirao_csv)

brasileirao_csv['data'] = pd.to_datetime(brasileirao_csv['data'], format = '%d/%m/%Y')
brasileirao_spfc_visitante = brasileirao_csv[(brasileirao_csv['visitante'] == 'Sao Paulo') & (brasileirao_csv['tecnico_visitante'] == 'R. Ceni')]
brasileirao_spfc_mandante = brasileirao_csv[(brasileirao_csv['mandante'] == 'Sao Paulo') & (brasileirao_csv['tecnico_mandante'] == 'R. Ceni')]
brasileirao_spfc_jogos = pd.concat([brasileirao_spfc_visitante, brasileirao_spfc_mandante])

brasileirao_spfc_jogos = brasileirao_spfc_jogos.sort_values(by = 'ID').reset_index()
#st.write(brasileirao_spfc_jogos)

#st.write(brasileirao_spfc_jogos.info())

rceni_spfc_2017 = brasileirao_spfc_jogos[brasileirao_spfc_jogos['data'].dt.strftime('%Y') == '2017']
rceni_spfc_2021 = brasileirao_spfc_jogos[brasileirao_spfc_jogos['data'].dt.strftime('%Y') == '2021']
rceni_spfc_2022 = brasileirao_spfc_jogos[brasileirao_spfc_jogos['data'].dt.strftime('%Y') == '2022']

#st.title("Jogo do R Ceni em 2017")
#st.write(rceni_spfc_2017)

#st.title("Jogo do R Ceni em 2021")
#st.write(rceni_spfc_2021)

#st.title("Jogo do R Ceni em 2022")
#st.write(rceni_spfc_2022)

##Função para cálculo de aproveitamento
def calularAproveitamento(totalJogos, vitorias, empates ):
    pontosAtingidos = (vitorias * 3) + empates
    pontosPossiveis = totalJogos * 3
    aproveitamento = int((pontosAtingidos * 100) / pontosPossiveis)
    return aproveitamento

##Cáculo de aproveitamento de 2017
vitoria_spfc_2017 = len(rceni_spfc_2017[rceni_spfc_2017['vencedor'] == 'Sao Paulo'])
empate_spfc_2017 = len(rceni_spfc_2017[rceni_spfc_2017['vencedor'] == '-'])
total_spfc_2017 = len(rceni_spfc_2017)
aproveitamento_2017 = calularAproveitamento(total_spfc_2017, vitoria_spfc_2017, empate_spfc_2017)

##Cáculo de aproveitamento de 2021
vitoria_spfc_2021 = len(rceni_spfc_2021[rceni_spfc_2021['vencedor'] == 'Sao Paulo'])
empate_spfc_2021 = len(rceni_spfc_2021[rceni_spfc_2021['vencedor'] == '-'])
total_spfc_2021 = len(rceni_spfc_2021)
aproveitamento_2021 = calularAproveitamento(total_spfc_2021, vitoria_spfc_2021, empate_spfc_2021)

##Cáculo de aproveitamento de 2022
vitoria_spfc_2022 = len(rceni_spfc_2022[rceni_spfc_2022['vencedor'] == 'Sao Paulo'])
empate_spfc_2022 = len(rceni_spfc_2022[rceni_spfc_2022['vencedor'] == '-'])
total_spfc_2022 = len(rceni_spfc_2022)
aproveitamento_2022 = calularAproveitamento(total_spfc_2022, vitoria_spfc_2022, empate_spfc_2022)

##Preparar plot do gráfico
array_aproveitamento = [aproveitamento_2017, aproveitamento_2021, aproveitamento_2022]
data_chart = pd.DataFrame(array_aproveitamento, columns=['aproveitamento (%)'])
data_chart = data_chart.set_index([pd.Index([2017, 2021, 2022])])

#st.title("Taxa de aproveitamento nas três temporadas")
#st.dataframe(data_chart)
#st.bar_chart(data_chart)

##Aproveitamento das primeiras rodadas
brasileirao_2017 = brasileirao_csv[brasileirao_csv['data'].dt.strftime('%Y') == '2017' ].sort_values(by = 'ID').reset_index()

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

rodada = st.slider("Escolha a rodada:", 1, 38, 38, key = 'rodada')

clubes = pd.unique(brasileirao_2017['visitante'])
print(clubes)

col1, col2= st.columns(2)

with col1:
    time1 = st.selectbox(
    'How would you like to be contacted?',
    (clubes), key = 'time1')
    st.write('You selected:', time1)

with col2:
   time2 = st.selectbox(
   'How would you like to be contacted?',
   (clubes), key = 'time2')
   st.write('You selected:', time2)

primeiroTime= aprovPorRodada(brasileirao_2017, time1, rodada)
segundoTime = aprovPorRodada(brasileirao_2017, time2, rodada)

arr_2017 = [1]
chart_aprov = pd.DataFrame({
    "first": primeiroTime,
    "scnd": segundoTime,
    })
st.line_chart(chart_aprov)

#print(aprovPorRodada(rceni_spfc_2017, 'Sao Paulo', 11))
#brasileirao_2017_to_2022 = brasileirao_csv[brasileirao_csv['data'].isin(pd.date_range("2017-01-01", "2022-12-31"))]
#brasileirao_2017_to_2022 = brasileirao_2017_to_2022[brasileirao_2017_to_2022['rodata'].isin(range(1,11))]
