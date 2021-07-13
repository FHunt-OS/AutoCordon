def get_edge_info_for_node(graph, node, info_names, valid_type=str,
                           invalid_fill="Unknown"):
    info = []
    for edge in graph[node].values():
        for key in edge.keys():
            edge_info = invalid_fill
            for info_name in info_names:
                edge_value = edge[key][info_name]
                if isinstance(edge_value, str):
                    edge_value = edge_value.strip().lower()
                if isinstance(edge_value, valid_type) and edge_value != "null":
                    edge_info = edge_value
                    if valid_type == str:
                        edge_info = edge_info.title()
                    break
            info.append(" " + edge_info)
    return info


def get_edge_info(graph, nodes, info_names,
                  valid_type=str, invalid_fill="Unknown"):
    info = []
    for node in nodes:
        edge_info = get_edge_info_for_node(graph, node,
                                           info_names, valid_type,
                                           invalid_fill)
        info.append(list(set(edge_info)))
    return info
