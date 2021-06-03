import networkx as nx
import numpy as np
from pygeos.creation import points
from pygeos.geometry import get_parts, get_point
from pygeos.measurement import distance


def make_buffer_zone_graph(centre_coords, roads):
    end_points = get_line_ends(roads)
    node_dists = get_distance_from_centre(end_points, centre_coords)

    # edges = []
    # for first_point, last_point in zip(*end_points):
    #     if node_dists[first_point] > node_dists[last_point]:
    #         edges.append((last_point, first_point))
    #     elif node_dists[first_point] < node_dists[last_point]:
    #         edges.append([first_point, last_point])
    #     else:
    #         edges.append([last_point, first_point])
    #         edges.append([first_point, last_point])

    graph = nx.Graph(list(zip(*end_points)))
    graph.nodes()
    nx.set_node_attributes(graph, node_dists, "dist_to_centre")
    return graph


def get_line_ends(lines):
    lines = get_parts(lines)
    return get_point(lines, 0), get_point(lines, -1)


def get_distance_from_centre(end_points, centre_coords):
    unique_points = list(set(np.concatenate(end_points)))
    distance_to_centre = distance(unique_points, points(centre_coords))
    return {node: dist for node, dist in zip(unique_points,
                                             distance_to_centre)}


def get_subgraphs(graph, interior_closure_points, exterior_closure_points,
                  exterior_closure_points_wider):
    interior_set = set(interior_closure_points)
    exterior_set = set(exterior_closure_points)
    exterior_wider_set = set(exterior_closure_points_wider)
    components = nx.connected_components(graph)
    subgraphs = {}
    for subgraph_id, component in enumerate(components):
        interior_nodes = interior_set.intersection(component)
        exterior_nodes = exterior_set.intersection(component)
        exterior_wider_nodes = exterior_wider_set.intersection(component)

        if interior_nodes and exterior_nodes:
            subgraph = graph.subgraph(list(component)).copy()
            subgraph.nodes(data="interior_closure", default=False)
            subgraph.nodes(data="exterior_closure", default=False)
            subgraph.nodes(data="exterior_wider_closure", default=False)
            for node in interior_nodes:
                subgraph.nodes[node]["interior_closure"] = True
            for node in exterior_nodes:
                subgraph.nodes[node]["exterior_closure"] = True
            for node in exterior_wider_nodes:
                subgraph.nodes[node]["exterior_wider_closure"] = True
            subgraphs[subgraph_id] = subgraph
    return subgraphs
