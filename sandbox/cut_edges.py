import pickle as pkl

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from AutoCordon.prune_edges import get_closure_edges
from pygeos.coordinates import get_coordinates
from pygeos.creation import linestrings
from os.path import join

axis_buffer = 10


def get_ax(gdf):
    f, ax = plt.subplots(figsize=[15, 15])
    bounds = gdf.total_bounds
    ax.set_xlim(bounds[0] - axis_buffer, bounds[2] + axis_buffer)
    ax.set_ylim(bounds[1] - axis_buffer, bounds[3] + axis_buffer)
    return f, ax


def plot_closures(remaining_roads_gdf, starting_edges_gdf,
                  sources_gdf, sinks_gdf, final_edges_gdf,
                  subgraph_id, save=False, file_path=None):
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
        path = f"Subgraph {subgraph_id}.png"
        if file_path:
            path = join(file_path, path)
        plt.savefig(path)
        plt.close()
    else:
        plt.show()


def get_graph_geometry(graph):
    sources = [node[0] for node in graph.nodes("interior_closure") if node[1]]
    sinks = [node[0] for node in graph.nodes("exterior_closure") if node[1]]
    edges = [linestrings(get_coordinates(coords)) for coords in graph.edges]
    return sources, sinks, edges


def update_data_dict(data_dict, geometry, subgraph_id):
    data_dict["geometry"].extend(geometry)
    data_dict["subgraph_id"].extend([subgraph_id] * len(geometry))
    return data_dict


def update_data(data, starting_edges, sources, sinks,
                closed_edges, subgraph_id):
    data["starting_edges"] = update_data_dict(data["starting_edges"],
                                              starting_edges,
                                              subgraph_id)
    data["sources"] = update_data_dict(data["sources"],
                                       sources,
                                       subgraph_id)
    data["sinks"] = update_data_dict(data["sinks"],
                                     sinks,
                                     subgraph_id)
    data["closed_edges"] = update_data_dict(data["closed_edges"],
                                            closed_edges,
                                            subgraph_id)
    return data


subgraphs = pkl.load(open("subgraphs_OR.pkl", "rb"))
remaining_roads = pkl.load(open("remaining_roads_OR.pkl", "rb"))
remaining_roads_gdf = gpd.GeoDataFrame({"geometry": remaining_roads})

data_cols = ["starting_edges", "sources",
             "sinks", "closed_edges"]
data = {d: {"geometry": [], "subgraph_id": []} for d in data_cols}
for subgraph_id in subgraphs:
    graph = nx.Graph(nx.to_undirected(subgraphs[subgraph_id]))
    sources, sinks, starting_edges = get_graph_geometry(graph)

    closure_edges = get_closure_edges(graph)
    closed_edges = [linestrings(get_coordinates(coords))
                    for coords in closure_edges]
    data = update_data(data, starting_edges, sources, sinks,
                       closed_edges, subgraph_id)


starting_edges_gdf = gpd.GeoDataFrame(data["starting_edges"])
sources_gdf = gpd.GeoDataFrame(data["sources"])
sinks_gdf = gpd.GeoDataFrame(data["sinks"])
closed_edges_gdf = gpd.GeoDataFrame(data["closed_edges"])

plot_closures(remaining_roads_gdf,
              starting_edges_gdf,
              sources_gdf,
              sinks_gdf,
              closed_edges_gdf,
              None, save=True)
for subgraph_id in subgraphs:
    plot_closures(remaining_roads_gdf,
                  starting_edges_gdf[starting_edges_gdf["subgraph_id"] == subgraph_id],
                  sources_gdf[sources_gdf["subgraph_id"] == subgraph_id],
                  sinks_gdf[sinks_gdf["subgraph_id"] == subgraph_id],
                  closed_edges_gdf[closed_edges_gdf["subgraph_id"] == subgraph_id],
                  subgraph_id, save=True)
