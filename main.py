from funcoes import *
import random

print("Insper Dominó")
print("=> Design de Software\n")
print("Bem-vindo(a) ao jogo de Dominó! O objetivo desse jogo é ficar sem peças na sua mão antes dos outros jogadores.\n")
print("Vamos começar!!!\n")

def peca_str(p):
    return "[" + str(p[0]) + "|" + str(p[1]) + "]"

def mostrar_mesa(mesa):
    if not mesa:
        print("(vazia)")
        return
    linha = ""
    i = 0
    while i < len(mesa):
        linha += peca_str(mesa[i]) + " "
        i += 1
    print(linha.strip())

def cor(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m"

def peca_colored_str(p):
    s = p[0] + p[1]
    m = s % 6
    if m == 0:
        return cor(peca_str(p), 32)   # verde
    if m == 1:
        return cor(peca_str(p), 36)   # azul claro
    if m == 2:
        return cor(peca_str(p), 33)   # amarelo
    if m == 3:
        return cor(peca_str(p), 35)   # rosa
    if m == 4:
        return cor(peca_str(p), 34)   # azul
    return cor(peca_str(p), 31)       # vermelho

def mostrar_mao(mao, posicoes_possiveis_na_mao=None):
    if posicoes_possiveis_na_mao is None:
        posicoes_possiveis_na_mao = []

    widths = []
    plain_tokens = []
    colored_tokens = []
    i = 0
    while i < len(mao):
        plain = peca_str(mao[i])
        col = peca_colored_str(mao[i])
        plain_tokens.append(plain)
        colored_tokens.append(col)
        widths.append(len(plain))
        i += 1

    # separador entre tokens 
    sep = "   "  

    # 1) linha de asteriscos 
    if plain_tokens:
        stars = []
        j = 0
        while j < len(plain_tokens):
            w = widths[j]
            if j in posicoes_possiveis_na_mao:
                star = "*".center(w)
            else:
                star = " " * w
            stars.append(star)
            j += 1
        # juntar com separador e imprimir
        line_stars = sep.join(stars)
        print(line_stars)

    # 2) linha das peças coloridas 
    if colored_tokens:
        line_pieces = sep.join(colored_tokens)
        print(line_pieces)

    # 3) linha dos índices 
    if plain_tokens:
        indices = []
        n = 1
        idx = 0
        while idx < len(plain_tokens):
            w = widths[idx]
            indices.append(str(n).center(w))
            n += 1
            idx += 1
        line_idx = sep.join(indices)
        print(line_idx)


def pedir_peca_inicial_humano(estado):
    pecas_humanas = estado['jogadores'][0]
    print("\nVocê foi sorteado para começar!")
    print("\nSuas peças:")
    # mesa vazia -> todas as posições possíveis
    listar = list(range(len(pecas_humanas)))
    mostrar_mao(pecas_humanas, listar)

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

def executa_jogada_inicial(jogador_atual, estado):
    if jogador_atual == 0:
        pedir_peca_inicial_humano(estado)
        return (0, None)
    else:
        mao_bot = estado['jogadores'][jogador_atual]
        idx_bot = random.randrange(len(mao_bot))
        peca_escolhida = mao_bot.pop(idx_bot)
        estado['mesa'] = adiciona_na_mesa(peca_escolhida, estado['mesa'])
        return (jogador_atual, peca_escolhida)

rodando = True
while rodando:

    while True:
        entrada = input("Quantos jogadores? (2-4) ").strip()
        if not entrada.isdigit():
            print("Digite um número válido (2, 3 ou 4).")
            continue
        num_jogadores = int(entrada)
        if num_jogadores < 2 or num_jogadores > 4:
            print("Número de jogadores deve ser 2, 3 ou 4.")
            continue
        break

    # inicia partida
    pecas = cria_pecas()
    estado = inicia_jogo(num_jogadores, pecas)

    jogador_atual = random.randrange(num_jogadores)

    starter, peca_inicial = executa_jogada_inicial(jogador_atual, estado)

    if starter == 0 and peca_inicial is None:
        pass
    else:
        qtd_antes = len(estado['jogadores'][starter]) + 1
        print("\nJogador: " + str(starter) + " com " + str(qtd_antes) + " peça(s)")
        if peca_inicial is not None:
            print("Colocou: " + peca_str(peca_inicial))

    print("\nMESA:")
    mostrar_mesa(estado['mesa'])

    print("\nJogador: Você com " + str(len(estado['jogadores'][0])) + " peça(s)\n")

    mostrar_mao(estado['jogadores'][0])
    print("\nMonte com " + str(len(estado['monte'])) + " peça(s).")

    game_over = False
    consecutive_passes = 0

    jogador_atual = (jogador_atual + 1) % num_jogadores

    while not game_over:
        mao = estado['jogadores'][jogador_atual]
        poss = posicoes_possiveis(estado['mesa'], mao)

        if jogador_atual == 0:
            # turno jogador
            print("\n-> Sua vez.")
            print("MESA:")
            mostrar_mesa(estado['mesa'])
            print("\nSua mão (" + str(len(mao)) + " peça(s)):")
            # mostra a mão com asteriscos nas posições possíveis
            mostrar_mao(mao, poss)
            print("Monte com " + str(len(estado['monte'])) + " peça(s).")

            if poss:
                # lista as posições possíveis em forma legível (1-based)
                print("Posições possíveis (índices na sua mão): ", end="")
                j = 0
                while j < len(poss):
                    print(str(poss[j] + 1), end=" ")
                    j += 1
                print()

                while True:
                    escolha = input("Escolha a peça (digite o número correspondente): ").strip()
                    if not escolha.isdigit():
                        print("Digite um número válido.")
                        continue
                    escolha_idx = int(escolha) - 1
                    valido = False
                    k = 0
                    while k < len(poss):
                        if poss[k] == escolha_idx:
                            valido = True
                            break
                        k += 1
                    if not valido:
                        print("Peça não é jogável. Escolha uma das posições possíveis.")
                        continue
                    peca_jogada = mao.pop(escolha_idx)
                    estado['mesa'] = adiciona_na_mesa(peca_jogada, estado['mesa'])
                    print("Você colocou: " + peca_str(peca_jogada))
                    consecutive_passes = 0
                    break
            else:
                if estado['monte']:
                    print("Nenhuma peça possível. Comprando do monte...")
                else:
                    print("Nenhuma peça possível e monte vazio. Você passa a vez.")
                bought_and_played = False
                while not poss and estado['monte']:
                    nova = estado['monte'].pop(0)
                    mao.append(nova)
                    print("Você comprou: " + peca_str(nova))
                    poss = posicoes_possiveis(estado['mesa'], mao)
                    if poss:
                        print("Agora há peças jogáveis.")
                        print("Posições possíveis (índices na sua mão): ", end="")
                        j = 0
                        while j < len(poss):
                            print(str(poss[j] + 1), end=" ")
                            j += 1
                        print()
                        while True:
                            escolha = input("Escolha a peça (digite o número correspondente): ").strip()
                            if not escolha.isdigit():
                                print("Digite um número válido.")
                                continue
                            escolha_idx = int(escolha) - 1
                            valido = False
                            k = 0
                            while k < len(poss):
                                if poss[k] == escolha_idx:
                                    valido = True
                                    break
                                k += 1
                            if not valido:
                                print("Peça não é jogável. Escolha uma das posições possíveis.")
                                continue
                            peca_jogada = mao.pop(escolha_idx)
                            estado['mesa'] = adiciona_na_mesa(peca_jogada, estado['mesa'])
                            print("Você colocou: " + peca_str(peca_jogada))
                            bought_and_played = True
                            consecutive_passes = 0
                            break
                        break
                if not poss and not bought_and_played:
                    print("Você não conseguiu jogar e passa a vez.")
                    consecutive_passes += 1

        else:
            # turno bot
            print("\n-> Vez do jogador " + str(jogador_atual))
            if poss:
                ind = random.randrange(len(poss))
                pos = poss[ind]
                peca_jogada = mao.pop(pos)
                estado['mesa'] = adiciona_na_mesa(peca_jogada, estado['mesa'])
                print("Jogador " + str(jogador_atual) + " jogou: " + peca_str(peca_jogada))
                consecutive_passes = 0
            else:
                bought_and_played = False
                while not poss and estado['monte']:
                    nova = estado['monte'].pop(0)
                    mao.append(nova)
                    poss = posicoes_possiveis(estado['mesa'], mao)
                    if poss:
                        pos = poss[0]
                        peca_jogada = mao.pop(pos)
                        estado['mesa'] = adiciona_na_mesa(peca_jogada, estado['mesa'])
                        print("Jogador " + str(jogador_atual) + " comprou e jogou: " + peca_str(peca_jogada))
                        bought_and_played = True
                        consecutive_passes = 0
                        break
                if not poss and not bought_and_played:
                    print("Jogador " + str(jogador_atual) + " não conseguiu jogar e passou.")
                    consecutive_passes += 1

        # verificar vencedor imediato
        vencedor = verifica_ganhador(estado['jogadores'])
        if vencedor != -1:
            if vencedor == 0:
                print("\nParabéns! Você ficou sem peças e venceu!")
            else:
                print("\nJogador " + str(vencedor) + " venceu ficando sem peças!")
            game_over = True
            break

        # verificar bloqueio (empate)
        if consecutive_passes >= num_jogadores and not estado['monte']:
            print("\nJogo bloqueado! Nenhum jogador conseguiu jogar e o monte está vazio.")
            menor = None
            vencedores = []
            i = 0
            while i < num_jogadores:
                pts = conta_pontos(estado['jogadores'][i])
                print("Jogador " + str(i) + " tem " + str(pts) + " pontos")
                if menor is None or pts < menor:
                    menor = pts
                    vencedores = [i]
                elif pts == menor:
                    vencedores.append(i)
                i += 1
            if len(vencedores) == 1:
                if vencedores[0] == 0:
                    print("Você venceu por menor pontuação: " + str(menor))
                else:
                    print("Jogador " + str(vencedores[0]) + " venceu por menor pontuação: " + str(menor))
            else:
                print("Empate entre os jogadores: ", end="")
                j = 0
                while j < len(vencedores):
                    print(str(vencedores[j]) + " ", end="")
                    j += 1
                print()
            game_over = True
            break

        jogador_atual = (jogador_atual + 1) % num_jogadores

    # fim da partida
    # pergunta se deseja reiniciar (nova partida)
    while True:
        again = input("\nDeseja jogar novamente? (s/n) ").strip().lower()
        if again in ('s', 'sim'):
            print("\nReiniciando a partida...\n")
            break
        elif again in ('n', 'nao', 'não'):
            print("Obrigado por jogar! Até a próxima.")
            rodando = False
            break
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")
            continue
