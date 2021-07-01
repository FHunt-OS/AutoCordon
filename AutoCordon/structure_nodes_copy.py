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
from networkx.algorithms.centrality import betweenness_centrality_subset, current_flow_betweenness_centrality_subset
import geopandas as gpd
from pygeos.io import from_shapely
import matplotlib.pyplot as plt
from collections import deque
import pygeos as pyg
import numpy as np
import math
from AutoCordon.get_roads import get_roads
from AutoCordon.manipulate_geometries import intersect, get_donut, overlay_gdf_with_geom
import momepy as mm


def get_junction_closures(centre, distance, distance_max,
                          edge_metric_func=betweenness_centrality_subset):
    roads = get_roads(centre, distance_max + 10)
    
    point = pyg.points(centre)
    
    hole = pyg.buffer(point, distance)
    hole_ring = pyg.get_exterior_ring(hole)
    
    shell = pyg.buffer(point, distance_max)
    shell_ring = pyg.get_exterior_ring(shell)

    shell_points = overlay_gdf_with_geom(roads, shell_ring)
    max_nodes = list(zip(shell_points.geometry.x, shell_points.geometry.y))
    
    hole_points = overlay_gdf_with_geom(roads, hole_ring)
    inner_nodes = list(zip(hole_points.geometry.x, hole_points.geometry.y))
    
    donut = pyg.polygons(shell_ring, holes=[hole_ring])
    donut_roads = overlay_gdf_with_geom(roads, donut)
    donut_roads_simplified = mm.remove_false_nodes(donut_roads)

    graph = mm.gdf_to_nx(donut_roads_simplified)
    subgraphs = [graph.subgraph(list(component)).copy()
                for component in nx.connected_components(graph)]
    
    removed_nodes = []
    graph_deque = deque(subgraphs)
    while len(graph_deque):
        g = graph_deque.pop()

        g_inner_nodes = [node for node in inner_nodes if node in g]
        if len(g_inner_nodes):
            g_max_nodes = [node for node in max_nodes if node in g]
            if len(g_max_nodes):
                betweeness = edge_metric_func(g,
                                                g_max_nodes,
                                                g_inner_nodes)
                if sum(betweeness.values()) == 0:
                    betweeness = edge_metric_func(g,
                                                  g_max_nodes,
                                                  g_inner_nodes)


                betweeness = {node: betweeness[node] for node in g.nodes}
                max_node = max(list(betweeness.items()), key=lambda x: x[1])[0]
                # TODO if joint max scores, choose closest to centre?
                g.remove_node(max_node)
                removed_nodes.append(max_node)
                if max_node in g_max_nodes:
                    g_max_nodes.remove(max_node)
                if max_node in g_inner_nodes:
                    g_inner_nodes.remove(max_node)

                if is_reachable(g, g_max_nodes, g_inner_nodes):
                    for component in nx.connected_components(g):
                        graph_deque.append(g.subgraph(list(component)).copy())

    return removed_nodes, hole, donut, graph
