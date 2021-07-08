import operator
from collections import deque, defaultdict
from itertools import chain

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


def get_routes(graph, sources, sinks):
    routes = []
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                routes.append(nx.shortest_path(graph, source, sink))
    return routes


def get_simple_routes(graph, sources, sinks):
    routes = []
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                routes.append(nx.all_simple_paths(graph, source, sink))
    return routes


def find_biggest_route_reduction(graph, sources, sinks):
    routes_per_node = defaultdict(list)
    for node in graph:
        g = graph.copy()
        so = sources.copy()
        si = sinks.copy()
        g.remove_node(node)
        if node in so:
            so.remove(node)
        if node in si:
            si.remove(node)
        n_routes = len(list(chain(get_routes(g, so, si))))
        print("n_routes", n_routes)
        # if n_routes:
        routes_per_node[n_routes].append(node)
    min_nodes = min(routes_per_node.keys())#, key=lambda x: x[1])
    # if routes_per_node:
    return routes_per_node[min_nodes]


def find_path(graph, sources, sinks):
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                return source


def dedupe_removals(graph, sources, removals):
    valid_removals = []
    for removal in removals:
        copies = get_copies([graph,
                             removals,
                             sources])
        graph_copy, removals_copy, sources_copy = copies
        removals_copy.remove(removal)

        for node in removals_copy:
            graph_copy.remove_node(node)
            if node in sources_copy:
                sources_copy.remove(node)

        if is_reachable(graph_copy, sources_copy, [removal]):
            valid_removals.append(removal)
    print("removals", len(removals), "valid_removals", len(valid_removals))
    return valid_removals


def get_copies(obj_list):
    return [obj.copy() for obj in obj_list]


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
