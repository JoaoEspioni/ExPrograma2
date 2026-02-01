from funcoes import *
import random

print("Insper Dominó")
print("=> Design de Software\n")
print("Bem-vindo(a) ao jogo de Dominó! O objetivo desse jogo é ficar sem peças na sua mão antes dos outros jogadores.\n")
print("Vamos começar!!!\n")

num_jogadores = int(input("Quantos jogadores? (2-4) "))

pecas = cria_pecas()
estado = inicia_jogo(num_jogadores, pecas)  

jogador_atual = random.randrange(num_jogadores)

def peca_str(p):
    return "[" + str(p[0]) + "|" + str(p[1]) + "]"

# jogador sorteado coloca a primeira peça
if jogador_atual == 0:
    print("\nVocê foi sorteado para começar!")
    pecas_humanas = estado['jogadores'][0]

    print("\nSuas peças:")
    contador = 1
    for p in pecas_humanas:  
        print(str(contador) + ": " + peca_str(p), end="  ")
        contador += 1
    print()


    while True:
        escolha = input("Escolha a peça inicial (digite o número): ").strip()
        if not escolha.isdigit():
            print("Digite um número válido.")
            continue
        pos = int(escolha) - 1
        if pos < 0 or pos >= len(pecas_humanas):
            print("Índice fora do intervalo. Tente novamente.")
            continue
        peca_escolhida = estado['jogadores'][0].pop(pos)
        estado['mesa'] = adiciona_na_mesa(peca_escolhida, estado['mesa'])
        print("\nVocê colocou: " + peca_str(peca_escolhida))
        break
else:
    mao_bot = estado['jogadores'][jogador_atual]
    idx_bot = random.randrange(len(mao_bot))
    peca_escolhida = mao_bot.pop(idx_bot)
    estado['mesa'] = adiciona_na_mesa(peca_escolhida, estado['mesa'])
    print("\nJogador " + str(jogador_atual) + " começou e colocou: " + peca_str(peca_escolhida))

print("\nMESA:")
if not estado['mesa']:
    print("(vazia)")
else:
    linha = ""
    i = 0
    while i < len(estado['mesa']):   
        p = estado['mesa'][i]
        linha += peca_str(p) + " "
        i += 1
    print(linha.strip())

print("\nJogador: Você com " + str(len(estado['jogadores'][0])) + " peça(s)\n")
i = 1
for p in estado['jogadores'][0]:
    print(str(i).rjust(2) + " " + peca_str(p), end="   ")
    i += 1
print("\n")
