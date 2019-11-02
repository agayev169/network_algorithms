class vertex:
    def __init__(self, label, visited=False):
        """
        Vertex object

        Args:
            label: str,
                Label of the vertex

            visited: bool, default: False
                Represents whether vertex is visited or not
        """
        self.__label   = label
        self.__visited = visited

    
    def visit(self):
        self.__visited = True


    def is_visited(self):
        return self.__visited

    
    def get_label(self):
        return self.__label


    def __str__(self):
        """
        Retruns the vertex represented as a string
        """
        return f"{self.__label}{'*' if self.__visited else ''}"


    def __repr__(self):
        """
        Retruns the vertex represented as a string
        """
        return f"{self.__label}{'*' if self.__visited else ''}"


class edge:
    __edge_count = 0
    def __init__(self, endpoints, weight=0, label=None):
        """
        Edge object

        Args:
            endpoints: list of 2 vertecies
                List of 2 vertices that are endpoints of the edge

            weight: int or float, default: 0
                Weight/cost of an edge

            label: str, default: None
                Label of the edge, by default is edge_x, where x is the number of edge
        """
        if len(endpoints) != 2 or not isinstance(endpoints[0], vertex) or not isinstance(endpoints[1], vertex):
            raise AssertionError("endpoints must contain 2 instances of vertex class")

        if not isinstance(weight, int) and not isinstance(weight, float):
            raise AssertionError("weight must be either int or float")

        self.__endpoints = endpoints
        self.__weight    = weight
        self.__label     = label
        if label is None:
            self.__label = f"edge_{edge.__edge_count}"
        edge.__edge_count += 1

    
    def get_endpoints(self):
        return self.__endpoints

    
    def get_weight(self):
        return self.__weight


    def __repr__(self):
        return f"{self.__label}: {self.__endpoints[0]} -> {self.__endpoints[1]} ({self.__weight})"


    def __str__(self):
        return f"{self.__label}: {self.__endpoints[0]} -> {self.__endpoints[1]} ({self.__weight})"

    
    def __eq__(self, other):
        return (isinstance(other, edge) and                                                                      \
               (self.__endpoints[0] == other.__endpoints[0] and self.__endpoints[1] == other.__endpoints[1]) and \
                self.__weight == other.__weight)


class graph:
    def __init__(self):
        """
        Graph object
        """
        self.__vertices = dict()
        self.__edges = []

    
    def get_vertex(self, label):
        """
        Get vertex by label

        Args:
            label: str
                Label of the vertex to return

        Returns:
            vertex: vertex
                Vertex with the given label. If there is no such vertex returns None
        """
        if not isinstance(label, str):
            raise AssertionError("Label must be str")

        for v in self.__vertices.keys():
            if v.get_label() == label:
                return v

        return None


    def get_edge(self, v1, v2):
        """
        Get edge connecting two verticies

        Args:
            v1, v2: vertex or str
                Vertecies to get an edge between
        
        Returns
            edge: edge
                An edge connecting verticies. None is returned if no edge found
        """

        if isinstance(v1, str):
            v1 = self.get_vertex(v1)
        
        if isinstance(v2, str):
            v2 = self.get_vertex(v2)

        if v1 not in self.__vertices.keys() or v2 not in self.__vertices.keys():
            raise AssertionError("v1 and v2 must be in the graph")

        for e in self.__edges:
            endpoints = e.get_endpoints()
            if endpoints[0] == v1 and endpoints[1] == v2:
                return e

        return None


    def add_vertex(self, label):
        """
        Adds a new vertex to the graph

        Args:
            label: str
                Label of the vertex to be added

        Returns:
            A vertex if it is not already in a graph, otherwise None
        """

        if not isinstance(label, str):
            raise AssertionError("Label must be str")

        v = None

        if label not in list(vert.get_label() for vert in self.__vertices.keys()):
            v = vertex(label)
            self.__vertices[v] = []

        return self.get_vertex(label) if v is None else v

    
    def add_edge(self, v1, v2, weight=0, label=None):
        """
        Adds an edge between 2 vertexes

        Args:
            v1, v2: vertex or str
                vertices to add an edge between
            
            weight: int or float, default: 0
                Weight of the edge
        """
        if (v1 not in self.__vertices.keys() and v1 not in [v.get_label() for v in self.__vertices.keys()]) or \
           (v2 not in self.__vertices.keys() and v2 not in [v.get_label() for v in self.__vertices.keys()]):
            raise AssertionError("Cannot connect an edge between 2 vertices that are not in the graph")

        if isinstance(v1, str):
            v1 = self.get_vertex(v1)
        
        if isinstance(v2, str):
            v2 = self.get_vertex(v2)

        if self.__edges.count(edge((v1, v2), weight, label)) == 0:
            self.__vertices[v1].append(v2)
            self.__edges.append(edge((v1, v2), weight, label))
            return self.__edges[-1]
        
        return None

    
    def degree(self, v):
        """
        Degree of the vertex

        Args:
            v: vertex
                Vertex to return the degree of

        Return:
            degree: int
                Degree of the vertex if it is in the graph, otherwise -1
        """

        if v not in self.__vertices[v]:
            return -1
        
        return len(self.__vertices[v])

    
    def is_empty(self):
        """
        Returns whether a graph is empty (no edges) or not

        Return:
            empty: bool
                Whether a graph is empty or not
        """
        res = 0
        for v in self.__vertices.keys():
            res += len(self.__vertices[v])
        
        for v1 in self.__vertices.keys():
            for v2 in self.__vertices[v1]:
                if v1 == v2:
                    res += 1
                    break

        return res == 0

    
    def is_singleton(self):
        """
        Returns whether a graph is singleton (1 vertex and no edges) or not

        Return:
            empty: bool
                Whether a graph is singleton or not
        """
        return len(self.__vertices.keys()) == 1 and self.is_empty()

    
    def is_null(self):
        """
        Returns whether a graph is null (no vertices) or not

        Return:
            empty: bool
                Whether a graph is null or not
        """
        return len(self.__vertices.keys()) == 0

    
    def is_trivial(self):
        """
        Return whether a graph is trivial (1 vertex and no edges) or not

        Return:
            empty: bool
                Whether a graph is trivial or not
        """
        return self.is_singleton()


    def has_loop(self):
        """
        Returns whether a graph has a loop or not

        Return:
            empty: bool
                Whether a graph has a loop or not
        """
        for v1 in self.__vertices.keys():
            for v2 in self.__vertices[v1]:
                if v1 == v2:
                    return True
        
        return False


    def has_parallel(self, v1=None, v2=None):
        """
        Returns whether a graph (default) or two vertices have parallel edges or not

        Args:
            v1, v2: vertex, default None
                Vertices to check the parallelness

        Return:
            empty: bool
                Whether a graph or two vertices have parallel edges or not
        """
        if not v1 is None and not v2 is None:
            if v1 not in self.__vertices.keys() or v2 not in self.__vertices.keys():
                raise AssertionError("Edges must be in the graph") 
            
            if self.__vertices[v1].count(v2) > 1:
                return True
            
            return False
        else:
            for v1 in self.__vertices.keys():
                for v2 in self.__vertices[v1]:
                    if self.has_parallel(v1, v2):
                        return True
            return False

    
    def is_simple(self):
        """
        Returns whether a graph is simple (no loops and multiple edges) or not

        Return:
            empty: bool
                Whether a graph is simple or not
        """
        return not self.has_loop() and not self.has_parallel()

    
    def is_complete(self):
        """
        Returns whether a graph is complete (all vertexes are connected with one another) or not

        Return:
            empty: bool
                Whether a graph is complete or not
        """
        if not self.is_simple():
            return False

        lenv = len(self.__vertices.keys())

        for v in self.__vertices.keys():
            deg = len(self.__vertices[v])
            if deg != lenv - 1:
                return False
            
        return True

    
    def are_adjacent_vertices(self, v1, v2):
        """
        Returns whether v1 and v2 are adjacent or not

        Args:
            v1, v2: vertex
                Vertices to cjeck the adjacency

        Return:
            empty: bool
                Whether v1 and v2 are adjacent or not
        """
        if v1 not in self.__vertices.keys() or v2 not in self.__vertices.keys():
            raise AssertionError("Edges must be in the graph") 

        return v2 in self.__vertices[v1]


    def adjacent_vertices(self, v):
        """
        Returns a list of adjacent vertices of v

        Args:
            v: vertex
                Vertex to return adjacent vertices of

        Return:
            empty: bool
                Whether a graph is complete or not
        """
        return self.__vertices[v] if v in self.__vertices.keys() else []


    def isolated_vertices(self):
        """
        Returns a list of isolated vertices

        Return:
            empty: bool
                Whether a graph is complete or not
        """
        return [v for v in self.__vertices.keys() if len(self.__vertices[v]) == 0]

    
    def __str__(self):
        """
        Retruns the graph represented as a string
        """

        # res = ""
        # for v in self.__vertices.keys():
        #     res += v.__repr__()
        #     res += " ->"
        #     for adj in self.__vertices[v]:
        #         res += f" {adj} ->"
        #     res += " /\n"
        # return res


        res = ""
        
        for i, e in enumerate(self.__edges):
            res += e.__str__()
            if i != len(self.__edges) - 1:
                res += "\n"

        return res

    
    def __repr__(self):
        """
        Retruns the graph represented as a string
        """

        # res = ""
        # for v in self.__vertices.keys():
        #     res += v.__repr__()
        #     res += " ->"
        #     for adj in self.__vertices[v]:
        #         res += f" {adj} ->"
        #     res += " /\n"
        # return res

        res = ""
        
        for i, e in enumerate(self.__edges):
            res += e.__str__()
            if i != len(self.__edges) - 1:
                res += "\n"

        return res


    
if __name__ == "__main__":
    gr = graph()
    a = gr.add_vertex("a")
    b = gr.add_vertex("b")
    c = gr.add_vertex("c")
    gr.add_vertex("a")

    e1 = gr.add_edge(a, b)
    e2 = gr.add_edge("b", a)
    e3 = gr.add_edge("a", "a")
    
    print(gr.is_empty())
    print(gr.has_loop())
    print(gr.is_simple())
    print(gr.is_singleton())
    print(gr.is_null())
    print(gr.is_complete())
    print(gr.are_adjacent_vertices(a, b))
    print(gr.are_adjacent_vertices(a, c))
    print(gr.are_adjacent_vertices(b, c))
    print(gr)
    print(gr.adjacent_vertices(b))
    print(gr.isolated_vertices())

    print(e1)
    print(e2)
    print(e3)
    print(e1 == e2)
    print(e1 == e3)