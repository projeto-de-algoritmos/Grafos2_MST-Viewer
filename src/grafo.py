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
            self.criar_aresta(no1, no2, peso)
        self.pos = nx.circular_layout(self.grafo)
    
    def criar_no(self, nome: str, posicao: tuple) -> None:
        self.grafo.add_node(nome, pos=posicao)

    def reset(self) -> None:
        self.grafo.clear()

    def get_arestas(self):
        return list(self.grafo.edges)

    def criar_aresta(self, no_1, no_2, peso) -> None:
        self.grafo.add_edge(no_1, no_2, weight=int(peso), lenght=int(peso))

    def remover_no(self, no):
        if no in self.grafo:
            self.grafo.remove_node(no)
            return True
        return False

    def criar_mst(self):
        mst = nx.minimum_spanning_tree(self.grafo)
        return mst
    
    def get_rotulo(self):
        return nx.get_edge_attributes(self.grafo, 'weight')
