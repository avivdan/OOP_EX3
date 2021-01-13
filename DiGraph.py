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
        if node_id is not None: #If exist
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
        if id1 in self.graph_edges_in.keys():  #If exist
            for x in self.graph_edges_in[id1].keys(): #For node which is connected to id1
                dic_return[x] = self.graph_edges_in[id1][x].weight
            return dic_return
        else:
            return {}

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        dic_return = {}
        if id1 in self.graph_edges_out.keys(): #If exist
            for x in self.graph_edges_out[id1].keys(): #For node which id1 is connected to
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
                return False #If edge already exist return false
            else:
                self.graph_edges_out[edge.src][edge.dest] = edge #Add edge to out_edges
        else:
            self.graph_edges_out[edge.src] = {edge.dest: edge} #Add edge to out_edges
        if edge.dest in self.graph_edges_in.keys():
            self.graph_edges_in[edge.dest][edge.src] = edge #Add edge to in_edges
        else:
            self.graph_edges_in[edge.dest] = {edge.src: edge} #Add edge to in_edges
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
        if node_id in self.graph_v.keys(): #If exist
            return False
        if node_id is not None:
            if pos is not None: #If has position
                self.graph_v[node_id] = NodeData(key=node_id, pos=pos) #Add node with the existing key and position
                self.mc_count += 1
                return True
            self.graph_v[node_id] = NodeData(key=node_id) #Add node with the existing key
            self.mc_count += 1
            return True
        if pos is not None:
            self.graph_v[node_id] = NodeData(pos=pos) #Add node with the existing position
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
        if node_id in self.graph_v.keys(): #If exist
            self.graph_v.pop(node_id) #Removes the node from graph_v
            self.mc_count += 1
            if node_id in self.graph_edges_out.keys():
                dict_in = self.graph_edges_out.pop(node_id)  # dict_in = dict, removes all the removed node out_edges
                for x in dict_in.keys():
                    self.graph_edges_in[x].pop(node_id) #Removes all the removed node in_edges
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
                self.graph_edges_out.get(node_id1).pop(node_id2) #Removes from "one side"
                self.graph_edges_in.get(node_id2).pop(node_id1) #Removes from "the other side"
                self.edge_size -= 1 #Because an edge has been removed
                self.mc_count += 1
                return True
        return False #If not exist
        # raise NotImplementedError
