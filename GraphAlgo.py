import heapq
import json
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import random

from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from components import *


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self, dg: DiGraph = None):
        if dg is None:
            self.graph = DiGraph()
        else:
            self.graph = dg

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
                    x, y, z = node["pos"].split(',')  # Seperate by ','
                    position = (x, y, z)
                    # node_key = node["node_id"]
                    self.get_graph().add_node(node_id=node["id"], pos=position)  # Add node by the exist id and position
                else:
                    self.graph.add_node(node_id=node["id"])  # Add node by the exist id
            for edge in s["Edges"]:
                self.graph.add_edge(edge["src"], edge["dest"], edge["w"])  # Add edge
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
        with open(file_name, 'w') as file:  # Write to file
            try:
                d = {"Nodes": [], "Edges": []}
                for node in self.graph.get_all_v().values():
                    if node.pos is None:
                        d["Nodes"].append({"id": node.key})
                    else:
                        d["Nodes"].append({"id": node.key,  # Write with position
                                           "pos": (
                                               node.pos.x,
                                               node.pos.y,
                                               node.pos.z
                                           )
                                           })
                for src in self.graph.graph_edges_out.keys():
                    for dest, weight in self.graph.all_out_edges_of_node(src).items():
                        d["Edges"].append({"src": src, "w": weight, "dest": dest})  # Write the edge

                json.dump(d, file)  # Stores d into file
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
        if id1 not in nodes or id2 not in nodes:  # If not exist
            return None
        visited = []  # Visited nodes list
        heap_min = []  # Min binomial heap
        prev_nodes = dict()
        for x in self.graph.graph_v.keys():
            nodes[x].tag = math.inf
        nodes[id1].tag = 0
        heapq.heappush(heap_min, (nodes[id1].tag, id1)) # Push to heap

        while len(heap_min) > 0:
            v = heapq.heappop(heap_min)[1]  # get the node with the smallest tag
            for node_neighbor in self.graph.all_out_edges_of_node(v).keys():  # from neighbors
                if node_neighbor not in visited:  # check if visited
                    # if node_neighbor in self.graph.all_out_edges_of_node(v).keys():  # not search null

                    # visited.append(node_neighbor)
                    alt_path = nodes[v].tag + self.graph.all_out_edges_of_node(v)[
                        node_neighbor]  # tag + edge weight

                    if self.graph.get_all_v()[node_neighbor].tag > alt_path:
                        self.graph.get_node(node_id=node_neighbor).tag = alt_path
                        prev_nodes[node_neighbor] = v
                        heapq.heappush(heap_min, (alt_path, node_neighbor))  # add to heap the node id by tag
            visited.append(v)
        node_key = id2
        li_return = []  # The path
        while self.graph.get_all_v()[node_key].tag > 0:
            li_return.append(node_key)
            if node_key not in prev_nodes.keys():
                return -1, {}
            else:
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
        if id1 not in self.graph.get_all_v().keys():
            return []
        set_in = set(self.bfs_in(id1))  # Set of the connected nodes to id1 and backwards
        set_out = set(self.bfs_out(id1))  # Set of the connected nodes from id1 and onwards
        list1 = [id1]
        list2 = list1 + list(set_in & set_out)  # Put also id1 in the list
        return list2
        # raise NotImplementedError

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        visited = [] # Visited nodes list
        list_return = []
        for node in self.graph.get_all_v().keys():
            if node not in visited:
                SCC_set = self.connected_component(node)
                visited.extend(SCC_set)
                list_return.append(SCC_set)
        return list_return
        # raise NotImplementedError

    def bfs_out(self, node_id: int) -> List:
        visited = {}  # Visited nodes dict
        for node in self.graph.get_all_v().keys():
            visited[node] = False
        queue = []
        visited[node_id] = True
        queue.append(node_id)  # Assert to the queue

        while queue:
            s = queue.pop(0)
            for i in self.graph.all_out_edges_of_node(s).keys():
                if not visited[i]:
                    queue.append(i)  # Assert to the queue
                    visited[i] = True

        list_return = []
        for node in visited:
            if visited[node]:
                list_return.append(node)  # Assert to the list
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

    def get_node(self, node_id):
        return self.graph.get_all_v()[node_id]

    # This function try to place the non positioned nodes and place them on the graph in elegant way,
    # but with a little random placing which don't come out from the graph margins
    def try_get_along(self, node: NodeData, min_x: float, max_x: float, min_y: float, max_y: float) -> tuple:
        node_to = []
        if len(self.get_graph().all_out_edges_of_node(node.key)) > 0:
            for node_dest in self.get_graph().all_out_edges_of_node(node.key).keys():
                if self.get_node(node_dest).pos is not None:
                    node_to.append(self.get_node(node_dest))
                if len(node_to) > 1:
                    x = (node_to[0].pos.x + node_to[1].pos.x +
                         random.uniform(min_x, max_x) - random.uniform(min_x, max_x)) / 3
                    y = (node_to[0].pos.y + node_to[1].pos.y +
                         random.uniform(min_x, max_x) - random.uniform(min_x, max_x)) / 3
                    z = (node_to[0].pos.z + node_to[1].pos.z) / 2
                    return_tu = (x, y, z)
                    return return_tu
        node_from = []
        if len(self.get_graph().all_in_edges_of_node(node.key)) > 0:
            for node_src in self.get_graph().all_in_edges_of_node(node.key).keys():
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
            x = (node_to[0].pos.x + np.random.uniform(min_x, max_x)) / 2
            y = (node_to[0].pos.y + np.random.uniform(min_y, max_y)) / 2
            z = node_to[0].pos.z
            return_tu = (x, y, z)
            return return_tu
        if len(node_from) > 0:
            x = (node_from[0].pos.x + np.random.uniform(min_x, max_x)) / 2
            y = (node_from[0].pos.y + np.random.uniform(min_y, max_y)) / 2
            z = node_from[0].pos.z
            return_tu = (x, y, z)
            return return_tu
        else:
            x = np.random.uniform(min_x, max_x) / 2
            y = np.random.uniform(min_y, max_y) / 2
            z = 0
            return_tu = (x, y, z)
            return return_tu


    def plot_graph(self):
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        positions_plt = [[], [], []]
        not_placed = 0
        for node in self.get_graph().get_all_v().values():
            if node.pos is not None:
                positions_plt[0].append(float(node.pos.x))
                positions_plt[1].append(float(node.pos.y))
                positions_plt[2].append(float(node.pos.z))
            else:
                not_placed += 1
        if not_placed == len(self.get_graph().get_all_v().keys()):
            min_x = 1
            min_y = 1
            max_x = 2
            max_y = 2
            for node in self.get_graph().get_all_v().values():
                node.pos = GeoLocation(self.try_get_along(node, min_x, max_x, min_y, max_y))
                positions_plt[0].append(float(node.pos.x))
                positions_plt[1].append(float(node.pos.y))
                positions_plt[2].append(float(node.pos.z))
        if not_placed > 0:
            if not_placed < 2:
                max_x = float(max(positions_plt[0]))
                max_y = float(max(positions_plt[1]))
            else:
                max_x = float(max(positions_plt[0])) + 1
                max_y = float(max(positions_plt[1])) + 1
            min_x = float(min(positions_plt[0]))
            min_y = float(min(positions_plt[1]))
            for node in self.get_graph().get_all_v().values():
                if node.pos is None:
                    node.pos = GeoLocation(self.try_get_along(node, min_x, max_x, min_y, max_y))
                    positions_plt[0].append(node.pos.x)
                    positions_plt[1].append(node.pos.y)
                    positions_plt[2].append(node.pos.z)
        margin_x = (float(max(positions_plt[0])) - float(min(positions_plt[0]))) / 20
        margin_y = (float(max(positions_plt[1])) - float(min(positions_plt[1]))) / 20
        min_x = float(min(positions_plt[0])) - math.fabs(margin_x)
        min_y = float(min(positions_plt[1])) - math.fabs(margin_y)
        max_x = float(max(positions_plt[0])) + math.fabs(margin_x)
        max_y = float(max(positions_plt[1])) + math.fabs(margin_y)

        for node in self.get_graph().get_all_v().values():
            plt.plot(float(node.pos.x), float(node.pos.y), 'bo', marker='o', markersize=3, data="d")
            label = node.key
            plt.annotate(label,  # this is the text
                         (float(node.pos.x), float(node.pos.y)),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0.85, 0.95),
                         fontsize=8,
                         ha='center')
            for dest_node_id in self.get_graph().all_out_edges_of_node(node.key).keys():
                dest_node = self.get_node(dest_node_id)
                plt.arrow(float(node.pos.x), float(node.pos.y),
                          (float(dest_node.pos.x) - float(node.pos.x)), (float(dest_node.pos.y) - float(node.pos.y)),
                          length_includes_head=True, width=0.000003, head_width=0.0002)
        plt.axis([min_x, max_x, min_y, max_y])
        plt.xlabel("axis X")
        plt.ylabel("axis Y")
        plt.title("wow")
        plt.tick_params(axis='x', which='major', labelsize=6)
        plt.show()
        # raise NotImplementedError