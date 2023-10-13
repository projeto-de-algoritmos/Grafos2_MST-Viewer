import networkx as nx


class Grafo:
    grafo: nx.Graph()
    pos: dict

    def __init__(self) -> None:
        self.grafo = nx.Graph()
        self.pos = {}

    def criar_grafo(self, entrada):
        for aresta in entrada:
            no1, no2, peso = aresta.strip().split(' ')
            try:
                peso = int(peso)
            except ValueError:
                return False
            self.criar_aresta(no1, no2, peso)
    
        self.pos = nx.circular_layout(self.grafo)
        return True
    
    def criar_no(self, nome: str, posicao: tuple) -> None:
        self.grafo.add_node(nome, pos=posicao)

    def reset(self) -> None:
        self.grafo.clear()
        self.pos.clear()

    def get_arestas(self):
        return list(self.grafo.edges)

    def criar_aresta(self, no_1, no_2, peso) -> None:
        self.grafo.add_edge(no_1, no_2, weight=peso)

    def remover_no(self, no):
        if no in self.grafo:
            self.grafo.remove_node(no)
            return True
        return False

    def criar_mst(self):
        mst, peso_total = self.prim()
        return mst, peso_total
    
    def prim(self):
        mst = nx.Graph()
        no_inicial = list(self.grafo.nodes())[0]
        nos_mst = set([no_inicial])
        peso_total = 0

        arestas = [(no_inicial, vizinho, data['weight']) for vizinho, data in self.grafo[no_inicial].items()]
        arestas.sort(key=lambda x: x[2])

        while len(nos_mst) < len(self.grafo.nodes()):
            u, v, weight = arestas.pop(0)
            
            if v not in nos_mst:
                mst.add_edge(u, v, weight=weight)
                nos_mst.add(v)
                peso_total += weight
                
                for vizinho, data in self.grafo[v].items():
                    if vizinho not in nos_mst:
                        arestas.append((v, vizinho, data['weight']))
                        arestas.sort(key=lambda x: x[2])

        return mst, peso_total

    
    def get_rotulo(self):
        return nx.get_edge_attributes(self.grafo, 'weight')
