"""

get all Closures

make graph from cordon roads
    mark default removable as False
    mark all edges as removable (True)
add outside edges to graph

find betweeness from centre nodes to outside nodes

find max betweeness in edges in tree from inner nodes to max nodes

remove max edge

recompute until cant reach max nodes from min nodes


find closure edges




list of edges to remove


"""
import networkx as nx
from networkx.algorithms.centrality import edge_betweenness_centrality_subset
from collections import deque
import pygeos as pyg
from collections import namedtuple

DistanceNodes = namedtuple("DistanceNodes", "inner max outer")


def get_line_ends(lines):
    lines = pyg.get_parts(lines)
    return pyg.get_point(lines, 0), pyg.get_point(lines, -1)


def get_cordon_graph(lines, centre_coords, min_distance, max_distance,
                     context_distance):
    centre_point = pyg.points(centre_coords)
    closable_edges = get_edges(lines, centre_point, min_distance,
                               max_distance)
    non_closable_edges = get_edges(lines, centre_point, max_distance,
                                   context_distance)
    return make_graph(closable_edges, non_closable_edges)


def get_distance_nodes(lines, centre_coords, min_distance, max_distance,
                       context_distance):
    centre_point = pyg.points(centre_coords)
    distance_nodes = []
    for distance in (min_distance, max_distance, context_distance):
        distance_nodes.append(get_nodes(lines, centre_point, distance))
    return DistanceNodes(*distance_nodes)


def get_edges(lines, centre_point, inner_radius, outer_radius):
    polygon = make_ring_polygon(centre_point, inner_radius, outer_radius)
    lines = get_lines_in_polygon(lines, polygon)
    return list(zip(*get_line_ends(lines)))


def get_nodes(lines, centre_point, distance):
    linear_ring = pyg.get_exterior_ring(pyg.buffer(centre_point, distance))
    nodes = pyg.intersection(lines, linear_ring)
    return clean_geometry_list(nodes)


def get_lines_in_polygon(lines, polygon):
    removable_lines = pyg.intersection(lines, polygon)
    return clean_geometry_list(removable_lines)


def make_ring_polygon(centre_point, inner_radius, outer_radius):
    inner_poly = pyg.buffer(centre_point, inner_radius)
    outer_poly = pyg.buffer(centre_point, outer_radius)
    return pyg.difference(outer_poly, inner_poly)


def clean_geometry_list(geometry_list):
    geometry_list = geometry_list[~pyg.is_empty(geometry_list)]
    return pyg.get_parts(geometry_list)


def make_graph(removable_edges, non_removable_edges):
    graph = nx.Graph()
    graph.add_edges_from(removable_edges, removable=True)
    graph.add_edges_from(non_removable_edges, removable=False)
    return graph


def get_nodes_in_graph(nodes, graph):
    return [node for node in nodes if node in graph]


def get_removed_edges(graph, distance_nodes,
                      metric=edge_betweenness_centrality_subset):
    subgraphs = [graph.subgraph(list(component)).copy()
                 for component in nx.connected_components(graph)]
    removed_edges = []
    graph_deque = deque(subgraphs)
    while len(graph_deque):
        g = graph_deque.pop()
        g_inner_nodes = get_nodes_in_graph(distance_nodes.inner,
                                           graph)
        if len(g_inner_nodes):
            g_max_nodes = get_nodes_in_graph(distance_nodes.max,
                                             graph)
            if len(g_max_nodes):
                g_outer_nodes = get_nodes_in_graph(distance_nodes.outer,
                                                   graph)
                g_distance_nodes = DistanceNodes(g_inner_nodes,
                                                 g_max_nodes,
                                                 g_outer_nodes)
                removal_edge = get_removal_edge(g, g_distance_nodes, metric)
                g.remove_edge(*removal_edge)
                removed_edges.append(removal_edge)

                if is_reachable(g, g_max_nodes, g_inner_nodes):
                    for component in nx.connected_components(g):
                        graph_deque.append(g.subgraph(list(component)).copy())
    return removed_edges


def is_reachable(graph, sources, sinks):
    for source in sources:
        for sink in sinks:
            if nx.has_path(graph, source, sink):
                return True
    return False


def get_removal_edge(graph, distance_nodes, metric):
    edge_metric_values = get_edge_metric_values(graph, distance_nodes, metric)
    max_metric_value = 0
    for edge, score in edge_metric_values.items():
        if graph.edges[edge[0], edge[1]]["removable"]:
            if score >= max_metric_value:
                max_metric_value = score
                max_edge = edge
    return max_edge


def get_edge_metric_values(graph, distance_nodes, metric):
    edge_metric = metric(graph, distance_nodes.outer, distance_nodes.inner)
    if sum(edge_metric.values()) == 0:
        edge_metric = metric(graph, distance_nodes.max, distance_nodes.inner)
    return edge_metric


def get_edge_removals(lines, centre_coords, min_distance,
                      max_distance, context_distance):
    graph = get_cordon_graph(lines, centre_coords, min_distance,
                             max_distance, context_distance)
    distance_nodes = get_distance_nodes(lines, centre_coords,
                                        min_distance, max_distance,
                                        context_distance)
    return get_removed_edges(graph, distance_nodes)


if __name__ == "__main__":
    import geopandas as gpd
    import matplotlib.pyplot as plt

    roads_path = r"tests\data\SU_RoadLink.shp"
    CENTRE_COORDS = (442000, 112000)
    MIN_DISTANCE = 550
    MAX_DISTANCE = 750
    CONTEXT_FACTOR = 1.25

    roads = gpd.read_file(roads_path)
    roads = roads.explode().reset_index(drop=True)
    road_lines = pyg.from_shapely(roads.geometry)

    context_distance = MAX_DISTANCE * CONTEXT_FACTOR
    removed_edges = get_edge_removals(road_lines, CENTRE_COORDS,
                                      MIN_DISTANCE, MAX_DISTANCE,
                                      context_distance)

    # Plot results -----------------------------------------------------
    removed_lines = [pyg.linestrings(pyg.get_coordinates(coords))
                     for coords in removed_edges]
    removed_lines_gdf = gpd.GeoDataFrame({"geometry": removed_lines})
    centre_point = pyg.points(CENTRE_COORDS)
    inner_nodes = get_nodes(road_lines, centre_point, MIN_DISTANCE)
    max_nodes = get_nodes(road_lines, centre_point, MAX_DISTANCE)
    closable_polygon = make_ring_polygon(centre_point,
                                         MIN_DISTANCE,
                                         MAX_DISTANCE)
    closable_edges = get_edges(road_lines, closable_polygon)

    fig, ax = plt.subplots()
    road_lines.plot(ax=ax, color="grey")
    gpd.GeoDataFrame({"geometry": closable_edges}).plot(ax=ax)
    removed_lines_gdf.plot(ax=ax, color="r")
    gpd.GeoDataFrame({"geometry": inner_nodes}).plot(ax=ax, color="r")
    gpd.GeoDataFrame({"geometry": max_nodes}).plot(ax=ax, color="g")
    ax.set_xlim(CENTRE_COORDS[0] - context_distance,
                CENTRE_COORDS[0] + context_distance)
    ax.set_ylim(CENTRE_COORDS[1] - context_distance,
                CENTRE_COORDS[1] + context_distance)
    fig.tight_layout()
    plt.show()
