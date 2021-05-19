import pickle as pkl

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from AutoCordon.prune_edges import get_disconnected_edges
from pygeos.coordinates import get_coordinates
from pygeos.creation import linestrings

axis_buffer = 10


def get_ax(gdf):
    f, ax = plt.subplots(figsize=[15, 15])
    bounds = gdf.total_bounds
    ax.set_xlim(bounds[0] - axis_buffer, bounds[2] + axis_buffer)
    ax.set_ylim(bounds[1] - axis_buffer, bounds[3] + axis_buffer)
    return f, ax


subgraphs = pkl.load(open("subgraphs.pkl", "rb"))
remaining_roads = pkl.load(open("remaining_roads.pkl", "rb"))
remaining_roads_gdf = gpd.GeoDataFrame({"geometry": remaining_roads})
for subgraph_id in subgraphs:
    graph = nx.Graph(nx.to_undirected(subgraphs[subgraph_id]))
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    sources_gdf = gpd.GeoDataFrame({"geometry": sources})
    sinks_gdf = gpd.GeoDataFrame({"geometry": sinks})
    starting_edges = [linestrings(get_coordinates(coords)) for coords in graph.edges]
    starting_edges_gdf = gpd.GeoDataFrame({"geometry": starting_edges})

    f, ax = get_ax(starting_edges_gdf)
    remaining_roads_gdf.plot(color="gray", ax=ax)
    starting_edges_gdf.plot(ax=ax, color="r")
    sources_gdf.plot(color="r", ax=ax)
    sinks_gdf.plot(color="g", ax=ax)

    disconnected = get_disconnected_edges(graph)
    final_edges = [linestrings(get_coordinates(coords)) for coords in disconnected]
    final_edges_gdf = gpd.GeoDataFrame({"geometry": final_edges})
    final_edges_gdf.plot(ax=ax)
    ax.set_title(f"{subgraph_id}: n default = {len(sources_gdf)}, n calc = {len(starting_edges_gdf) - len(final_edges_gdf)}")

    plt.show()
