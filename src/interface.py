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
    medium_pad = 15
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

    def criar_janelas(self):
        esquerda = ttk.Frame(self.root)
        esquerda.pack(
            side="left", padx=self.small_pad, pady=self.small_pad, expand=True
        )

        direita = ttk.Frame(self.root, height=400, width=650, style="Custom.TFrame")
        direita.pack(
            side="right", padx=self.small_pad, pady=self.small_pad, expand=True
        )

        return esquerda, direita

    def inserir_widget(self, janela: ttk.Frame, args: dict):
        rotulo = ttk.Label(janela, text=args["rotulo"])
        rotulo.pack()

        entrada = ttk.Entry(janela, width=args["entrada"])
        entrada.pack(pady=self.small_pad)

        if "botao" in args:
            botao = ttk.Button(
                janela, text=args["botao"], command=args["comando_botao"]
            )
            botao.pack()

        spacer = tk.Label(janela, text="", height=args["espacamento"])
        spacer.pack()

        return entrada

    def criar_widgets(self):
        janela_esq, janela_dir = self.criar_janelas()

        # Widget de inserir arestas ----------------------------------------------------------------------
        inserir_arestas = {
            "rotulo": "Insira as arestas: (Ex: nó1 nó2 peso, ...)",
            "entrada": 40,
            "botao": "Inserir",
            "comando_botao": self.criar_grafo,
            "espacamento": 2,
        }
        self.arestas_entrada = self.inserir_widget(janela_esq, inserir_arestas)

        # Widget de remover nó --------------------------------------------------------------------------
        remover_no = {
            "rotulo": "Insira o nó que deseja remover:",
            "entrada": 15,
            "botao": "Remover",
            "comando_botao": self.remover_no,
            "espacamento": 2,
        }
        self.remove_entrada = self.inserir_widget(janela_esq, remover_no)

        # Widgets de peso ------------------------------------------------------------------------------
        escolher_peso = {
            "rotulo": "Insira o peso da aresta:",
            "entrada": 15,
            "espacamento": 1,
        }
        self.peso_entrada = self.inserir_widget(janela_esq, escolher_peso)

        # Widget da MST --------------------------------------------------------------------------------
        separator = tk.Frame(
            janela_esq, bd=10, relief="sunken", height=2, background="black"
        )
        separator.pack(side="top", fill="x")

        botao_frame = ttk.Frame(janela_esq)
        botao_frame.pack(pady=self.small_pad)

        limpar_botao = ttk.Button(
            botao_frame, text="Limpar", command=self.reset, bootstyle="danger"
        )
        limpar_botao.pack(side="left", padx=self.small_pad, fill="both", expand=True)

        mst_botao = ttk.Button(
            botao_frame, text="Gerar MST", command=self.exibir_mst, bootstyle="success"
        )
        mst_botao.pack(side="left", padx=self.small_pad, fill="both", expand=True)

        # Widget da Figura --------------------------------------------------------------------------------
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.grafo_canvas = FigureCanvasTkAgg(self.figura, master=janela_dir)
        self.grafo_canvas_widget = self.grafo_canvas.get_tk_widget()
        self.grafo_canvas_widget.pack(padx=10, pady=10)

        self.grafo_canvas.mpl_connect("button_press_event", self.on_click)

    def reset(self):
        self.grafo.reset()
        self.exibir_grafo()

    def criar_grafo(self):
        if self.arestas_entrada.get():
            if self.grafo.criar_grafo(self.arestas_entrada.get().split(",")):
                self.exibir_grafo()
                self.arestas_entrada.delete(0, "end")
            else:
                tk.messagebox.showwarning("Aviso", "O peso deve ser um número inteiro.")

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
        if self.grafo.pos:
            if nx.is_connected(self.grafo.grafo):
                mst, peso_total = self.grafo.criar_mst()
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
                tk.messagebox.showinfo(
                    "Sucesso", f"Soma dos pesos das arestas utilizadas: {peso_total}"
                )
            else:
                tk.messagebox.showwarning(
                    "Aviso", "Para gerar uma MST, o grafo deve ser conectado."
                )
        else:
            tk.messagebox.showwarning("Aviso", "Crie um grafo antes de exibir a MST.")

    def encontrar_no_clicado(self, event):
        if self.grafo.pos is not None:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                for node, pos in self.grafo.pos.items():
                    node_x, node_y = pos
                    # Vamos considerar que o nó tem um raio de 0.1 para clique
                    if (x - node_x) ** 2 + (y - node_y) ** 2 <= 0.1**2:
                        return node
        return None

    def conectar_nos(self, no_selecionado, peso):
        if self.primeiro_no_selecionado is None:
            self.primeiro_no_selecionado = no_selecionado
        else:
            segundo_no_selecionado = no_selecionado
            self.grafo.criar_aresta(
                self.primeiro_no_selecionado, segundo_no_selecionado, peso
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
                node_label = f"{len(self.grafo.get_nos()) + 1}"
                i = 1
                for no in self.grafo.grafo.nodes:
                    if node_label == self.grafo.grafo.nodes[no].get("name", None):
                        i += 1
                    else:
                        node_label = f"{len(self.grafo.get_nos()) + i}"
                self.grafo.criar_no(node_label, posicao=(x, y))
                self.grafo.pos[node_label] = (x, y)
                self.exibir_grafo()

                if self.primeiro_no_selecionado is not None:
                    segundo_no_selecionado = node_label
                    peso_entrada = self.peso_entrada.get()
                    peso = int(peso_entrada) if peso_entrada.isdigit() else 1
                    self.grafo.criar_aresta(
                        self.primeiro_no_selecionado,
                        segundo_no_selecionado,
                        peso,
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
            self.remove_entrada.delete(0, "end")
        else:
            tk.messagebox.showwarning("Aviso", "O nó deve estar presente no grafo.")

        self.exibir_grafo()
