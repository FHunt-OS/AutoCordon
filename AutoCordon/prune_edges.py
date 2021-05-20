import operator
from collections import deque

import networkx as nx
from networkx.algorithms.centrality import edge_current_flow_betweenness_centrality_subset as flow_betweenness


def get_sources_and_sinks(graph):
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    return sources, sinks


def is_reachable(graph, sources, sinks):
    reachable = []
    for source in sources:
        reachable.extend(nx.dfs_tree(graph, source).nodes())
    return set(sinks).intersection(set(reachable))


def get_max_betweenness_edge(graph, sources, sinks):
    betweeness = flow_betweenness(graph, sources, sinks)
    return max(betweeness.items(), key=operator.itemgetter(1))[0]


def get_disconnected_edges(graph):
    disconnected = []
    graph_deque = deque([graph.copy()])
    while len(graph_deque):
        g = graph_deque.pop()
        sources, sinks = get_sources_and_sinks(g)
        if sources and sinks:
            max_edge = get_max_betweenness_edge(g, sources, sinks)
            g.remove_edge(*max_edge)
            if is_reachable(g, sources, sinks):
                for component in nx.connected_components(g):
                    graph_deque.append(g.subgraph(list(component)).copy())
            else:
                disconnected.extend(g.edges)
        else:
            disconnected.extend(g.edges)
    return disconnected


def get_closure_edges(graph):
    removed_edges = []
    graph_deque = deque([graph.copy()])
    while len(graph_deque):
        g = graph_deque.pop()
        sources, sinks = get_sources_and_sinks(g)
        if sources and sinks:
            max_edge = get_max_betweenness_edge(g, sources, sinks)
            g.remove_edge(*max_edge)
            removed_edges.append(max_edge)
            if is_reachable(g, sources, sinks):
                for component in nx.connected_components(g):
                    graph_deque.append(g.subgraph(list(component)).copy())
    return removed_edges
