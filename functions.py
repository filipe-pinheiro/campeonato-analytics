def calularAproveitamento(totalJogos, vitorias, empates ):
    pontosAtingidos = (vitorias * 3) + empates
    pontosPossiveis = totalJogos * 3
    aproveitamento = float((pontosAtingidos * 100) / pontosPossiveis)
    return round(aproveitamento, 2)

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

    return [arr_aprov, vitoria, empate]
