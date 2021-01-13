# OOP-Ex3-Python

## About the project
>This project is an implementation of a weighted directed graph.
A graph is represented in adjacency list and each one contains a list of nodes,
and a list of weighted edges.
This last assignment is about the implement the data structures in the oopEx2 assignment and check 
for the differences between them by time, also, to show us our data structure effectiveness against
known library.


The A0 graph from assignment 2:</br>
![graph A0](https://github.com/avivdan/OOP_EX3/blob/master/pics/A0.png?raw=true)

---

<h3>would be represented:</h3>

```
      |V|=11 , |E|=22 , MC=33
from #0:
	 To: 1 | 10 | 

from #1:
	 To: 0 | 2 | 

from #2:
	 To: 1 | 3 | 

from #3:
	 To: 2 | 4 | 

from #4:
	 To: 3 | 5 | 

from #5:
	 To: 4 | 6 | 

from #6:
	 To: 5 | 7 | 

from #7:
	 To: 6 | 8 | 

from #8:
	 To: 7 | 9 | 

from #9:
	 To: 8 | 10 | 

from #10:
	 To: 0 | 9 | 

```

---

<h2>comparison</h2>
<h3>java vs python vs networkx</h3>


>networkx won...</br>
because networkx got run time of zero on every graph we didn't place him on a bar chart,</br> 
but we surly measure and load all the graphs for comparison.



>**Shortest Path**

![Shortest Path](https://github.com/avivdan/OOP_EX3/blob/master/pics/shortestPath.png.png?raw=true)

>**Strongly Connected Components**

![SCC](https://github.com/avivdan/OOP_EX3/blob/master/pics/SCCs.png?raw=true)

>**Strongly Connected Component**

![SCC](https://github.com/avivdan/OOP_EX3/blob/master/pics/SCC_node.png?raw=true)

---

## DiGraph class
| Method  | Description  | 
| :------ |:-------------| 
|add_node(node_id, position)| adds a node to the graph. | 
|remove_node(node_id)| removes a vertex with all its edges from the graph by its key|
|get_node()|returns the vertex associated with a given key|
|addEdge(id1, id2, weight)|adds an edge with a weight between two existing vertices. The edge is a direction from source to destination when added in a directed graph. If the edge already exists or one of the nodes dose not exists the functions will do nothing|
|removeEdge(id1, id2)|removes an edge between two existing vertices|
|all_in_edges_of_node(node_id)|return a dictionary of all the nodes connected to (into) dst , each node is represented using a pair (key, weight)|
|all_out_edges_of_node(node_id)|return a dictionary of all the nodes connected from src , each node is represented using a pair (key, weight)|
|v_size()|gets the number of vertices in the graph.|
|e_size()|gets the number of edges in the graph.|
|get_mc()|Returns the current version of this graph, on every change in the graph state - the MC should be increased|

## GraphAlgo class summary
| Method  | Description  | Complexity |
| :------ |:-------------| :---------:|
|[load_from_json(file_name)](https://www.json.org/json-en.html)|Loads a graph from a json file.|O(V+E)|
|[save_to_json(file_name)](https://www.json.org/json-en.html)|Saves the graph in JSON format to a file|O(V+E)|
|[shortest_path(src, dst)](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)|Returns the shortest path from node src to node dst using Dijkstra's Algorithm|O((V+E)*LOG(V))|
|[connected_component(key)](https://en.wikipedia.org/wiki/Strongly_connected_component)|Finds the Strongly Connected Component(SCC) that node id1 is a part of.|O(V+E)|
|[connected_components()](https://www.geeksforgeeks.org/strongly-connected-components/)|Finds all the Strongly Connected Component(SCC) in the graph.|O(V*(V+E))|
|[plot_graph()](https://matplotlib.org/)|Plots the graph. If the nodes have a position, the nodes will be placed there. Otherwise, they go to getAlong|O(V+E)|
|try_get_along(node, min_x, max_x, min_y, max_y) |The function is setting elegantly the unpositioned nodes and put them between neighbors or inbox. At the end will return position|O(1)|
|[bfs_in(node_id)](https://en.wikipedia.org/wiki/Breadth-first_search) |checks which nodes node_id could go to|O(V+E)|
|[bfs_in(node_id)](https://en.wikipedia.org/wiki/Breadth-first_search) |checks which nodes could get into node_id|O(V+E)|