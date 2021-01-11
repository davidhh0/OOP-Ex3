
## EX3 - Object Oriented Programming 
### General info
This project is about directed and weighted graphs in Python. One of the main purposes of this project is comparing java implementation from the previous project to python implementation.

###  Structure of the project
#### directory (data):

 - includes many graphs as Json files in order to load/save them.
#### directory (src):
 - Interfaces:
	 GraphInterface.py, 
	 GraphAlgoInferface.py
 - Python classes: 
	 DiGraph.py, 
	 data.py, 
	 GraphAlgo.py, 
	 DFS.py, 
	 Ex3_main.py, 
	 comparison.py, 
	 PlottingTheComparison.py, 
	 TestDiGraph.py
	 
###  Algorithms and Testing in the project
data class is about node represented by a unique key value and each node has a position for plotting the graph.

DiGraph class implements the Graph interface using dictionary for saving each node in it as a key->node_data and same thing for edges , every edge is saved in a edges dictionary so that the source -> destination -> weight.

GraphAlgo class implements the Graph Algo interface and allows saving and loading a graph to a Json file, getting the shortest path from source to destination (as weight,list). Also, getting the connected components of the graph or the connected component of specified node using the DFS class in order to determine the components of the graph by using Depth-first-search.

The comparison class measures time elapsed over calculating the main algorithms of the project with my own implementation and NetworkX graph. 

Plotting the comparison class takes the data evaluated in the comparison class and the previous java implementation for the same algorithms and graph and plots it to a diagram (see wiki).

