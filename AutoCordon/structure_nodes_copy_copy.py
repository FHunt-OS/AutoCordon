import momepy as mm
from networkx.algorithms.centrality import betweenness_centrality_subset

from AutoCordon.get_roads import get_roads
from AutoCordon.manipulate_geometries import get_geoms, overlay_gdf_with_geom
from AutoCordon.prune_edges import (dedupe_removals, find_path, get_copies,
                                    is_reachable)


def get_junction_closures(centre, distance, distance_max):
    roads = get_roads(centre, distance_max + 10)
    geoms = get_geoms(roads,
                      centre,
                      distance,
                      distance_max)
    donut_roads = overlay_gdf_with_geom(roads, geoms["polygons"]["donut"])
    graph = mm.gdf_to_nx(donut_roads)
    removed_nodes = get_removals(graph,
                                 geoms['nodes']["hole"],
                                 geoms['nodes']["shell"])
    return (removed_nodes, geoms["polygons"]["hole"],
            geoms["polygons"]["donut"], graph)


def get_removals(graph, inner_nodes, outer_nodes):
    removed_nodes = remove_nodes(graph,
                                 inner_nodes,
                                 outer_nodes)
    return dedupe_removals(graph,
                           inner_nodes,
                           removed_nodes)


def remove_nodes(graph, hole_nodes, shell_nodes):
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
