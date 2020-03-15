"""
    requires igraph module to view the connected components
"""

from igraph import *

with open("../scraped_data/web_links/web_links.txt") as f:
    seen_vertex = set()
    edges = dict()
    g = Graph(directed=True)
    for line in f:
        source_vertex,destination_vertexes = line.split("\t")
        destination_vertexes = destination_vertexes.split(",")
        seen_vertex.add(source_vertex)
        for each in destination_vertexes:
            seen_vertex.add(each)
        edges[source_vertex] = destination_vertexes
    for each_vertex in list(seen_vertex):
        g.add_vertex(each_vertex)
    for each_source in edges.keys():
        for each_des in edges[each_source]:
            try:
                g.add_edge(each_source,each_des)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise 
    layout = g.layout("kk")
    g.vs["label"] = g.vs["name"]
    plot(g, layout = layout, vertex_size=20)


