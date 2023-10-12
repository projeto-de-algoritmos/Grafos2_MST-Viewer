# MST Visualizer

[Vídeo de apresentação]()

**Número da Lista**: 1<br>
**Conteúdo da Disciplina**: Grafos 2<br>

## Alunos

| Matrícula  | Aluno                        |
| ---------- | ---------------------------- |
| 19/0036567 | Pedro Lucas Cassiano Martins |
| 19/0020814 | Vinícius Roriz               |

## Sobre

O projeto MST Visualizer é o segundo trabalho da dupla para a disciplina de Projeto de Algoritmos e remete ao segundo conteúdo dos métodos de travessia de grafos abrangendo Djikistra, Prim e Kruskal.
O objetivo do projeto é criar uma janela interativa onde o usuário pode criar grafos e tentar desenhar a MST ou pedir para o aplicativo gerar a MST desse grafo utilizando um dos algoritmos aprendidos em sala de aula (Prim ou Kruskal). O aplicativo cria grafos aleatórios baseado nas conexões e pesos descritas por texto pelo usuário, permite que o usuário crie os nós e os conecte com o clique do mouse, permite que o usuário clique nas arestas para desenhar a MST, e gera a MST do grafo desenhado na tela.

## Screenshots

![1](assets/image-2.png)
![2](assets/image.png)
![3](assets/image-1.png)

## Instalação

**Linguagem**: Python<br>

##### Crie um ambiente virtual:

`$ python3 -m venv venv `

##### Entre no ambiente virtual

`$ . venv/bin/activate`
ou
` .\venv\Script\activate`

##### Instale os requirements

`$ pip install -r requirements.txt`

##### Execute a main.py

`$ python3 src/main.py`

## Uso

Na interface do gradio:

1.  Escolha um dos exemplos na parte dos examples abaixo de "Clear" e "Submit" ou arraste um dos labirintos gerados pelo projeto [Kruskal Maze Generator](https://github.com/projeto-de-algoritmos/Grafos2_KruskalMazeGenerator) à janela de upload ou clique na janela de upload e suba um labirinto feito pelo mesmo projeto mencionado
2.  Clique em "Submit" e espere o aplicativo resolver seu labirinto!
