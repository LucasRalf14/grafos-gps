import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.grafo:
            self.grafo[origem] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origem].append((destino, peso))
        self.grafo[destino].append((origem, peso))

    def dijkstra(self, inicio):
        distancias = {vertice: float('infinity') for vertice in self.grafo}
        distancias[inicio] = 0
        antecessores = {vertice: None for vertice in self.grafo}
        fila_prioridade = [(0, inicio)]

        while fila_prioridade:
            distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

            if distancia_atual > distancias[vertice_atual]:
                continue

            for vizinho, peso in self.grafo[vertice_atual]:
                distancia = distancia_atual + peso
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    antecessores[vizinho] = vertice_atual
                    heapq.heappush(fila_prioridade, (distancia, vizinho))

        return distancias, antecessores

    def menor_caminho(self, inicio, destino):
        distancias, antecessores = self.dijkstra(inicio)
        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            atual = antecessores[atual]
        return caminho, distancias[destino]


g = Grafo()
g.adicionar_aresta("Boa Viagem", "Imbiribeira", 10)
g.adicionar_aresta("Imbiribeira", "Afogados", 8)
g.adicionar_aresta("Afogados", "Santo Amaro", 6)
g.adicionar_aresta("Boa Viagem", "Pina", 7)
g.adicionar_aresta("Pina", "Santo Amaro", 12)
g.adicionar_aresta("Boa Viagem", "Casa Forte", 20)
g.adicionar_aresta("Santo Amaro", "Casa Forte", 5)

# Calcular menor caminho
origem = "Boa Viagem"
destino = "Casa Forte"
caminho, tempo = g.menor_caminho(origem, destino)

# -------------------------------
# Visualização com NetworkX
# -------------------------------
G = nx.Graph()
for v in g.grafo:
    for vizinho, peso in g.grafo[v]:
        G.add_edge(v, vizinho, weight=peso)

pos = nx.spring_layout(G, seed=42)  # Layout bonito e fixo

# Desenhar todos os nós e arestas
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="red", font_size=10, font_weight="bold")
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Destacar o menor caminho
caminho_edges = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, width=3, edge_color="blue")

plt.title(f"Menor rota de {origem} até {destino} ({tempo} min)", fontsize=12, fontweight="bold")
plt.show()
