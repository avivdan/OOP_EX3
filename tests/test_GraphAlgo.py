import unittest
from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from GraphAlgoInterface import GraphAlgoInterface
from random import seed, randrange, random


class MyTestCase(TestCase):

    def create_graph(self, nodes: int, edges: int):
        seed(1)
        self.graph = DiGraph()
        i = 0
        while i < nodes:
            self.graph.add_node(i)
            i += 1
        while self.graph.e_size() < edges:
            rnd = randrange(0, nodes)
            rnd2 = randrange(0, nodes)
            rnd3 = random()
            self.graph.add_edge(rnd, rnd2, rnd3 * 100)
        return self.graph

    def test_get_graph(self):
        self.graph_algo = GraphAlgo()
        self.graph = self.create_graph(0, 0)
        self.graph.add_node(1)
        self.graph_algo.get_graph().add_node(1)
        self.assertEqual(self.graph_algo.get_graph().v_size(), 1)

    def test_save_load_json(self):
        graph = self.create_graph(5, 5)
        graph_algo1 = GraphAlgo(graph)
        graph_algo1.save_to_json("test.txt")
        graph_algo2 = GraphAlgo()
        graph_algo2.load_from_json("test.txt")
        self.assertEqual(graph_algo1.shortest_path(1, 3), graph_algo2.shortest_path(1, 3))

    def test_shortest_path(self):
        graph = DiGraph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_edge(0, 1, 9)
        graph.add_edge(1, 2, 4)
        graph.add_edge(2, 3, 11)
        graph.add_edge(3, 4, 2)
        graph.add_edge(1, 4, 10)
        graph_algo1 = GraphAlgo(graph)
        answer = (10, [1, 4])
        self.assertEqual(graph_algo1.shortest_path(1, 4), answer)
        answer = (13, [0, 1, 2])
        self.assertEqual(graph_algo1.shortest_path(0, 2), answer)
        answer = (0, [3])
        self.assertEqual(graph_algo1.shortest_path(3, 3), answer) #Shortest path from a node to itself
        self.assertEqual(graph_algo1.shortest_path(3, 6), None) #The dst node is not exist

    def test_connected_component(self):
        graph = DiGraph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_edge(0, 1, 9)
        graph.add_edge(1, 0, 4)
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_component(1), [1, 0])
        graph.add_edge(1, 3, 6) #node 1 is weakly connected with node 3
        self.assertEqual(graph_algo.connected_component(1), [1, 0])
        graph.add_edge(3, 1, 9.3) #node 1 is strongly connected with node 3
        self.assertEqual(graph_algo.connected_component(1), [1, 0, 3])
        self.assertEqual(graph_algo.connected_component(10), []) #This node does not exist
        self.assertEqual(graph_algo.connected_component(4), [4]) #This node is not strongly connected with another one

    def test_connected_components(self):
        graph = DiGraph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(0, 1, 9)
        graph.add_edge(1, 0, 4)
        graph.add_edge(1, 2, 9)
        graph.add_edge(2, 1, 4)
        graph.add_edge(2, 3, 9)
        graph.add_edge(3, 2, 4)
        graph.add_edge(0, 3, 9)
        graph.add_edge(3, 0, 4)
        graph.add_edge(0, 2, 9)
        answer = [[0, 1, 2, 3]]
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_components(), answer)
        graph.add_node(4) #Adding a node which is not connected to any other node
        graph.add_edge(4, 1, 7) #node 4 is weakly connected to 1
        answer = [[0, 1, 2, 3], [4]]
        self.assertEqual(graph_algo.connected_components(), answer)
        graph.add_node(5) #node 5 is not connected to any other node
        answer = [[0, 1, 2, 3], [4], [5]]
        self.assertEqual(graph_algo.connected_components(), answer)
        graph.add_edge(4, 5, 10)
        graph.add_edge(5, 4, 2.5)
        answer = [[0, 1, 2, 3], [4, 5]]
        self.assertEqual(graph_algo.connected_components(), answer)
