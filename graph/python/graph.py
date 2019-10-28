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


class graph:
    def __init__(self):
        """
        Graph object
        """
        self.__vertices = dict()


    def add_vertex(self, label):
        """
        Adds a new vertex to the graph

        Args:
            label: str, int, object
                Label of the vertex to be added

        Returns:
            A vertex if it is not already in a graph, otherwise None
        """

        v = None

        if label not in list(vert.get_label() for vert in self.__vertices.keys()):
            v = vertex(label)
            self.__vertices[v] = []

        return v

    
    def add_edge(self, v1, v2):
        """
        Adds an edge between 2 vertexes

        Args:
            v1, v2: vertex
                vertices to add an edge between
        """
        if v1 not in self.__vertices.keys() or v2 not in self.__vertices.keys():
            raise AssertionError("Cannot connect an edge between 2 vertices that are not in the graph") 

        # TODO: add possibility to add an edge by calling add_edge function with vertex names

        self.__vertices[v1].append(v2)
        self.__vertices[v2].append(v1)

    
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

        res = ""
        for v in self.__vertices.keys():
            res += v.__repr__()
            res += " ->"
            for adj in self.__vertices[v]:
                res += f" {adj} ->"
            res += " /\n"
        return res

    
    def __repr__(self):
        """
        Retruns the graph represented as a string
        """

        res = ""
        for v in self.__vertices.keys():
            res += v.__repr__()
            res += " ->"
            for adj in self.__vertices[v]:
                res += f" {adj} ->"
            res += " /\n"
        return res


    
if __name__ == "__main__":
    gr = graph()
    a = gr.add_vertex("a")
    b = gr.add_vertex("b")
    c = gr.add_vertex("c")
    gr.add_vertex("a")

    gr.add_edge(a, b)
    
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