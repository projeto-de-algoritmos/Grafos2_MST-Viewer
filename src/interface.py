import networkx as nx
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from grafo import Grafo


class InterfaceGrafica:
    grafo: Grafo
    small_pad = 10
    medium_pad = 20
    node_color = "skyblue"
    font_color = "black"
    edge_color = "black"
    mst_edge_color = "red"
    edge_label_color = "red"
    node_size = 700
    edge_width = 2
    font_weight = "bold"

    def __init__(self, root):
        self.root = root
        self.grafo = Grafo()
        self.root.title("Visualização de MST")
        self.primeiro_no_selecionado = None
        self.style = Style(theme="lumen")
        self.style.configure("Custom.TFrame", background="lightgray")
        self.criar_widgets()

    def criar_widgets(self):
        janela_esq = ttk.Frame(self.root)
        janela_esq.pack(side="left", padx=self.small_pad, pady=self.small_pad, expand=True)

        janela_dir = ttk.Frame(self.root, height=400, width=650, style="Custom.TFrame")
        janela_dir.pack(side="right", padx=self.small_pad, pady=self.small_pad, expand=True)

        # Widgets de inserir arestas -------------------------------------------------------------------
        arestas_rotulo = ttk.Label(janela_esq, text="Insira as arestas: (Ex: nó1 nó2 peso, ...)")
        arestas_rotulo.pack()

        self.arestas_entrada = ttk.Entry(janela_esq, width=40)
        self.arestas_entrada.pack(pady=self.small_pad)

        arestas_botao = ttk.Button(janela_esq, text="Inserir", command=self.criar_grafo)
        arestas_botao.pack()

        spacer = tk.Label(janela_esq, text="", height=2)
        spacer.pack()

        # Widgets de remover nó ------------------------------------------------------------------------------
        remove_rotulo = ttk.Label(janela_esq, text="Insira o nó que deseja remover:")
        remove_rotulo.pack()
        
        self.remove_entrada = ttk.Entry(janela_esq)
        self.remove_entrada.pack(pady=self.small_pad)

        remove_botao = ttk.Button(janela_esq, text="Remover", command=self.remover_no)
        remove_botao.pack()

        spacer = tk.Label(janela_esq, text="", height=2)
        spacer.pack()

        # Widgets de peso ------------------------------------------------------------------------------
        peso_rotulo = ttk.Label(janela_esq, text="Insira o peso da aresta:")
        peso_rotulo.pack()
        
        self.peso_entrada = ttk.Entry(janela_esq)
        self.peso_entrada.pack(pady=self.small_pad)

        spacer = tk.Label(janela_esq, text="", height=1)
        spacer.pack()

        # Widget da MST --------------------------------------------------------------------------------
        separator = tk.Frame(janela_esq, bd=10, relief='sunken', height=2, background='black')
        separator.pack(side='top', fill='x')

        mst_botao = ttk.Button(janela_esq, text="Gerar MST",  command=self.exibir_mst, bootstyle="danger")
        mst_botao.pack(pady=self.small_pad)

        # Widget da Figura --------------------------------------------------------------------------------
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.grafo_canvas = FigureCanvasTkAgg(self.figura, master=janela_dir)
        self.grafo_canvas_widget = self.grafo_canvas.get_tk_widget()
        self.grafo_canvas_widget.pack(padx=10, pady=10)

    def criar_grafo(self):
        self.grafo.reset()
        self.grafo.criar_grafo(self.arestas_entrada.get().split(','))
        self.exibir_grafo()

    def exibir_grafo(self):
        self.figura.clear()
        
        nx.draw(
            G=self.grafo.grafo,
            pos=self.grafo.pos,
            with_labels=True,
            font_weight=self.font_weight,
            node_size=self.node_size,
            node_color=self.node_color,
            font_color=self.font_color,
            edgelist=self.grafo.get_arestas(),
            width=self.edge_width,
            edge_color=self.edge_color,
            ax=self.figura.add_subplot(111),
        )
        
        # Desenhar labels de arestas TODO: desativar atraves de um switch
        edge_labels = self.grafo.get_rotulo()
        nx.draw_networkx_edge_labels(
            G=self.grafo.grafo,
            pos=self.grafo.pos,
            horizontalalignment="center",
            verticalalignment="bottom",
            clip_on=False,
            rotate=False,
            edge_labels=edge_labels,
            font_color=self.edge_label_color,
            ax=self.figura.gca(), 
        )
        
        self.grafo_canvas.draw()

    def exibir_mst(self):
        # TODO: implementar manualmente e checar se o grafo é conectado
        if self.grafo.pos:
            mst = self.grafo.criar_mst()
            nx.draw(
                G=mst,
                pos=self.grafo.pos,
                with_labels=True,
                font_weight=self.font_color,
                node_size=self.node_size,
                node_color=self.node_color,
                font_color=self.font_color,
                edgelist=list(mst.edges()),
                width=self.edge_width,
                edge_color=self.mst_edge_color,
                ax=self.figura.add_subplot(111),
            )
            self.grafo_canvas.draw()
        else:
            tk.messagebox.showwarning(
                "Aviso", "Crie um grafo antes de exibir a MST."
            )   

    def encontrar_no_clicado(self, event):
        if self.grafo.pos is not None:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                for node, pos in self.grafo.pos.items():
                    node_x, node_y = pos
                    # Vamos considerar que o nó tem um raio de 0.1 para clique
                    if (x - node_x) ** 2 + (y - node_y) ** 2 <= 0.1 ** 2:
                        return node
        return None

    def conectar_nos(self, no_selecionado, peso):
        if self.primeiro_no_selecionado is None:
            self.primeiro_no_selecionado = no_selecionado
        else:
            segundo_no_selecionado = no_selecionado
            self.grafo.add_edge(
                self.primeiro_no_selecionado, segundo_no_selecionado, weight=peso
            )
            self.grafo.get_arestas().append(
                (self.primeiro_no_selecionado, segundo_no_selecionado, peso)
            )
            self.primeiro_no_selecionado = None
            self.exibir_grafo()

    def on_click(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            no_clicado = self.encontrar_no_clicado(event)
            
            if no_clicado is not None:
                peso_entrada = self.peso_entrada.get()
                peso = int(peso_entrada) if peso_entrada.isdigit() else 1
                self.conectar_nos(no_clicado, peso)
            else:
                node_label = f"{len(self.grafo.nodes) + 1}"
                self.grafo.add_node(node_label, pos=(x, y))
                self.grafo.pos[node_label] = (x, y)
                self.exibir_grafo()
                
                if self.primeiro_no_selecionado is not None:
                    segundo_no_selecionado = node_label
                    peso_entrada = self.peso_entrada.get()
                    peso = int(peso_entrada) if peso_entrada.isdigit() else 1
                    self.grafo.add_edge(
                        self.primeiro_no_selecionado,
                        segundo_no_selecionado,
                        weight=peso
                    )
                    self.grafo.get_arestas().append(
                        (self.primeiro_no_selecionado, segundo_no_selecionado)
                    )
                    self.primeiro_no_selecionado = None
                    self.exibir_grafo()
                else:
                    self.primeiro_no_selecionado = node_label
   
    def remover_no(self):
        no_a_remover = self.remove_entrada.get()

        self.grafo.remover_no(no_a_remover)

        if self.grafo.pos and no_a_remover in self.grafo.pos:
            del self.grafo.pos[no_a_remover]

        self.exibir_grafo()