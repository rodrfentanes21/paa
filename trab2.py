import itertools
import math
import matplotlib.pyplot as plt

class Loja:
    def __init__(self, numero, x, y, destinos):
        self.numero = numero
        self.x = x
        self.y = y
        self.destinos = destinos

def calcular_distancia(loja1, loja2):
    return math.sqrt((loja2.x - loja1.x) ** 2 + (loja2.y - loja1.y) ** 2)

def calcular_combustivel(distancia, carga_atual):
    rendimento_base = 10  # km/litro
    rendimento_por_produto = 0.5  # km/litro por produto
    rendimento_atual = rendimento_base - (carga_atual * rendimento_por_produto)
    combustivel_gasto = distancia / rendimento_atual
    return combustivel_gasto

def calcular_rota_otima(lojas, capacidade_caminhao):
    # inicialização das variaveis de rota otima e combustivel da rota ótima
    menor_combustivel_total = float('inf') 
    rota_otima = None

    # biblioteca usada para gerar combinações entre todos os caminhos possiveis passando 1x por cada loja, 
    # evidentemente como se trata de um método força bruta nem todos serão válidos ou satisfatórios
    perm_lojas = itertools.permutations(lojas[1:])

    # itera cada um dos casos gerados na permutação
    for perm in perm_lojas:
        rota = [lojas[0]] + list(perm) + [lojas[0]]
        combustivel_total = 0
        cargas = set()

        # itera cara um dos passos do caso gerado
        for i in range(len(rota) - 1):
            atual = rota[i]
            proximo = rota[i + 1]
            distancia = calcular_distancia(atual, proximo)

            #variavel vai acumulando o combustivel gasto a cada passo da jornada
            combustivel_total += calcular_combustivel(distancia, len(cargas))
            
            # caso tenha alguma entrega no proximo destino, devemos removê-la do set de cargas
            if proximo.numero in cargas:
                cargas.remove(proximo.numero)
            cargas.update(proximo.destinos)
            
            # caso esse caminho ocasione na ultrapassagem do limite de carga, ele é invalido, portanto acabamos a iteração por aqui
            if len(cargas) > capacidade_caminhao:
                break
            
            # no penultimo elemento, antes da volta a 0, caso todos pacotes tenham sido entregados, esse caminho é válido e satisfatório
            if i == len(rota) - 2 and len(cargas) == 0:
                # registrado o caminho como mais eficiente, caso ele seja satisfatório, válido e gaste menos combustível
                if combustivel_total < menor_combustivel_total:
                    menor_combustivel_total = combustivel_total
                    rota_otima = rota

    return rota_otima, menor_combustivel_total

def exibir_animacao(rota):
    x = [loja.x for loja in rota]
    y = [loja.y for loja in rota]

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo-')
    ax.plot(x[0], y[0], 'go')  # Marcando a matriz (loja 0) em verde
    ax.set(xlabel='Coordenada X', ylabel='Coordenada Y', title='Rota do caminhão')
    ax.grid()
    plt.show()

def ler_lojas_do_arquivo(arquivo):
    lojas = []
    with open(arquivo, 'r') as f: 
        for linha in f:
            valores = linha.split()
            numero = int(valores[0])
            x = int(valores[1])
            y = int(valores[2])
            destinos = []
            if len(valores) > 3:
                destinos = [int(d) for d in valores[3:]]
            loja = Loja(numero, x, y, destinos)
            lojas.append(loja)
    return lojas

def main():
    arquivo_lojas = 'lojas.txt'
    capacidade_caminhao = int(input())

    lojas = ler_lojas_do_arquivo(arquivo_lojas)
    rota_otima, combustivel_total = calcular_rota_otima(lojas, capacidade_caminhao)

    if rota_otima is not None:
        print(f'Rota ótima: {[loja.numero for loja in rota_otima]}')
        print(f'Combustível total gasto: {combustivel_total:.5f} litros')

        print("Combustível gasto por trecho:")
        for i in range(len(rota_otima) - 1):
            loja_atual = rota_otima[i]
            loja_proxima = rota_otima[i + 1]
            distancia = calcular_distancia(loja_atual, loja_proxima)
            carga_atual = len(loja_proxima.destinos)
            combustivel_trecho = calcular_combustivel(distancia, carga_atual)
            print(f'De loja {loja_atual.numero} para loja {loja_proxima.numero}: {combustivel_trecho:.5f} litros')

        exibir_animacao(rota_otima)
    else:
        print("Não foi encontrada uma rota que satisfaça as condições")

if __name__ == '__main__':
    main()