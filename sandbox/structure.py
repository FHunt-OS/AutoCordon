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
from AutoCordon.buffer_zone_graph import get_line_ends
from AutoCordon.prune_edges import is_reachable
import networkx as nx
from networkx.algorithms.centrality import edge_current_flow_betweenness_centrality_subset as flow_betweenness
from networkx.algorithms.centrality import edge_betweenness_centrality_subset
import geopandas as gpd
from pygeos.io import from_shapely
import matplotlib.pyplot as plt
from collections import deque
import pygeos
import numpy as np
import math

roads_path = r"tests\data\SU_RoadLink.shp"
centre = (442000, 112000)
distance = 550
distance_max = 750
wider_factors = [1, 1.25, 1.5, 2]


roads = gpd.read_file(roads_path)
roads = roads.explode().reset_index(drop=True)
road_lines = from_shapely(roads.geometry)

centre_point = pygeos.points(centre)
middle_hole_buffer = pygeos.buffer(centre_point, distance)
max_closure_buffer = pygeos.buffer(centre_point, distance_max)
closable_ring_buffer = pygeos.difference(max_closure_buffer, middle_hole_buffer)
inner_nodes = pygeos.intersection(pygeos.get_interior_ring(closable_ring_buffer, 0), road_lines)
max_nodes = pygeos.intersection(pygeos.get_exterior_ring(closable_ring_buffer), road_lines)
inner_nodes = pygeos.get_parts(inner_nodes[~pygeos.is_empty(inner_nodes)])
max_nodes = pygeos.get_parts(max_nodes[~pygeos.is_empty(max_nodes)])
closable_lines = pygeos.intersection(road_lines, closable_ring_buffer)
lines_removable = pygeos.get_parts(closable_lines[~pygeos.is_empty(closable_lines)])
removable_edges = list(zip(*get_line_ends(lines_removable)))

f, ax = plt.subplots(2, math.ceil(len(wider_factors) / 2), sharex=True, sharey=True)
ax = np.ravel(ax)
for i in range(len(wider_factors)):

    distance_wider = distance_max * wider_factors[i]

    wider_buffer = pygeos.buffer(centre_point, distance_wider)

    ring_buffer = pygeos.difference(wider_buffer, middle_hole_buffer)

    ring_lines = pygeos.intersection(road_lines, ring_buffer)
    wider_lines = pygeos.difference(ring_lines, closable_ring_buffer)

    outer_nodes = pygeos.intersection(pygeos.get_exterior_ring(ring_buffer), road_lines)

    lines_non_removable = pygeos.get_parts(wider_lines[~pygeos.is_empty(wider_lines)])
    outer_nodes = pygeos.get_parts(outer_nodes[~pygeos.is_empty(outer_nodes)])

    non_removable_edges = list(zip(*get_line_ends(lines_non_removable)))

    graph = nx.Graph()
    graph.add_edges_from(removable_edges, removable=True)
    graph.add_edges_from(non_removable_edges, removable=False)

    subgraphs = [graph.subgraph(list(component)).copy()
                 for component in nx.connected_components(graph)]

    removed_edges = []
    graph_deque = deque(subgraphs)
    while len(graph_deque):
        g = graph_deque.pop()

        g_inner_nodes = [node for node in inner_nodes if node in g]
        if len(g_inner_nodes):
            g_max_nodes = [node for node in max_nodes if node in g]
            if len(g_max_nodes):

                g_outer_nodes = [node for node in outer_nodes if node in g]
                betweeness = edge_betweenness_centrality_subset(g,
                                                                g_outer_nodes,
                                                                g_inner_nodes)
                if sum(betweeness.values()) == 0:
                    betweeness = edge_betweenness_centrality_subset(g,
                                                                    g_max_nodes,
                                                                    g_inner_nodes)

                max_betweeness = 0
                for edge, score in betweeness.items():
                    if g.edges[edge[0], edge[1]]["removable"]:
                        if score >= max_betweeness:
                            max_betweeness = score
                            max_edge = edge

                g.remove_edge(*max_edge)
                removed_edges.append(max_edge)

                if is_reachable(g, g_max_nodes, g_inner_nodes):
                    for component in nx.connected_components(g):
                        graph_deque.append(g.subgraph(list(component)).copy())

    removed_lines = [pygeos.linestrings(pygeos.get_coordinates(coords))
                     for coords in removed_edges]
    starting_lines = [pygeos.linestrings(pygeos.get_coordinates(coords))
                      for coords in removable_edges]
    removed_lines_gdf = gpd.GeoDataFrame({"geometry": removed_lines})
    starting_lines_gdf = gpd.GeoDataFrame({"geometry": starting_lines})

    starting_lines_gdf.plot(ax=ax[i])
    removed_lines_gdf.plot(ax=ax[i], color="r")
    gpd.GeoDataFrame({"geometry": inner_nodes}).plot(ax=ax[i], color="r")
    gpd.GeoDataFrame({"geometry": max_nodes}).plot(ax=ax[i], color="g")
    gpd.GeoDataFrame({"geometry": lines_non_removable}).plot(ax=ax[i], color="grey")
    ax[i].set_title(wider_factors[i])
f.tight_layout()
plt.show()
