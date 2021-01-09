from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.edge_size = 0
        self.mc_count = 0
        self.graph_v = {}  # dict of all the nodes in the graph (int : NodeData)
        self.graph_edges_out = {}  # dict of all the nodes connected from a node (int : {int : EdgeData})
        self.graph_edges_in = {}  # dict of all the nodes connected to a node (int : {int : EdgeData})

    def v_size(self) -> int:
        return len(self.graph_v.keys())
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        raise NotImplementedError

    def e_size(self) -> int:
        return self.edge_size
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        raise NotImplementedError

    def get_all_v(self) -> dict:
        return self.graph_v
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """

    def all_in_edges_of_node(self, id1: int) -> dict:
        dic_return = {}
        for x in dict(self.graph_edges_in[id1]).keys():
            dic_return[x] = self.graph_edges_in[id1][x].weight
        return dic_return
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """

    def all_out_edges_of_node(self, id1: int) -> dict:
        dic_return = {}
        for x in dict(self.graph_edges_out[id1]).keys():
            dic_return[x] = self.graph_edges_out[id1][x].weight
        return dic_return

        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """

    def get_mc(self) -> int:
        return self.mc_count
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        raise NotImplementedError

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        edge = EdgeData(id1, id2, weight)
        if edge.src in self.graph_edges_out.keys():
            if edge.dest in self.graph_edges_out[edge.src].keys():
                return False
            else:
                self.graph_edges_out[edge.src][edge.dest] = edge
                self.edge_size += 1
        else:
            self.graph_edges_out[edge.src] = {edge.dest: edge}
            self.edge_size += 1
        if edge.dest in self.graph_edges_in.keys():
            self.graph_edges_in[edge.dest][edge.src] = edge
        else:
            self.graph_edges_in[edge.dest] = {edge.src: edge}
        return True
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        raise NotImplementedError

    def add_node(self, node_id: int, pos: tuple = (0, 0, 0)) -> bool:
        if node_id in self.graph_v.keys():
            return False
        self.graph_v[node_id] = NodeData(node_id, "", 0.0, pos)
        return True

        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        raise NotImplementedError

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.graph_v.keys():
            self.graph_v.pop(node_id)
            if node_id in self.graph_edges_out.keys():
                dict_in = self.graph_edges_out.pop(node_id)  # dict_in = dict
                for x in dict_in.keys():
                    self.graph_edges_in[x].pop(node_id)
            return True
        return False

        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """
        raise NotImplementedError

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self.graph_edges_out.keys():
            if node_id2 in self.graph_edges_out[node_id1].keys():
                self.graph_edges_out.get(node_id1).pop(node_id2)
                self.graph_edges_in.get(node_id2).pop(node_id1)
                self.edge_size -= 1
                return True
        return False
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        raise NotImplementedError


class NodeData:

    def __init__(self, key: int = 0, info: str = None, weight: float = 0.0, pos: tuple = (0, 0, 0)):
        self.tag = -1
        self.key = key
        self.info = info
        self.weight = weight
        self.pos = GeoLocation(pos)  # a tuple himself

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag

    def get_pos(self):
        return self.pos

    def set_tag(self, pos):
        self.pos = pos


class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight
        self.info = ""

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.weight

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    # def get_tag(self):
    #     return self.tag
    #
    # def set_tag(self, tag):
    #     self.tag = tag


class GeoLocation:
    def __init__(self, pos: tuple = (0, 0, 0)):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def get_pos(self):
        tup = (self.x, self.y, self.z)
        return tup


if __name__ == '__main__':
    # def check0():
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
    # dic = g.get_all_v()
    # for x in dic.values():
    #     print(x.key)
    # print(dic[1].pos.x)

    # with open('data.txt', 'w') as outfile:
    #     json.dump(json.dumps(g), outfile)
    # g_algo = GraphAlgo(g)
    # print(g_algo.shortest_path(0, 3))
    # g_algo.plot_graph()
