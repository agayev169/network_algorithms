import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

from graph import graph, vertex, edge

def dfs(gr, orig, dest, edges=[]):
    """
    DFS algorithm. Finds path between origin and destionation
    
    Args:
        gr: graph
            Graph we are working with
        
        orig: vertex or str
            Origin vertex

        dest: vertex or str
            Destination vertex
    
    Result:
        edges: edge
            Edges passed to go from origin to destination
    """

    if not isinstance(gr, graph):
        raise AssertionError("gr must be graph")

    if isinstance(orig, str):
        orig = gr.get_vertex(orig)
    
    if isinstance(dest, str):
        dest = gr.get_vertex(dest)

    if not isinstance(orig, vertex) or not isinstance(dest, vertex):
        raise AssertionError("orig and dest must be vertecies and must be presented in graph")

    orig.visit()

    if dest in gr.adjacent_vertices(orig):
        dest.visit()
        edges.append(gr.get_edge(orig, dest))
    else:
        for v in gr.adjacent_vertices(orig):
            if not v.is_visited():
                dfs(gr, v, dest)
                if dest.is_visited():
                    edges.append(gr.get_edge(orig, v))
                    return edges
                # edges.append(dfs(gr, v, dest)[-1])

    return edges

filename = "cities_in_az.csv"
# filename = "airports.csv"
gr = graph()

data = pd.read_csv(filename)

if filename == "cities_in_az.csv":
    for i in range(len(data)):
        d = data.loc[i].values

        v1 = gr.add_vertex(d[0])
        v2 = gr.add_vertex(d[1])

        gr.add_edge(v1, v2, d[2], label=f"{d[0]}_{d[1]}")

    begin = time.time()
    res = dfs(gr, "Baku", "Goychay")[::-1]
    end = time.time()
    print(f"Time spent: {end - begin}s")

    for e in res:
        print(e)

    cost = sum([e.get_weight() for e in res])
    print(f"Total cost of path: {cost}")

    g = nx.from_pandas_edgelist(data, source="Origin", target="Destiny", edge_attr=True)
    plt.figure()
    nx.draw_networkx(g, with_labels=True)
    plt.show()

elif filename == "airports.csv":
    data = pd.read_csv(filename)

    for i in range(len(data)):
        d = data.loc[i].values

        v1 = gr.add_vertex(d[9])
        v2 = gr.add_vertex(d[10])

        gr.add_edge(v1, v2, int(d[11]), label=f"{d[9]}_{d[10]}")

    begin = time.time()
    res = dfs(gr, "IAD", "CRP")[::-1]
    end = time.time()
    print(f"Time spent: {end - begin}s")

    for e in res:
        print(e)

    cost = sum([e.get_weight() for e in res])
    print(f"Total cost of the path: {cost}")

    g = nx.from_pandas_edgelist(data, source="Origin", target="Dest", edge_attr="Distance")
    plt.figure()
    nx.draw_networkx(g, with_labels=True)
    plt.show()