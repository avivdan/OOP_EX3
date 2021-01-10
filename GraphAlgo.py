import heapq
import math
from typing import List
import json
from GraphInterface import GraphInterface
from DiGraph import DiGraph


class GraphAlgoInterface:
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.graph = DiGraph()

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    # *************************************************************************************
    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            with open(file_name) as file:
                s = json.load(file)

            for node in s["Nodes"]:
                if "pos" in node:
                    self.graph.add_node(node_id=node["node_id"], pos=node["pos"])
                else:
                    self.graph.add_node(node_id=node["node_id"])
            for edge in s["Edges"]:
                self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            file.close()
        # raise NotImplementedError

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        with open(file_name, 'w') as file:
            try:
                d = {"Nodes": [], "Edges": []}
                for node in self.graph.get_all_v().values():
                    if node.pos is None:
                        d["Nodes"].append({"node_id": node.key})
                    else:
                        d["Nodes"].append({"node_id": node.key,
                                           "pos": (
                                               node.pos.x,
                                               node.pos.y,
                                               node.pos.z
                                           )
                                           })
                for src in self.graph.graph_edges_out.keys():
                    for dest, weight in self.graph.all_out_edges_of_node(src).items():
                        d["Edges"].append({"src": src, "w": weight, "dest": dest})

                json.dump(d, file)
                return True
            except Exception as e:
                print(e)
                return False
            finally:
                file.close()
        # raise NotImplementedError

    # *************************************************************************************

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through

        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])

        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        nodes = self.graph.get_all_v()
        if id1 not in nodes or id2 not in nodes:
            return None
        visited = []
        heap_min = []
        prev_nodes = dict()
        for x in self.graph.graph_v.keys():
            nodes[x].tag = math.inf
        nodes[id1].tag = 0
        heapq.heappush(heap_min, (nodes[id1].tag, id1))

        while len(heap_min) > 0:
            v = heapq.heappop(heap_min)[1]  # get the node with the smallest tag
            for node_id in self.graph.all_out_edges_of_node(v).keys():  # from neighbors
                if node_id not in visited:  # check if visited
                    if node_id in self.graph.all_out_edges_of_node(v).keys():  # not search null
                        alt_path = nodes[v].tag + self.graph.all_out_edges_of_node(v)[node_id]  # tag + edge weight
                        if self.graph.get_all_v()[node_id].tag > alt_path:
                            self.graph.graph_v[node_id].tag = alt_path
                            prev_nodes[node_id] = v
                            heapq.heappush(heap_min, (alt_path, node_id))  # add to heap the node id by tag
        node_key = id2
        li_return = []
        while self.graph.get_all_v()[node_key].tag > 0:
            li_return.append(node_key)
            node_key = prev_nodes[node_key]
        li_return.append(node_key)
        li_return.reverse()
        return self.graph.get_all_v()[id2].tag, li_return

        # raise NotImplementedError

    # ******************************************************************************************************

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        set_in = self.bfs_in(id1)
        set_out = self.bfs_out(id1)
        return list(set_in & set_out)
        # raise NotImplementedError

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        visited = []
        list_return = []
        for node in self.graph.get_all_v().keys():
            if node not in visited:
                SCC_set = self.connected_component(node)
                visited.extend(SCC_set)
                list_return.append(SCC_set)
        return list_return
        # raise NotImplementedError

    def bfs_out(self, node_id: int) -> List:
        visited = {}
        for node in self.graph.get_all_v().keys():
            visited[node] = False
        queue = []
        visited[node_id] = True
        queue.append(node_id)

        while queue:
            s = queue.pop(0)
            for i in self.graph.all_out_edges_of_node(s).keys():
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
        for node in self.graph.get_all_v().keys():
            visited[node] = False
        queue = []
        visited[node_id] = True
        queue.append(node_id)

        while queue:
            s = queue.pop(0)
            for i in self.graph.all_in_edges_of_node(s).keys():
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True

        list_return = []
        for node in visited:
            if visited[node]:
                list_return.append(node)
        list_return.remove(node_id)
        return list_return

    # ******************************************************************************************************

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError
