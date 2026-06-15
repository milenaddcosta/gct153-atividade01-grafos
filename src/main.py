import heapq

# ==================================================
# CLASSE GRAFO PONDERADO
# ==================================================

class GrafoPonderado:

    # Construtor da classe
    # Cria um grafo com a quantidade de vértices informada
    # utilizando lista de adjacência
    def __init__(self, vertices):

        self.V = vertices

        # Dicionário onde cada vértice possui
        # uma lista de pares (vizinho, peso)
        self.adj = {i: [] for i in range(vertices)}

    # Adiciona uma aresta não direcionada
    # entre os vértices u e v
    def adicionar_aresta(self, u, v, peso):

        self.adj[u].append((v, peso))
        self.adj[v].append((u, peso))

    # Exibe a lista de adjacência do grafo
    def exibir(self):

        for v in self.adj:
            print(f"{v}: {self.adj[v]}")

    # Retorna os vizinhos de um vértice
    def vizinhos(self, v):

        return self.adj[v]


# ==================================================
# ALGORITMO DE DIJKSTRA
# ==================================================

def dijkstra(grafo, origem):

    # Inicializa todas as distâncias com infinito
    dist = [float('inf')] * grafo.V

    # Armazena o predecessor de cada vértice
    pai = [None] * grafo.V

    # A distância da origem para ela mesma é zero
    dist[origem] = 0

    # Fila de prioridade (heap)
    fila = [(0, origem)]

    while fila:

        # Remove o vértice com menor distância
        distancia_atual, u = heapq.heappop(fila)

        # Ignora entradas antigas da fila
        if distancia_atual > dist[u]:
            continue

        # Percorre todos os vizinhos do vértice atual
        for v, peso in grafo.vizinhos(u):

            # Calcula uma possível nova distância
            nova_dist = dist[u] + peso

            # Relaxamento da aresta
            if nova_dist < dist[v]:

                # Atualiza a menor distância encontrada
                dist[v] = nova_dist

                # Atualiza o predecessor
                pai[v] = u

                # Insere o vértice na fila
                heapq.heappush(fila, (nova_dist, v))

    return dist, pai


# ==================================================
# RECONSTRUÇÃO DO CAMINHO
# ==================================================

# Reconstrói o menor caminho a partir
# do vetor de predecessores gerado pelo Dijkstra
def reconstruir_caminho(pai, destino):

    caminho = []

    # Volta do destino até a origem
    while destino is not None:

        caminho.append(destino)

        destino = pai[destino]

    # Inverte para obter origem -> destino
    caminho.reverse()

    return caminho


# ==================================================
# ALGORITMO DE PRIM
# ==================================================

def prim(grafo, inicio=0):

    # Marca os vértices já inseridos na árvore
    visitado = [False] * grafo.V

    # Heap contendo:
    # (peso da aresta, vértice, pai)
    fila = [(0, inicio, -1)]

    arvore = []

    custo_total = 0

    ordem = []

    while fila:

        # Seleciona a aresta de menor peso disponível
        peso, u, pai = heapq.heappop(fila)

        if visitado[u]:
            continue

        visitado[u] = True

        ordem.append(u)

        # Não adiciona aresta para o vértice inicial
        if pai != -1:

            arvore.append((pai, u, peso))

            custo_total += peso

        # Adiciona os vizinhos na fila
        for v, p in grafo.vizinhos(u):

            if not visitado[v]:

                heapq.heappush(fila, (p, v, u))

    return arvore, custo_total, ordem


# ==================================================
# ESTRUTURA UNION-FIND
# ==================================================

class UnionFind:

    def __init__(self, n):

        # Cada vértice começa em seu próprio conjunto
        self.pai = list(range(n))

    # Encontra o representante do conjunto
    def find(self, x):

        # Compressão de caminho
        if self.pai[x] != x:

            self.pai[x] = self.find(self.pai[x])

        return self.pai[x]

    # Une dois conjuntos distintos
    def union(self, a, b):

        ra = self.find(a)

        rb = self.find(b)

        if ra != rb:

            self.pai[rb] = ra


# ==================================================
# ALGORITMO DE KRUSKAL
# ==================================================

def kruskal(grafo):

    arestas = []

    # Obtém todas as arestas do grafo
    for u in grafo.adj:

        for v, peso in grafo.adj[u]:

            # Evita armazenar arestas duplicadas
            if u < v:

                arestas.append((peso, u, v))

    # Ordena as arestas em ordem crescente de peso
    arestas.sort()

    uf = UnionFind(grafo.V)

    mst = []

    descartadas = []

    custo = 0

    # Analisa as arestas da menor para a maior
    for peso, u, v in arestas:

        # Se os vértices pertencem a conjuntos diferentes,
        # a aresta não forma ciclo
        if uf.find(u) != uf.find(v):

            uf.union(u, v)

            mst.append((u, v, peso))

            custo += peso

        else:

            # Aresta descartada por formar ciclo
            descartadas.append((u, v, peso))

    return arestas, mst, descartadas, custo


# ==================================================
# CONSTRUÇÃO DO GRAFO DO ENUNCIADO
# ==================================================

g = GrafoPonderado(9)

arestas = [
    (0, 1, 4),
    (0, 2, 2),
    (1, 2, 1),
    (1, 3, 5),
    (2, 3, 8),
    (2, 4, 10),
    (3, 4, 2),
    (3, 5, 6),
    (4, 5, 3),
    (4, 6, 7),
    (5, 6, 1),
    (5, 7, 9),
    (6, 7, 4),
    (6, 8, 6),
    (7, 8, 2)
]

# Adiciona todas as arestas ao grafo
for u, v, p in arestas:

    g.adicionar_aresta(u, v, p)


# ==================================================
# EXIBIÇÃO DO GRAFO
# ==================================================

print("=== GRAFO ===")

g.exibir()


# ==================================================
# DIJKSTRA ORIGEM 0
# ==================================================

print("\n=== DIJKSTRA origem 0 ===")

dist, pai = dijkstra(g, 0)

print("Distancias:", dist)
print("Pais:", pai)

caminho5 = reconstruir_caminho(pai, 5)
caminho8 = reconstruir_caminho(pai, 8)

print("Caminho 0 -> 5:", caminho5)
print("Custo:", dist[5])

print("Caminho 0 -> 8:", caminho8)
print("Custo:", dist[8])


# ==================================================
# DIJKSTRA ORIGEM 4
# (EXPERIMENTO EXIGIDO PELO PROFESSOR)
# ==================================================

print("\n=== DIJKSTRA origem 4 ===")

dist4, pai4 = dijkstra(g, 4)

print("Distancias:", dist4)
print("Pais:", pai4)


# ==================================================
# PRIM
# ==================================================

print("\n=== PRIM ===")

mst, custo, ordem = prim(g, 0)

print("Arestas selecionadas:")

for aresta in mst:
    print(aresta)

print("Custo total:", custo)
print("Ordem:", ordem)


# ==================================================
# PRIM COM OUTRO VÉRTICE INICIAL
# (EXPERIMENTO EXIGIDO PELO PROFESSOR)
# ==================================================

print("\n=== PRIM origem 4 ===")

mst2, custo2, ordem2 = prim(g, 4)

print("Arestas selecionadas:")

for aresta in mst2:
    print(aresta)

print("Custo total:", custo2)
print("Ordem:", ordem2)


# ==================================================
# KRUSKAL
# ==================================================

print("\n=== KRUSKAL ===")

arestas_ord, mstk, descartadas, custoK = kruskal(g)

print("Arestas ordenadas:")

for a in arestas_ord:
    print(a)

print("\nSelecionadas:")

for a in mstk:
    print(a)

print("\nDescartadas:")

for a in descartadas:
    print(a)

print("Custo total:", custoK)


# ==================================================
# COMPARAÇÃO FINAL
# ==================================================

print("\n=== COMPARAÇÃO ===")
print("Custo Prim:", custo)
print("Custo Kruskal:", custoK)

if custo == custoK:
    print("Prim e Kruskal produziram o mesmo custo total.")
else:
    print("Os custos obtidos foram diferentes.")
