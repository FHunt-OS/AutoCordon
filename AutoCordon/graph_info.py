def get_edge_info_for_node(graph, node, info_name, valid_type=str,
                           invalid_fill="Unknown"):
    info = []
    for edge in graph[node].values():
            for key in edge.keys():
                edge_info = edge[key][info_name]
                if not isinstance(edge_info, valid_type):
                    edge_info = invalid_fill
                info.append(edge_info)