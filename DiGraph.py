from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.edge_size = 0
        self.mc_count = 0
        self.graph_v = {}  # dict of all the nodes in the graph (int : NodeData)
        self.graph_edges = {}  # dict of all the nodes connected from a node (int : {int : EdgeData})

    def v_size(self) -> int:
        return self.edge_size
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        raise NotImplementedError

    def e_size(self) -> int:
        return len(self.graph_v)
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
        self.edges_to = {}
        for x,y in self.graph_edges:
            if id1 in y:
                self.edges_to[x] = self.graph_edges.get(x).values.get_weight()
        return self.edges_to
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """

    def all_out_edges_of_node(self, id1: int) -> dict:
        self.edges_from = {}
        for x, y in self.graph_edges:
            if x == id1:
                self.edges_from[self.graph_edges.get(x).keys()] = self.graph_edges.get(x).values().get_weight()
        return self.edges_from

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
        if edge in self.graph_edges:
            return False
        self.graph_edges[id1] = {id2 : edge}
        return  True
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        raise NotImplementedError

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        raise NotImplementedError

    def remove_node(self, node_id: int) -> bool:
        if not node_id in self.graph_v:
            return False
        self.graph_v.pop(node_id)
        return True
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """
        raise NotImplementedError

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if not node_id1 in self.graph_edges and not node_id2 in self.graph_edges.values():
            return False
        if node_id2 in self.graph_edges.get(node_id1):
            self.graph_edges.get(node_id1).pop(node_id2)
            return True
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        raise NotImplementedError


class NodeData:

    def __init__(self, key: int = 0, info: str = None, weight: float = 0.0):
        self.tag = -1
        self.key = key
        self.info = info
        self.weight = weight

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

    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag

