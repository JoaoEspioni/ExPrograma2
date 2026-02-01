import random

def cria_pecas():
    pecas = []
    for valor_esquerda in range(7):
        for valor_direita in range(valor_esquerda, 7):
            pecas.append([valor_esquerda, valor_direita])
    random.shuffle(pecas)
    return pecas

def inicia_jogo(num_jogadores, pecas):
    jogadores = {}
    pecas_por_jogador = 7

    indice = 0
    for jogador in range(num_jogadores):
        jogadores[jogador] = pecas[indice:indice + pecas_por_jogador]
        indice += pecas_por_jogador

    monte = pecas[indice:]
    mesa = []

    return {
        'jogadores': jogadores,
        'monte': monte,
        'mesa': mesa
    }

def verifica_ganhador(jogadores):
    for numero_jogador in jogadores:
        if len(jogadores[numero_jogador]) == 0:
            return numero_jogador
    return -1

def conta_pontos(pecas_jogador):
    pontos = 0
    for peca in pecas_jogador:
        pontos += peca[0] + peca[1]
    return pontos

def posicoes_possiveis(mesa, pecas_jogador):
    posicoes = []

    if mesa == []:
        indice = 0
        for i in pecas_jogador:
            posicoes.append(indice)
            indice += 1
        return posicoes

    ponta_esquerda = mesa[0][0]
    ponta_direita = mesa[-1][1]

    indice = 0
    for peca in pecas_jogador:
        if (peca[0] == ponta_esquerda or
            peca[1] == ponta_esquerda or
            peca[0] == ponta_direita or
            peca[1] == ponta_direita):
            posicoes.append(indice)
        indice += 1

    return posicoes

def adiciona_na_mesa(peca, mesa):
    if not mesa:
        return [peca]

    ponta_esquerda = mesa[0][0]
    ponta_direita = mesa[-1][1]

    a = peca[0]
    b = peca[1]

    if b == ponta_esquerda:
        return [[a, b]] + mesa
    if a == ponta_esquerda:
        return [[b, a]] + mesa

    if a == ponta_direita:
        return mesa + [[a, b]]
    if b == ponta_direita:
        return mesa + [[b, a]]

    return mesa