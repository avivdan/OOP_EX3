from typing import List
import json
from GraphInterface import GraphInterface


class GraphAlgoInterface:
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.graph = GraphInterface()

    def get_graph(self) -> GraphInterface:
        return self.graph

    """
    :return: the directed graph on which the algorithm works on.
    """

    def load_from_json(self, file_name: str) -> bool:

        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            with open("wow.txt") as file:
                s = json.load(file)
            for node in s["Nodes"]:
                self.graph.add_node(node["node_id"], node["node_position"])
            for edge in s["Edges"]:
                self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            file.close()
        raise NotImplementedError

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        with open(file_name, 'w') as file:
            try:
                d = {"Nodes": [], "Edges": []}
                for node_id in self.graph.get_all_v().keys():
                    d["Nodes"].append({"node_id": node_id,
                                       "pos": (
                                           self.get_all_v()[node_id].pos.x,
                                           self.get_all_v()[node_id].pos.y,
                                           self.get_all_v()[node_id].pos.z
                                       )
                                       })
                for src in self.graph.graph_edges_out.keys():
                    for dest, weight in self.graph.all_out_edges_of_node(src).items():
                        d["Edges"].append({"src": src, "w": weight, "dest": dest})

                json.dump(d, file)
                return True
            except Exception as e:
                print("Error save to Json: " + e.__repr__())
                return False
            finally:
                file.close()
        raise NotImplementedError

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
        raise NotImplementedError

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        raise NotImplementedError

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        raise NotImplementedError

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError
