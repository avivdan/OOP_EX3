import math
from typing import List

from GraphInterface import GraphInterface
from components import *
import heapq
import matplotlib.pyplot as plt
import numpy as np


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.edge_size = 0
        self.mc_count = 0
        self.graph_v = dict()  # dict of all the nodes in the graph (int : NodeData)
        self.graph_edges_out = dict()  # dict of all the nodes connected from a node (int : {int : EdgeData})
        self.graph_edges_in = dict()  # dict of all the nodes connected to a node (int : {int : EdgeData})

    def __repr__(self):
        s = "|V|={} , |E|={} , MC={}\n".format(len(self.get_all_v().keys()), self.edge_size, self.mc_count)
        for key in self.graph_v.keys():
            s += "from {}:\n".format(self.graph_v[key])
            s += "\t To: "
            for w in self.all_out_edges_of_node(key).keys():
                s += str(w)
                s += " | "
            s += "\n"
            # s += "\t from:\t"
            # for w in self.all_out_edges_of_node(key).keys():
            #     s += str(w)
            #     s += ", "
            s += "\n"
        return s

    def get_node(self, node_id):
        if node_id is not None:
            return self.get_all_v()[node_id]
        else:
            return None

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.graph_v.keys())
        # raise NotImplementedError

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.edge_size
        # raise NotImplementedError

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        return self.graph_v

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        dic_return = {}
        if id1 in self.graph_edges_in.keys():
            for x in self.graph_edges_in[id1].keys():
                dic_return[x] = self.graph_edges_in[id1][x].weight
            return dic_return
        else:
            return {}

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        dic_return = {}
        if id1 in self.graph_edges_out.keys():
            for x in self.graph_edges_out[id1].keys():
                dic_return[x] = self.graph_edges_out[id1][x].weight
            return dic_return
        else:
            return {}

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc_count
        # raise NotImplementedError

    # *****************************************************************

    def try_get_along(self, node: NodeData, min_x: int, max_x: int, min_y: int, max_y: int) -> tuple:
        node_to = []
        if len(self.all_out_edges_of_node(node.key)) > 0:
            for node_dest in self.all_out_edges_of_node(node.key).keys():
                if self.get_node(node_dest).pos is not None:
                    node_to.append(self.get_node(node_dest))
                if len(node_to) > 1:
                    x = (node_to[0].pos.x + node_to[1].pos.x) / 2
                    y = (node_to[0].pos.y + node_to[1].pos.y) / 2
                    z = (node_to[0].pos.z + node_to[1].pos.z) / 2
                    return_tu = (x, y, z)
                    return return_tu
        node_from = []
        if len(self.all_in_edges_of_node(node.key)) > 0:
            for node_src in self.all_in_edges_of_node(node.key).keys():
                if self.get_node(node_src).pos is not None:
                    node_from.append(self.get_node(node_src))
                if len(node_from) > 1:
                    x = (node_from[0].pos.x + node_from[1].pos.x) / 2
                    y = (node_from[0].pos.y + node_from[1].pos.y) / 2
                    z = (node_from[0].pos.z + node_from[1].pos.z) / 2
                    return_tu = (x, y, z)
                    return return_tu
        if len(node_to) > 0 and len(node_from) > 0:
            x = (node_to[0].pos.x + node_from[0].pos.x) / 2
            y = (node_to[0].pos.y + node_from[0].pos.y) / 2
            z = (node_to[0].pos.z + node_from[0].pos.z) / 2
            return_tu = (x, y, z)
            return return_tu
        if len(node_to) > 0:
            x = (node_to[0].pos.x + np.random.uniform(min_x, max_x))/2
            y = (node_to[0].pos.y + np.random.uniform(min_y, max_y))/2
            z = node_to[0].pos.z
            return_tu = (x, y, z)
            return return_tu
        if len(node_from) > 0:
            x = (node_from[0].pos.x + np.random.uniform(min_x, max_x))/2
            y = (node_from[0].pos.y + np.random.uniform(min_y, max_y))/2
            z = node_from[0].pos.z
            return_tu = (x, y, z)
            return return_tu
        else:
            x = np.random.uniform(min_x, max_x) / 2
            y = np.random.uniform(min_y, max_y) / 2
            z = 0
            return_tu = (x, y, z)
            return return_tu

    # ******************************************************************

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        edge = EdgeData(id1, id2, weight)
        if edge.src in self.graph_edges_out.keys():
            if edge.dest in self.graph_edges_out[edge.src].keys():
                return False
            else:
                self.graph_edges_out[edge.src][edge.dest] = edge
        else:
            self.graph_edges_out[edge.src] = {edge.dest: edge}
        if edge.dest in self.graph_edges_in.keys():
            self.graph_edges_in[edge.dest][edge.src] = edge
        else:
            self.graph_edges_in[edge.dest] = {edge.src: edge}
        self.edge_size += 1
        self.mc_count += 1
        return True
        # raise NotImplementedError

    def add_node(self, node_id: int = None, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id in self.graph_v.keys():
            return False
        if node_id is not None:
            if pos is not None:
                self.graph_v[node_id] = NodeData(key=node_id, pos=pos)
                self.mc_count += 1
                return True
            self.graph_v[node_id] = NodeData(key=node_id)
            self.mc_count += 1
            return True
        if pos is not None:
            self.graph_v[node_id] = NodeData(pos=pos)
            self.mc_count += 1
            return True
        self.graph_v[node_id] = NodeData()
        self.mc_count += 1
        return True
        # raise NotImplementedError

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id in self.graph_v.keys():
            self.graph_v.pop(node_id)
            self.mc_count += 1
            if node_id in self.graph_edges_out.keys():
                dict_in = self.graph_edges_out.pop(node_id)  # dict_in = dict
                for x in dict_in.keys():
                    self.graph_edges_in[x].pop(node_id)
            return True
        return False
        # raise NotImplementedError

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 in self.graph_edges_out.keys():
            if node_id2 in self.graph_edges_out[node_id1].keys():
                self.graph_edges_out.get(node_id1).pop(node_id2)
                self.graph_edges_in.get(node_id2).pop(node_id1)
                self.edge_size -= 1
                self.mc_count += 1
                return True
        return False
        # raise NotImplementedError

    # *+*+*+*+*+*+*+*+*+*++*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+
    # for testing purposes only

    def shortest_path(self, src: int, dst: int) -> (float, list):
        if src not in self.get_all_v() or dst not in self.get_all_v():
            return None
        visited = []
        heap_min = []
        prev_nodes = dict()
        for x in self.graph_v.keys():
            self.get_all_v()[x].tag = math.inf
        self.get_all_v()[src].tag = 0
        heapq.heappush(heap_min, (self.get_all_v()[src].tag, src))

        while len(heap_min) > 0:
            v = heapq.heappop(heap_min)[1]  # get the node with the smallest tag
            # if len(self.all_out_edges_of_node())
            for node_id in self.all_out_edges_of_node(v).keys():  # from neighbors
                if node_id not in visited:  # check if visited
                    if node_id in self.all_out_edges_of_node(v).keys():  # not search null
                        alt_path = self.get_all_v()[v].tag + self.all_out_edges_of_node(v)[node_id]  # tag + edge weight
                        if self.get_all_v()[node_id].tag > alt_path:
                            self.graph_v[node_id].tag = alt_path
                            prev_nodes[node_id] = v
                            heapq.heappush(heap_min, (alt_path, node_id))  # add to heap the node id by tag
        node_key = dst
        li_return = []
        while self.get_all_v()[node_key].tag > 0:
            li_return.append(node_key)
            node_key = prev_nodes[node_key]
        li_return.append(node_key)
        li_return.reverse()
        return self.get_all_v()[dst].tag, li_return

    def bfs_out(self, node_id: int) -> List:
        visited = {}
        for node in self.get_all_v().keys():
            visited[node] = False
        queue = []
        visited[node_id] = True
        queue.append(node_id)

        while queue:
            s = queue.pop(0)
            for i in self.all_out_edges_of_node(s).keys():
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True

        list_return = []
        for node in visited:
            if visited[node]:
                list_return.append(node)
        list_return.remove(node_id)
        return list_return

    def bfs_in(self, node_id: int) -> List:
        visited = {}
        for node in self.get_all_v().keys():
            visited[node] = False
        queue = []
        visited[node_id] = True
        queue.append(node_id)

        while queue:
            s = queue.pop(0)
            for i in self.all_in_edges_of_node(s).keys():
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True

        list_return = []
        for node in visited:
            if visited[node]:
                list_return.append(node)
        list_return.remove(node_id)
        return list_return

    # *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*


if __name__ == '__main__':
    def check0():
        """
        This function tests the naming (main methods of the DiGraph class, as defined in GraphInterface.
        :return:
        """


    g = DiGraph()  # creates an empty directed graph
    for n in range(4):
        g.add_node(n)
    r = NodeData(pos=(4, 5, 3))
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(1, 0, 1.1)
    g.add_edge(2, 3, 1.1)
    g.add_edge(1, 3, 0.2)
    print(g.bfs_in(1))
    print(g.bfs_out(1))
    print(set(g.bfs_in(1)) & set(g.bfs_out(1)))
    # a = list(g.graph_v.keys())
    # plt.plot(a, "ro")
    # for node_id in g.graph_v.keys():
    #     for i in g.all_out_edges_of_node(node_id):
    #         plt.arrow()
    # plt.plot(a, [2, 4, 6, 8], "ro")
    print(len(g.graph_v.values()))
    # for node in g.get_all_v().values():
    #     plt.arrow(node.key, node.key, 1, 2)
    #     print(node.key)
    # plt.axis([0, 6, 0, 20])
    # print("wow")
    # print
    fg = DiGraph()
    fg.add_node(1, (20, 14, 3))
    fg.add_node(2, (3, 1, 4))
    fg.add_node(3)
    fg.add_edge(2, 3, 3)
    fg.add_edge(3, 1, 4)
    fg.add_edge(1, 2, 5)
    a = [[], [], []]

    # asd[0].extend(2)
    not_placed = 0
    for node in fg.get_all_v().values():
        if node.pos is not None:
            a[0].append(node.pos.x)
            a[1].append(node.pos.y)
            a[2].append(node.pos.z)
        else:
            not_placed += 1
    if not_placed == len(fg.get_all_v().values()):
        min_x = 1
        min_y = 1
        max_x = 2
        max_y = 2
        for node in fg.get_all_v().values():
            node.pos = GeoLocation(fg.try_get_along(node, min_x, max_x, min_y, max_y))
            a[0].append(node.pos.x)
            a[1].append(node.pos.y)
            a[2].append(node.pos.z)
    if not_placed > 0:
        if not_placed < 2:
            max_x = max(a[0])
            max_y = max(a[1])
        else:
            max_x = max(a[0]) + 1
            max_y = max(a[1]) + 1
        min_x = min(a[0])
        min_y = min(a[1])
        for node in fg.get_all_v().values():
            if node.pos is None:
                node.pos = GeoLocation(fg.try_get_along(node, min_x, max_x, min_y, max_y))
                a[0].append(node.pos.x)
                a[1].append(node.pos.y)
                a[2].append(node.pos.z)
    margin_x = (min(a[0]) + max(a[0])) / 3
    margin_y = (max(a[1]) + min(a[1])) / 3
    min_x = min(a[0]) - math.fabs(margin_x)
    min_y = min(a[1]) - math.fabs(margin_y)
    max_x = max(a[0]) + math.fabs(margin_x)
    max_y = max(a[1]) + math.fabs(margin_y)

    plt.plot(a[0], a[1], "ro")
    for node in fg.get_all_v().values():
        for dest_node_id in fg.all_out_edges_of_node(node.key).keys():
            dest_node = fg.get_node(dest_node_id)
            plt.arrow(node.pos.x, node.pos.y, (dest_node.pos.x - node.pos.x), (dest_node.pos.y - node.pos.y))
    plt.axis([min_x, max_x, min_y, max_y])
    plt.show()
