import heapq  # Importa a biblioteca de fila de prioridade eficiente para os algoritmos de Dijkstra e Prim

class GrafoPonderado:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices  # Armazena o número total de vértices do grafo
        self.adj = {i: [] for i in range(num_vertices)}  # Inicializa a lista de adjacência como um dicionário de listas vazias

    def adicionar_aresta(self, u, v, peso):
        # Como o grafo é não direcionado, a estrada conecta as duas cidades em ambos os sentidos
        self.adj[u].append((v, peso))  # Adiciona a conexão do vértice u para o vértice v com seu respectivo peso
        self.adj[v].append((u, peso))  # Adiciona a conexão de retorno do vértice v para o vértice u com o mesmo peso

    def exibir_grafo(self):
        print("=== GRAFO ===")
        # Percorre cada vértice e sua respectiva lista de vizinhos para exibição em tela
        for vertices, vizinhos in self.adj.items():
            print(f"{vertices}: {vizinhos}")

    def obtener_vizinhos(self, u):
        return self.adj[u]  # Retorna a lista de tuplas (vizinho, peso) diretamente ligadas ao vértice u

    # --- PARTE 1: ALGORITMO DE DIJKSTRA (CAMINHOS MÍNIMOS) ---
    def dijkstra(self, origem):
        # Inicializa todas as distâncias como infinito, exceto a origem que recebe custo zero
        distancias = {i: float('inf') for i in range(self.num_vertices)}
        predecessores = {i: None for i in range(self.num_vertices)}  # Dicionário para rastrear o caminho estruturado (pais)
        distancias[origem] = 0  # A distância para o próprio nó de origem é sempre zero
        
        # Cria a fila de prioridades e insere o nó inicial no formato (distancia, vertice)
        fila_prioridade = [(0, origem)]
        
        while fila_prioridade:
            # Extrai o vértice que possui a menor distância acumulada até o momento
            dist_atual, u = heapq.heappop(fila_prioridade)
            
            # Se a distância extraída for maior do que a já registrada, ignora o processamento (otimização)
            if dist_atual > distancias[u]:
                continue
                
            # Varre todos os vizinhos do vértice u para realizar o processo de relaxamento
            for vizinho, peso in self.obter_vizinhos(u):
                # Se passar por 'u' oferecer um caminho mais curto até 'vizinho', atualiza os dados
                if distancias[u] + peso < distancias[vizinho]:
                    distancias[vizinho] = distancias[u] + peso  # Atualiza a menor distância para o vizinho
                    predecessores[vizinho] = u  # Define 'u' como o pai/antecessor direto deste vizinho
                    heapq.heappush(fila_prioridade, (distancias[vizinho], vizinho))  # Insere a nova distância na fila
                    
        return distancias, predecessores  # Retorna o vetor de distâncias mínimas e o vetor de predecessores

    def reconstruir_caminho(self, predecessores, destino):
        caminho = []  # Lista que armazenará a sequência de vértices do caminho
        atual = destino  # Começa o rastreamento de trás para frente, a partir do destino
        while atual is not None:
            caminho.append(atual)  # Adiciona o vértice atual na sequência
            atual = predecessores[atual]  # Move para o pai do vértice atual
        caminho.reverse()  # Inverte a lista para que o caminho fique ordenado da Origem para o Destino
        return caminho

    # --- PARTE 2: ALGORITMO DE PRIM (ÁRVORE GERADORA MÍNIMA) ---
    def prim(self, vertice_inicial=0):
        visitados = set()  # Conjunto para armazenar e controlar os vértices já incluídos na árvore
        arestas_escolhidas = []  # Lista que armazenará a árvore final no formato (u, v, peso)
        ordem_vertices = []  # Lista para registrar a ordem exata em que os nós foram descobertos
        custo_total = 0  # Variável para acumular o peso total da infraestrutura da rede
        
        # Inicializa a fila com uma aresta fictícia para forçar a entrada no vértice inicial: (peso, pai, destino)
        fila_prioridade = [(0, -1, vertice_inicial)]
        
        while fila_prioridade and len(visitados) < self.num_vertices:
            # Seleciona sempre a aresta de menor peso conectada a um nó já visitado (estratégia gulosa)
            peso, u, v = heapq.heappop(fila_prioridade)
            
            # Se o vértice de destino 'v' já foi incluído na árvore, descarta a aresta para evitar ciclos
            if v in visitados:
                continue
                
            visitados.add(v)  # Marca o vértice 'v' como incluído na árvore
            ordem_vertices.append(v)  # Salva a ordem de visitação do vértice
            custo_total += peso  # Incrementa o custo da aresta na soma global da rede
            
            # Se não for o vértice inicial fictício, adiciona a aresta na lista final da AGM
            if u != -1:
                arestas_escolhidas.append((u, v, peso))
                
            # Varre os vizinhos do nó recém-adicionado para alimentar a fila de prioridades
            for vizinho, peso_aresta in self.obter_vizinhos(v):
                if vizinho not in visitados:
                    heapq.heappush(fila_prioridade, (peso_aresta, v, vizinho))  # Adiciona nova opção de expansão
                    
        return arestas_escolhidas, custo_total, ordem_vertices  # Retorna a árvore, o custo total e a ordem de inserção

    # --- PARTE 3: ALGORITMO DE KRUSKAL (ÁRVORE GERADORA MÍNIMA VIA ARESTAS) ---
    def obter_todas_arestas(self):
        arestas = set()  # Usa um conjunto para evitar duplicar arestas (já que u-v e v-u são a mesma aresta)
        for u in self.adj:
            for v, peso in self.adj[u]:
                if (v, u, peso) not in arestas:
                    arestas.add((u, v, peso))  # Garante o armazenamento único de cada estrada ponderada
        return list(arestas)

    def kruskal(self):
        arestas = self.obter_todas_arestas()
        # Ordena todas as arestas do grafo por peso em ordem crescente (essencial para o funcionamento do algoritmo)
        arestas_ordenadas = sorted(arestas, key=lambda x: x[2])
        
        # Inicializa a estrutura Union-Find interna: cada vértice começa sendo pai de si mesmo (conjuntos disjuntos)
        pai = list(range(self.num_vertices))
        
        def find(i):
            # Função recursiva com compressão de caminhos para encontrar o representante do conjunto do nó 'i'
            if pai[i] == i:
                return i
            pai[i] = find(pai[i])  # Otimiza a estrutura apontando diretamente para a raiz principal
            return pai[i]
            
        def union(i, j):
            # Une os conjuntos dos elementos 'i' e 'j' vinculando suas respectivas raízes
            raiz_i = find(i)
            raiz_j = find(j)
            pai[raiz_i] = raiz_j

        arestas_selecionadas = []  # Lista de arestas que farão parte da árvore geradora mínima
        arestas_descartadas = []  # Lista de arestas puladas por causarem formação de circuitos fechados (ciclos)
        custo_total = 0  # Somatório de custo da rede construída por Kruskal
        
        for u, v, peso in arestas_ordenadas:
            raiz_u = find(u)  # Encontra o conjunto ao qual o vértice 'u' pertence
            raiz_v = find(v)  # Encontra o conjunto ao qual o vértice 'v' pertence
            
            # Se as raízes forem diferentes, significa que 'u' e 'v' estão em árvores separadas (não forma ciclo)
            if raiz_u != raiz_v:
                union(raiz_u, raiz_v)  # Combina os dois conjuntos em um só
                arestas_selecionadas.append((u, v, peso))  # Aceita a aresta na árvore geradora mínima
                custo_total += peso  # Adiciona o valor ao custo total final
            else:
                arestas_descartadas.append((u, v, peso))  # Aresta recusada por conectar nós já integrados na mesma malha
                
        return arestas_ordenadas, arestas_selecionadas, arestas_descartadas, custo_total  # Retorna os dados analíticos


# --- BLOCO DE EXECUÇÃO DOS EXPERIMENTOS EXIGIDOS ---
if __name__ == "__main__":
    # Instancia o objeto do grafo com 9 vértices conforme especificado na Seção 3 do roteiro
    g = GrafoPonderado(9)
    
    # Lista de arestas extraída fielmente da tabela do enunciado do trabalho
    dados_arestas = [
        (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8),
        (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3), (4, 6, 7),
        (5, 6, 1), (5, 7, 7), (6, 7, 9), (6, 8, 4), (7, 8, 2)
    ]
    
    # Laço para alimentar e construir a estrutura interna do grafo ponderado
    for u, v, p in dados_arestas:
        g.adicionar_aresta(u, v, p)

    # Imprime a lista de adjacências gerada na tela
    g.exibir_grafo()
    print("\n" + "="*30 + "\n")

    # Execução do Experimento 1: Dijkstra partindo do Vértice 0
    dist, pred = g.dijkstra(0)
    print("=== DIJKSTRA origem 0 ===")
    print(f"Distancias: {[dist[i] for i in range(g.num_vertices)]}")
    print(f"Pais: {[pred[i] for i in range(g.num_vertices)]}")
    
    # Processa e imprime a menor rota reconstruída ponto a ponto de 0 até o destino 5
    cam_5 = g.reconstruir_caminho(pred, 5)
    print(f"Caminho 0 -> 5: {' -> '.join(map(str, cam_5))}")
    print(f"Custo: {dist[5]}")
    
    # Processa e imprime a menor rota reconstruída ponto a ponto de 0 até o destino 8
    cam_8 = g.reconstruir_caminho(pred, 8)
    print(f"Caminho 0 -> 8: {' -> '.join(map(str, cam_8))}")
    print(f"Custo: {dist[8]}")
    print("\n" + "="*30 + "\n")

    # Execução do Experimento 2: Dijkstra partindo de outro vértice (Escolha: Vértice 3)
    dist_3, _ = g.dijkstra(3)
    print(f"=== DIJKSTRA origem 3 ===\nDistancias: {[dist_3[i] for i in range(g.num_vertices)]}\n")

    # Execução dos Experimentos 3 e 4: Algoritmo de Prim a partir da origem 0 e origem 3
    arestas_p0, custo_p0, ordem_p0 = g.prim(0)
    print("=== PRIM origem 0 ===")
    print(f"Arestas selecionadas: {arestas_p0}")
    print(f"Ordem de adicao: {ordem_p0}")
    print(f"Custo total: {custo_p0}")
    
    _, custo_p3, _ = g.prim(3)
    print(f"Custo total do Prim iniciando em 3: {custo_p3}\n")

    # Execução do Experimento 5: Algoritmo de Kruskal no mesmo Grafo
    ar_ord, ar_sel, ar_desc, custo_k = g.kruskal()
    print("=== KRUSKAL ===")
    print(f"Lista de arestas ordenadas: {ar_ord}")
    print(f"Arestas selecionadas: {ar_sel}")
    print(f"Arestas descartadas (ciclo): {ar_desc}")
    print(f"Custo total: {custo_k}")
