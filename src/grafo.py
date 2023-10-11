import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfaceGrafica:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Visualização de MST")
        self.layout_original = None
        self.arestas_originais = None
        self.grafo = nx.Graph()
        self.pos = {}  # Inicializamos como um dicionário vazio
        self.desenhando = True
        self.primeiro_no_selecionado = None
        self.criar_widgets()

    def criar_widgets(self):
        # Rótulo e entrada para inserir arestas
        self.rotulo_arestas = ttk.Label(
            self.janela,
            text="Insira as arestas no formato 'nó1 nó2 peso', separadas por vírgulas:",
        )
        self.rotulo_arestas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entrada_arestas = ttk.Entry(self.janela, width=40)
        self.entrada_arestas.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Botão para criar o grafo e exibir
        self.botao_criar_grafo = ttk.Button(
            self.janela, text="Criar Grafo e Exibir", command=self.criar_e_exibir_grafo
        )
        self.botao_criar_grafo.grid(row=2, column=0, columnspan=2, pady=10)

        # Área para exibir o grafo
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.grafo_canvas = FigureCanvasTkAgg(self.figura, master=self.janela)
        self.grafo_canvas_widget = self.grafo_canvas.get_tk_widget()
        self.grafo_canvas_widget.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Botão para exibir a MST
        self.botao_exibir_mst = ttk.Button(
            self.janela, text="Exibir MST", command=self.exibir_mst
        )
        self.botao_exibir_mst.grid(row=4, column=0, columnspan=2, pady=10)

        # Adicionando evento de clique para desenhar nós
        self.grafo_canvas.mpl_connect("button_press_event", self.on_click)

    def criar_e_exibir_grafo(self):
        arestas_input = self.entrada_arestas.get()
        self.grafo = self.criar_grafo(arestas_input)
        self.layout_original = nx.spring_layout(self.grafo)
        self.arestas_originais = list(self.grafo.edges())
        self.pos = self.layout_original
        self.desenhando = True
        self.exibir_grafo()

    def exibir_grafo(self):
        self.figura.clear()
        nx.draw(
            self.grafo,
            self.pos,
            with_labels=True,
            font_weight="bold",
            node_size=700,
            node_color="skyblue",
            font_color="black",
            edgelist=self.arestas_originais,
            width=2,
            edge_color="black",
            ax=self.figura.add_subplot(111),
        )
        self.grafo_canvas.draw()

    def exibir_mst(self):
        if hasattr(self, "grafo") and self.layout_original is not None:
            mst = nx.minimum_spanning_tree(self.grafo)
            nx.draw(
                mst,
                self.layout_original,
                with_labels=True,
                font_weight="bold",
                node_size=700,
                node_color="skyblue",
                font_color="black",
                edgelist=list(mst.edges()),
                width=2,
                edge_color="red",
                ax=self.figura.add_subplot(111),
            )
            self.grafo_canvas.draw()
        else:
            tk.messagebox.showwarning(
                "Aviso", "Crie um grafo antes de exibir a MST."
            )   

    def encontrar_no_clicado(self, event):
        if self.pos is not None:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                for node, pos in self.pos.items():
                    node_x, node_y = pos
                    # Vamos considerar que o nó tem um raio de 0.1 para clique
                    if (x - node_x) ** 2 + (y - node_y) ** 2 <= 0.1 ** 2:
                        return node
        return None

    def conectar_nos(self, no_selecionado):
        if self.primeiro_no_selecionado is None:
            self.primeiro_no_selecionado = no_selecionado
        else:
            segundo_no_selecionado = no_selecionado
            self.grafo.add_edge(
                self.primeiro_no_selecionado, segundo_no_selecionado, weight=1
            )
            self.arestas_originais.append(
                (self.primeiro_no_selecionado, segundo_no_selecionado)
            )
            self.primeiro_no_selecionado = None
            self.exibir_grafo()

    def on_click(self, event):
        if self.desenhando:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                # Verificar se o usuário clicou em algum nó existente
                no_clicado = self.encontrar_no_clicado(event)
                
                if no_clicado is not None:
                    # O usuário clicou em um nó existente
                    self.conectar_nos(no_clicado)
                else:
                    # O usuário clicou em um local vazio, então cria um novo nó
                    node_label = f"Nó {len(self.grafo.nodes) + 1}"
                    self.grafo.add_node(node_label, pos=(x, y))
                    self.pos[node_label] = (x, y)
                    self.exibir_grafo()
                    
                    # Agora, conectamos os nós apenas se o primeiro nó já estiver selecionado
                    if self.primeiro_no_selecionado is not None:
                        segundo_no_selecionado = node_label
                        self.grafo.add_edge(
                            self.primeiro_no_selecionado, segundo_no_selecionado, weight=1
                        )
                        self.arestas_originais.append(
                            (self.primeiro_no_selecionado, segundo_no_selecionado)
                        )
                        self.primeiro_no_selecionado = None
                        self.exibir_grafo()
                    
                    # Se o primeiro nó não estiver selecionado, definimos o nó atual como o primeiro
                    else:
                        self.primeiro_no_selecionado = node_label




    def criar_grafo(self, arestas_input):
        grafo = nx.Graph()

        arestas = arestas_input.split(",")
        for aresta in arestas:
            n1, n2, peso = aresta.strip().split()
            grafo.add_edge(n1, n2, weight=int(peso))

        return grafo


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
