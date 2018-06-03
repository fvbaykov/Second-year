import sys
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import networkx as nx
import matplotlib.pyplot as plt 

def open_model(m):
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)
    return(model)

def create_graph(words, model):
    G = nx.Graph()
    for i in range(len(words)):
        G.add_node(i, label = words[i])
        for j in range(i):
            if words[i] in model:
                if words[j] in model:
                    if model.similarity(words[i], words[j]) > 0.5:
                        G.add_edge(i,j)
    return(G)

def characteristics(G):
    deg = nx.degree_centrality(G)
    print('Узлы в порядке убывания центральности: ')
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        print(nodeid, sep = '; ')
    print('Радиус графа равен ', nx.radius(G))
    print('Средняя кластеризация графа равна ', nx.average_clustering(G))
    print('Кластерный коэффициент графа равен ', nx.transitivity(G))

def draw_graph(G):
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=70)
    nx.draw_networkx_edges(G, pos, edge_color='green')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='Arial')
    plt.axis('off')
    plt.show() 

def main():
    m = 'ruscorpora_upos_skipgram_300_10_2017.bin.gz'
    model = open_model(m)
    words = ['рубашка_NOUN', 'рубашечка_NOUN', 'рубашонка_NOUN', 'блузка_NOUN', 'блуза_NOUN', 'футболка_NOUN', 'майка_NOUN', 'безрукавка_NOUN', 'косоворотка_NOUN', 'сорочка_NOUN']
    graph = create_graph(words, model)
    characteristics(graph)
    draw_graph(graph)

a = main()
