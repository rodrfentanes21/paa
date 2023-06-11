import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

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
    menor_combustivel_total = float('inf')
    rota_otima = None

    def permutate(current, remaining):
        nonlocal menor_combustivel_total, rota_otima

        if not remaining:
            rota = current + [lojas[0]]
            combustivel_total = 0
            cargas = set()

            for i in range(len(rota) - 1):
                atual = rota[i]
                proximo = rota[i + 1]
                distancia = calcular_distancia(atual, proximo)
                

                combustivel_total += calcular_combustivel(distancia, len(cargas))
                
                if proximo.numero in cargas:
                    cargas.remove(proximo.numero)
                cargas.update(proximo.destinos)
                
                if len(cargas) > capacidade_caminhao:
                    break

                if i == len(rota) - 2 and len(cargas) == 0:
                    if combustivel_total < menor_combustivel_total:
                        menor_combustivel_total = combustivel_total
                        rota_otima = rota

        else:
            for i in range(len(remaining)):
                permutate(current + [remaining[i]], remaining[:i] + remaining[i+1:])

    permutate([lojas[0]], lojas[1:])

    return rota_otima, menor_combustivel_total

def exibir_animacao(rota):
    x = [loja.x for loja in rota]
    y = [loja.y for loja in rota]
    numeros = [loja.numero for loja in rota]  # Store numbers

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo-')
    ax.plot(x[0], y[0], 'go')  # Marcando a matriz (loja 0) em verde
    ax.set(xlabel='Coordenada X', ylabel='Coordenada Y', title='Rota do caminhão')
    ax.grid()

    # Annotate store numbers on the graph
    for i, num in enumerate(numeros):
        ax.annotate(num, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Create truck marker
    truck_marker = ax.plot([], [], 'r>', markersize=10)[0]

    def update(frame):
        truck_marker.set_data(x[frame], y[frame])
        return truck_marker,

    # Set up animation
    anim = animation.FuncAnimation(fig, update, frames=len(x), interval=1000, repeat=False, blit=True)

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

    start = time.time()

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
            carga_atual = capacidade_caminhao - len(loja_proxima.destinos)
            combustivel_trecho = calcular_combustivel(distancia, carga_atual)
            print(f'De loja {loja_atual.numero} para loja {loja_proxima.numero}: {combustivel_trecho:.5f} litros')

        end = time.time()
        print("Tempo de execução: " + str(end - start))
        exibir_animacao(rota_otima)

if __name__ == '__main__':
    main()
