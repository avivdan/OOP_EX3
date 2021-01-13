from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import time
import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np


def load_from_json(file_name: str) -> nx:
    ngx = nx.DiGraph()
    try:
        with open(file_name) as file:
            s = json.load(file)
        for node in s["Nodes"]:
            ngx.add_node(node["id"])
        for edge in s["Edges"]:
            ngx.add_weighted_edges_from([(edge["src"], edge["dest"], edge["w"])])
        return ngx
    except Exception as e:
        print(e)
        return ngx
    finally:
        file.close()
    # raise NotImplementedError


def check():
    """
    Graph: |V|=4 , |E|=5
    {0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 3 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 3: 3: |edges out| 0 |edges in| 2}
    {0: 1}
    {0: 1.1, 2: 1.3, 3: 10}
    (3.4, [0, 1, 2, 3])
    [[0, 1], [2], [3]]
    (2.8, [0, 1, 3])
    (inf, [])
    2.062180280059253 [1, 10, 7]
    17.693921758901507 [47, 46, 44, 43, 42, 41, 40, 39, 15, 16, 17, 18, 19]
    11.51061380461898 [20, 21, 32, 31, 30, 29, 14, 13, 3, 2]
    inf []
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]]
    """
    check0()
    check1()
    check2()


def check0():
    """
    This function tests the naming (main methods of the DiGraph class, as defined in GraphInterface.
    :return:
    """
    g = DiGraph()  # creates an empty directed graph
    for n in range(4):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(2, 3, 1.1)
    g.add_edge(1, 3, 1.9)
    g.remove_edge(1, 3)
    g.add_edge(1, 3, 10)
    print(g)  # prints the __repr__ (func output)
    print(g.get_all_v())  # prints a dict with all the graph's vertices.
    print(g.all_in_edges_of_node(1))
    print(g.all_out_edges_of_node(1))
    g_algo = GraphAlgo(g)
    print(g_algo.shortest_path(0, 3))
    g_algo.plot_graph()


def check1():
    """
       This function tests the naming (main methods of the GraphAlgo class, as defined in GraphAlgoInterface.
    :return:
    """
    g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
    file = "data/A4.json"
    g_algo.load_from_json(file)  # init a GraphAlgo from a json file
    print(g_algo.connected_components())
    print(g_algo.shortest_path(0, 3))
    print(g_algo.shortest_path(3, 1))
    g_algo.save_to_json(file + '_saved')
    g_algo.plot_graph()


def check2():
    """ This function tests the naming, basic testing over A5 json file.
      :return:
      """
    g_algo = GraphAlgo()
    file = 'data/A5.json'
    g_algo.load_from_json(file)
    g_algo.get_graph().remove_edge(13, 14)
    g_algo.save_to_json(file + "_edited")
    dist, path = g_algo.shortest_path(1, 7)
    print(dist, path)
    dist, path = g_algo.shortest_path(47, 19)
    print(dist, path)
    dist, path = g_algo.shortest_path(20, 2)
    print(dist, path)
    dist, path = g_algo.shortest_path(2, 20)
    print(dist, path)
    print(g_algo.connected_component(0))
    print(g_algo.connected_components())
    g_algo.plot_graph()


def check_runtime():
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_10_80_1.json"
    print("G_10_80_1")
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_100_800_1.json"
    print("\nG_100_800_1")
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_1000_8000_1.json"
    print("\nG_1000_8000_1")
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    print("\nG_10000_80000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_10000_80000_1.json"
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    print("\nG_20000_160000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_20000_160000_1.json"
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))
    # **********************************************************************************
    # ----------------------------------------------------------------------------------
    print("\nG_30000_240000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_30000_240000_1.json"
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(file)
    start = time.time()
    graph_algo.shortest_path(1, 3)
    end = time.time()
    print("shortest path : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_components()
    end = time.time()
    print("connected components : ", (end - start))
    #  ==============================================================================
    start = time.time()
    graph_algo.connected_component(4)
    end = time.time()
    print("connected component* : ", (end - start))


def networkX():
    print("G_10_80_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_10_80_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================
    print("G_100_800_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_100_800_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================
    print("G_1000_8000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_1000_8000_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================
    print("G_10000_80000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_10000_80000_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================
    print("G_20000_160000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_20000_160000_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================
    print("G_30000_240000_1")
    file = "/home/aviv/PycharmProjects/OOP_EX3/Graphs_on_circle/G_30000_240000_1.json"
    gnx = load_from_json(file)
    start = time.time()
    nx.shortest_path(gnx, 2, 9)
    end = time.time()
    print("shortest path : ", (end - start))
    start = time.time()
    nx.strongly_connected_components(gnx)
    end = time.time()
    print("SCC : ", (end - start))
    #  =========================================================================
    #  =========================================================================
    #  =========================================================================


def build_bar_chart():
    labels = ["G_10_80_1", "G_100_800_1", "G_1000_8000_1", "G_10000_80000_1", "G_20000_160000_1", "G_30000_240000_1"]
    java_sccs = [0, 0, 0.002, 0.047, 0.106, 0.166]
    python_sccs = [0, 0, 0, 0.004, 0.25, 0.476]
    java_Dijkstra = [0, 0, 0.65, 41.938, 192.605, 353.267]
    python_Dijkstra = [0, 0.002, 0.742, 7.14, 35.856, 89.654]
    java_scc = [0, 0.004, 0.731, 131.712, 617.267, 1419.259]
    python_scc = [0, 0, 0, 0.904, 4.11, 11.078]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, java_sccs, width, label='java')
    rects2 = ax.bar(x + width / 2, python_sccs, width, label='python')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Time Measure')
    ax.set_title('SCC singal')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontSize=6)

    autolabel(rects1)
    autolabel(rects2)
    ax.tick_params(axis='x', which='major', labelsize=6)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # check_runtime()
    # networkX()
    build_bar_chart()
    print("wow")
