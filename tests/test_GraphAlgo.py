import unittest
from unittest import TestCase
from GraphAlgoInterface import GraphAlgoInterface
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph
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
        print(graph.v_size())
        graph_algo1 = GraphAlgo(graph)
        graph_algo1.save_to_json("test.txt")
        print(graph_algo1.get_graph().v_size())
        graph_algo2 = GraphAlgo()
        graph_algo2.load_from_json("test.txt")
        print(graph_algo2.get_graph().v_size())
        self.assertEqual(graph_algo1.get_graph(), graph_algo2.get_graph())

    def test_shortest_path(self):
        graph = self.create_graph(5, 5)
        graph_algo1 = GraphAlgo(graph)
        answer = (75.41872169814071, [1, 0, 3])
        self.assertEqual(graph_algo1.shortest_path(1, 3), answer)


if __name__ == '__main__':
    unittest.main()
    # pass
