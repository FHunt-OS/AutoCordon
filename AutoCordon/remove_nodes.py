from networkx.algorithms.centrality import betweenness_centrality_subset

from AutoCordon.prune_edges import find_path, get_copies, is_reachable


def get_removals(graph, hole_nodes, shell_nodes):
    graph_rm, hole_nodes_rm, shell_nodes_rm = get_copies([graph,
                                                          hole_nodes,
                                                          shell_nodes])

    removed_nodes = []
    reachable = is_reachable(graph_rm, hole_nodes_rm, shell_nodes_rm)
    while reachable:
        betweeness = betweenness_centrality_subset(graph_rm, hole_nodes_rm,
                                                   shell_nodes_rm)
        max_node, max_betweeness = max(list(betweeness.items()),
                                       key=lambda x: x[1])
        if max_betweeness == 0:
            max_node = find_path(graph_rm, hole_nodes_rm, shell_nodes_rm)
            hole_nodes_rm.remove(max_node)
        graph_rm.remove_node(max_node)
        removed_nodes.append(max_node)
        reachable = is_reachable(graph_rm, hole_nodes_rm,
                                 shell_nodes_rm)
    return removed_nodes
