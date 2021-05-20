import pickle as pkl

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from AutoCordon.prune_edges import get_closure_edges
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
    starting_edges_gdf.plot("subgraph_id", ax=ax, cmap="tab20")
    sources_gdf.plot(color="r", ax=ax)
    sinks_gdf.plot(color="g", ax=ax)
    final_edges_gdf.plot(ax=ax, color="r")
    n_final_edges = len(final_edges_gdf)
    outcome = "REDUCTION" if n_final_edges < len(sources_gdf) else "USE DEFAULT"
    ax.set_title(f""" Subgraph {subgraph_id} {outcome}:
                 n default = {len(sources_gdf)}, n calc = {n_final_edges}""")
    if save:
        plt.savefig(f"Subgraph {subgraph_id}.png")
        plt.close()
    else:
        plt.show()


def get_graph_geometry(graph):
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    edges = [linestrings(get_coordinates(coords))
                      for coords in graph.edges]
    return sources, sinks, edges


all_sources = []
all_sinks = []
all_closed_edges = []
all_starting_edges = []
starting_edge_subgraph_ids = []
source_subgraph_ids = []
sink_subgraph_ids = []
closure_subgraph_ids = []

subgraphs = pkl.load(open("subgraphs_OR.pkl", "rb"))
remaining_roads = pkl.load(open("remaining_roads_OR.pkl", "rb"))
remaining_roads_gdf = gpd.GeoDataFrame({"geometry": remaining_roads})
for subgraph_id in subgraphs:
    graph = nx.Graph(nx.to_undirected(subgraphs[subgraph_id]))
    sources, sinks, starting_edges = get_graph_geometry(graph)

    closure_edges = get_closure_edges(graph)
    closed_edges = [linestrings(get_coordinates(coords))
                    for coords in closure_edges]

    all_starting_edges.extend(starting_edges)
    all_sources.extend(sources)
    all_sinks.extend(sinks)
    all_closed_edges.extend(closed_edges)
    starting_edge_subgraph_ids.extend([subgraph_id] * len(starting_edges))
    source_subgraph_ids.extend([subgraph_id] * len(sources))
    sink_subgraph_ids.extend([subgraph_id] * len(sinks))
    closure_subgraph_ids.extend([subgraph_id] * len(closed_edges))


sources_gdf = gpd.GeoDataFrame({"geometry": all_sources,
                                "subgraph_id": source_subgraph_ids})
sinks_gdf = gpd.GeoDataFrame({"geometry": all_sinks,
                              "subgraph_id": sink_subgraph_ids})
starting_edges_gdf = gpd.GeoDataFrame({"geometry": all_starting_edges,
                                       "subgraph_id": starting_edge_subgraph_ids})
closed_edges_gdf = gpd.GeoDataFrame({"geometry": all_closed_edges,
                                     "subgraph_id": closure_subgraph_ids})

for subgraph_id in subgraphs:
    plot_closures(remaining_roads_gdf,
                  starting_edges_gdf[starting_edges_gdf["subgraph_id"] == subgraph_id],
                  sources_gdf[sources_gdf["subgraph_id"] == subgraph_id],
                  sinks_gdf[sinks_gdf["subgraph_id"] == subgraph_id],
                  closed_edges_gdf[closed_edges_gdf["subgraph_id"] == subgraph_id],
                  subgraph_id, save=True)
