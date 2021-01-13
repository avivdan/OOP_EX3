from unittest import TestCase
from DiGraph import DiGraph

class TestDiGraph(TestCase):


    def setUp(self) -> None:
        self.graph = DiGraph()

    def test_add_node(self):
        self.graph.add_node(2)
        self.assertEqual(self.graph.v_size(), 1)
        self.graph.add_node(3)
        self.graph.add_node(2) #Adding an existing node
        self.assertEqual(self.graph.v_size(), 2)
        self.assertFalse(self.graph.add_node(3))

    def test_add_edge(self):
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_node(4)
        self.assertEqual(self.graph.e_size(), 0)
        self.graph.add_edge(2,3,5.6)
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.add_edge(3,6,2.0)
        self.assertEqual(self.graph.e_size(), 2)
        self.assertFalse(self.graph.add_edge(3, 6, 2.0))

    def test_remove_node(self):
        self.graph.add_node(1)
        self.assertEqual(self.graph.v_size(), 1)
        self.graph.remove_node(1)
        self.assertEqual(self.graph.v_size(), 0)
        self.graph.add_node(3)
        self.graph.remove_node(4) #Removes a not existing node
        self.assertFalse(self.graph.remove_node(4))
        self.assertEqual(self.graph.v_size(), 1)

    def test_remove_edge(self):
        self.graph.add_node(0)
        self.graph.add_node(1)
        self.graph.add_edge(0, 1, 9)
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.remove_edge(0, 1)
        self.assertEqual(self.graph.e_size(), 0)
        self.graph.add_edge(1, 0, 3.5)
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.remove_edge(2, 3) #Removes a not existing edge
        self.assertFalse(self.graph.remove_edge(2, 3))
        self.assertEqual(self.graph.e_size(), 1)

    def test_get_node(self):
        self.graph.add_node(3)
        self.assertIsNotNone(self.graph.get_node(3))
        try:
            self.graph.get_node(2)
        except:
            print("OK")
        try:
            self.graph.get_node(0)
        except:
            print("OK")

    def test_v_size(self):
        self.graph.add_node(3)
        self.assertEqual(self.graph.v_size(), 1)
        self.graph.add_node(3) #Adding an existing node
        self.assertEqual(self.graph.v_size(), 1)
        self.graph.add_node(2)
        self.graph.remove_node(2)
        self.assertEqual(self.graph.v_size(), 1)
        self.graph.remove_node(7) #Removing a not existing node
        self.assertEqual(self.graph.v_size(), 1)

    def test_e_size(self):
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_edge(1,2,10)
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.add_edge(1, 3, 10)
        self.assertEqual(self.graph.e_size(), 2)
        self.graph.remove_edge(1,2)
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.remove_edge(3, 2) #Removing a not existing edge
        self.assertEqual(self.graph.e_size(), 1)
        self.graph.remove_node(1)
        self.assertEqual(self.graph.e_size(), 1)

    def test_get_all_v(self):
        self.graph.add_node(1)
        self.graph.add_node(2)
        test_data_1 = self.graph.get_node(2)
        self.assertIn(test_data_1, self.graph.get_all_v().values())
        test_data_2 = self.graph.get_node(1)
        self.graph.remove_node(1)
        self.assertNotIn(test_data_2, self.graph.get_all_v().values())

    def test_all_in_edges_of_node(self):
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_edge(1, 2, 8)
        self.graph.add_edge(1, 3, 5)
        self.graph.add_edge(3, 2, 2)
        self.assertEqual(2, len(self.graph.all_in_edges_of_node(2)))
        self.assertEqual(1, len(self.graph.all_in_edges_of_node(3)))
        self.graph.remove_edge(1, 2)
        self.assertEqual(1, len(self.graph.all_in_edges_of_node(2)))

    def test_all_out_edges_of_node(self):
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_edge(1, 2, 8)
        self.graph.add_edge(1, 3, 5)
        self.graph.add_edge(3, 2, 2)
        self.assertEqual(2, len(self.graph.all_out_edges_of_node(1)))
        self.graph.add_edge(2, 1, 8)
        self.assertEqual(2, len(self.graph.all_out_edges_of_node(1)))
        self.graph.remove_node(1)
        self.assertEqual(0, len(self.graph.all_out_edges_of_node(1)))

    def test_get_mc(self):
        self.assertEqual(0, self.graph.get_mc())
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.remove_node(1)
        self.assertEqual(3, self.graph.get_mc())
        self.graph.add_node(1)
        self.graph.add_edge(1, 2, 9)
        self.graph.remove_edge(1, 2)
        self.assertEqual(6, self.graph.get_mc())





    # def test_get_node(self):
    #     self.assert
