import networkx as nx


def is_reachable(graph, sources, sinks):
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                return True
    return False


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
