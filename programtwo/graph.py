#!/usr/bin/python
#Brian Fox

from collections import deque
import math

class Graph :
    """Graph represented with adjacency lists."""

    __slots__ = ['_adj']

    def __init__(self, v=10, edges=[]) :
        """Initializes a graph with a specified number of vertices.

        Keyword arguments:
        v - number of vertices
        edges - any iterable of ordered pairs indicating the edges 
        """

        self._adj = [ _AdjacencyList() for i in range(v) ]
        for a, b in edges :
            self.add_edge(a, b)



    def add_edge(self, a, b) :
        """Adds an edge to the graph.

        Keyword arguments:
        a - first end point
        b - second end point
        """

        self._adj[a].add(b)
        self._adj[b].add(a)
    

    def num_vertices(self) :
        """Gets number of vertices of graph."""
        
        return len(self._adj)


    def degree(self, vertex) :
        """Gets degree of specified vertex.

        Keyword arguments:
        vertex - integer id of vertex
        """
        
        return self._adj[vertex]._size

    def bfs(self, s) :
        """Performs a BFS of the graph from a specified starting vertex.
        Returns a list of objects, one per vertex, containing the vertex's distance
        from s in attribute d, and vertex id of its predecessor in attribute pred.

        Keyword arguments:
        s - the integer id of the starting vertex.
        """
        
        class VertexData :
            __slots__ = [ 'd', 'pred' ]

            def __init__(self) :
                self.d = math.inf
                self.pred = None

        vertices = [VertexData() for i in range(len(self._adj))]
        vertices[s].d = 0
        q = deque([s])
        while len(q) > 0 :
            u = q.popleft()
            for v in self._adj[u] :
                if vertices[v].d == math.inf :
                    vertices[v].d = vertices[u].d + 1
                    vertices[v].pred = u
                    q.append(v)
        return vertices

    def dfs(self) :
        """Performs a DFS of the graph.  Returns a list of objects, one per vertex, containing
        the vertex's discovery time (d), finish time (f), and predecessor in the depth first forest
        produced by the search (pred).
        """

        class VertexData :
            __slots__ = [ 'd', 'f', 'pred' ]

            def __init__(self) :
                self.d = 0
                self.pred = None

        vertices = [VertexData() for i in range(len(self._adj))]
        time = 0

        def dfs_visit(u) :
            nonlocal time
            nonlocal vertices

            time = time + 1
            vertices[u].d = time
            for v in self._adj[u] :
                if vertices[v].d == 0 :
                    vertices[v].pred = u
                    dfs_visit(v)
            time = time + 1
            vertices[u].f = time

        for u in range(len(vertices)) :
            if vertices[u].d == 0 :
                dfs_visit(u)
        return vertices

        

        
    

    def print_graph(self) :
        """Prints the graph."""
        
        for v, vList in enumerate(self._adj) :
            print(v, end=" -> ")
            for u in vList :
                print(u, end="\t")
            print()
            




class Digraph(Graph) :

    def add_edge(self, a, b) :
        self._adj[a].add(b)

    def topological_sort(self) :
        """Topological Sort of the directed graph (Section 22.4 from textbook).
        Returns the topological sort as a list of vertex indices.
        """
        
        # Remove this pass statement after you implement this method.  Simply here temporarily.

        #       Homework Hints/Suggestions/Etc:
        #           1) Textbook indicates to use a Linked List.  Python doesn't have
        #               one in the standard library.  Instead, use a deque (don't simply use
        #               a python list since adding at the front is O(N) for a python list,
        #               while it is O(1) for a deque).
        #           2) From the pseudocode, you will be tempted to (a) call DFS, and then (b) sort
        #               vertices by the finishing times.  However, don't do that since the sort will
        #               cost O(V lg V) unnecessarily.
        #           3) So, how do you do it without sorting?
        #               Here is one of the ways to do it. Reimplement the DFS directly within topological_sort,
        #               but initialize an empty list for the result toward the beginning of the method,
        #               and then where the finishing time is set, add the vertex index to the front of that list.
        #               And then make sure you return your list of vertices at the end.
        
        sorted_list = LinkedList()
        visited = set()
        
        def top_visit(adj,v):
            nonlocal sorted_list
            nonlocal visited
            visited.add(adj)
            for e in adj:
                if not self._adj[e] in visited:
                    top_visit(self._adj[e],e)

            sorted_list.insert(v)

        for v, adj in enumerate(self._adj):
            if not adj in visited:
                top_visit(adj,v)

        return sorted_list

    def transpose(self) :
        """Computes the transpose of a directed graph. (See textbook page 616 for description of transpose).
        Does not alter the self object.  Returns a new Digraph that is the transpose of self."""
        
        pass # Remove this pass statement after you implement this method.  Simply here temporarily.

        #    Homework Hint: Make sure you don't change the graph.  Start by constructing a new Digraph
        #                   object with the same number of vertices.
        #                   If you want to construct a Digraph with v vertices, you'd do something like:
        #                   t = Digraph(v)
        #                   Once you have that, you'd then iterate over the edges of the original graph,
        #                   and for each add an edge to t but with vertices in opposite order.
        #     Another hint:  See the print_graph method above for an example of how to iterate over the edges
        #                   of a graph.  Ignore the print statements in that example (you don't want to print anything here).
        #                   That example iterates over the edges (v,u).  i.e., if you're in the body of the nested loop,
        #                   then (v,u) is an edge of the graph you are iterating over.




    def strongly_connected_components(self) :
        """Computes the strongly connected components of a digraph.
        Returns a list of lists, containing one list for each strongly connected component,
        which is simply a list of the vertices in that component."""
        
        pass # Remove this pass statement after you implement this method.  Simply here temporarily.

        #       Homework Hints/Suggestions/Etc: See algorithm on page 617.
        #           1) Take a look at algorithm steps 1 and 2 before you do anything.  Notice that Step 1 computes finishing times with DFS,
        #               and step 3 uses vertices in order of decreasing finishing times.  As in the topological sort, don't actually sort
        #               by finishing time (to avoid O(V lg v) step).  However, this is easier than in the topological sort as you already
        #               have a method that will get you what you need.  For step 1 of algorithm you can simply call your topological sort.
        #               That will give you the vertices in decreasing order by finishing time, which is really the intention of algorithm line 1.
        #           2) Line 2 is just the transpose and you implemented a method to compute this above.
        #           3) The DFS in line 3 can be done in a couple ways.  The simplest is NOT to call DFS, but instead to reimplement it here.
        #               In the outer loop, use the vertex ordering obtained from algorithm line 1 (to implement line 3).
        #               And to do line 4, you'll need to have your code generate the list of lists for the return value.
   



class _AdjacencyList :

    __slots__ = [ '_first', '_last', '_size']

    def __init__(self) :
        self._first = self._last = None
        self._size = 0

    def add(self, node) :
        if self._first == None :
            self._first = self._last = _AdjListNode(node)
        else :
            self._last._next = _AdjListNode(node)
            self._last = self._last._next
        self._size = self._size + 1

    def __iter__(self):
        return _AdjListIter(self)

    

class _AdjListNode :

    __slots__ = [ '_next', '_data' ]

    def __init__(self, data) :
        self._next = None
        self._data = data

        

class _AdjListIter :

    __slots__ = [ '_next', '_num_calls' ]

    def __init__(self, adj_list) :
        self._next = adj_list._first
        self._num_calls = adj_list._size

    def __iter__(self) :
        return self

    def __next__(self) :
        if self._num_calls == 0 :
            raise StopIteration
        self._num_calls = self._num_calls - 1
        data = self._next._data
        self._next = self._next._next
        return data


class LinkedList(_AdjacencyList):
    """extending  _AdjacencyList for use as a general linked list"""
    def insert(self,node):
        if self._first == None :
            self._first = self._last = _AdjListNode(node)
        else :
            new = _AdjListNode(node)
            new._next = self._first
            self._first = new      
        self._size = self._size + 1
            

if __name__ == "__main__" :
    # here is where you will implement any code necessary to confirm that your
    # topological sort, transpose, and strongly connected components methods work correctly.
    # Code in this if block will only run if you run this module, and not if you load this module with
    # an import for use by another module.
    
    g = Digraph(5,[(0,1),(1,2),(2,3),(3,4),(4,0)])
    
    g.print_graph()

    for v in g.topological_sort():
        print(v,end="  ")
    print()

    g = Digraph(6,[(0,1),(1,2),(2,3),(3,0),(4,5),(5,4)])
    
    g.print_graph()

    for v in g.topological_sort():
        print(v,end="  ")
    print()
