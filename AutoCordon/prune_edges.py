import operator
from collections import deque

import networkx as nx
from networkx.algorithms.centrality import edge_current_flow_betweenness_centrality_subset as flow_betweenness


def get_sources_and_sinks(graph):
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    outside = [node[0] for node in graph.nodes("exterior_wider_closure") if node[1]]
    return sources, sinks, outside


def is_reachable(graph, sources, sinks):
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                return True
    return False


def get_max_betweenness_edge(graph, inner_graph, sources, sinks):
    betweeness = flow_betweenness(graph, sources, sinks)
    print(betweeness)
    inner_betweeness = {edge: betweeness[edge] for edge in inner_graph.edges()
                        if edge in betweeness}
    print(inner_betweeness)
    return max(inner_betweeness.items(), key=operator.itemgetter(1))[0]


def get_closure_edges(graph, inner_graph):
    removed_edges = []
    graph_deque = deque([graph.copy()])
    while len(graph_deque):
        g = graph_deque.pop()
        sources, sinks, outside = get_sources_and_sinks(g)
        if sources and sinks:
            max_edge = get_max_betweenness_edge(g, inner_graph, sources,
                                                outside)
            g.remove_edge(*max_edge)
            removed_edges.append(max_edge)
            if is_reachable(g, sources, sinks):
                for component in nx.connected_components(g):
                    graph_deque.append(g.subgraph(list(component)).copy())
    return removed_edges


def get_min_closures(graph):
    closure_edges = get_closure_edges(graph)
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    if len(closure_edges) >= len(sources):
        closure_edges = graph.edges(sources)
        print(closure_edges)
    return closure_edges
