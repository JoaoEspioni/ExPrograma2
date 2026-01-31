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
