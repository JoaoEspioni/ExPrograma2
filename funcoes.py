import random

def cria_pecas():
    pecas = []
    for valor_esquerda in range(7):
        for valor_direita in range(valor_esquerda, 7):
            pecas.append([valor_esquerda, valor_direita])
    random.shuffle(pecas)
    return pecas