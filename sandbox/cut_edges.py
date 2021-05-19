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


def plot_closures(remaining_roads_gdf, starting_edges_gdf,
                  sources_gdf, sinks_gdf, final_edges_gdf,
                  subgraph_id, save=False):
    if subgraph_id is None:
        subgraph_id = "All"
    f, ax = get_ax(starting_edges_gdf)
    remaining_roads_gdf.plot(color="gainsboro", ax=ax)
    starting_edges_gdf.plot(ax=ax, color="r")
    sources_gdf.plot(color="r", ax=ax)
    sinks_gdf.plot(color="g", ax=ax)
    final_edges_gdf.plot("subgraph_id", ax=ax, cmap="tab20")
    n_final_edges = len(starting_edges_gdf) - len(final_edges_gdf)
    outcome = "REDUCTION" if n_final_edges < len(sources_gdf) else "USE DEFAULT"
    ax.set_title(f""" Subgraph {subgraph_id} {outcome}:
                 n default = {len(sources_gdf)}, n calc = {n_final_edges}""")
    if save:
        plt.savefig(f"Subgraph {subgraph_id}.png")
        plt.close()
    else:
        plt.show()


all_sources = []
all_sinks = []
all_final_edges = []
all_starting_edges = []
edge_subgraph_ids = []

subgraphs = pkl.load(open("subgraphs_OR.pkl", "rb"))
remaining_roads = pkl.load(open("remaining_roads_OR.pkl", "rb"))
remaining_roads_gdf = gpd.GeoDataFrame({"geometry": remaining_roads})
for subgraph_id in subgraphs:
    graph = nx.Graph(nx.to_undirected(subgraphs[subgraph_id]))
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    sources_gdf = gpd.GeoDataFrame({"geometry": sources})
    sinks_gdf = gpd.GeoDataFrame({"geometry": sinks})
    starting_edges = [linestrings(get_coordinates(coords))
                      for coords in graph.edges]
    starting_edges_gdf = gpd.GeoDataFrame({"geometry": starting_edges})
    disconnected = get_disconnected_edges(graph)
    final_edges = [linestrings(get_coordinates(coords))
                   for coords in disconnected]
    graph_id = [subgraph_id] * len(final_edges)
    edge_subgraph_ids.extend(graph_id)
    final_edges_gdf = gpd.GeoDataFrame({"geometry": final_edges,
                                    "subgraph_id": graph_id})

    plot_closures(remaining_roads_gdf, starting_edges_gdf,
                  sources_gdf, sinks_gdf, final_edges_gdf,
                  subgraph_id, save=True)

    all_sources.extend(sources)
    all_sinks.extend(sinks)
    all_starting_edges.extend(starting_edges)
    all_final_edges.extend(final_edges)

sources_gdf = gpd.GeoDataFrame({"geometry": all_sources})
sinks_gdf = gpd.GeoDataFrame({"geometry": all_sinks})
starting_edges_gdf = gpd.GeoDataFrame({"geometry": all_starting_edges})
final_edges_gdf = gpd.GeoDataFrame({"geometry": all_final_edges,
                                    "subgraph_id": edge_subgraph_ids})

plot_closures(remaining_roads_gdf, starting_edges_gdf,
              sources_gdf, sinks_gdf, final_edges_gdf,
              None, save=True)
