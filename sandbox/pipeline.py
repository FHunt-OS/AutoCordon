import geopandas as gpd
from AutoCordon.buffer_zone import BufferZone
from AutoCordon.buffer_zone_graph import make_buffer_zone_graph, get_subgraphs
from cut_edges import get_all_closures, plot_closures
from pygeos.io import from_shapely
import momepy as mm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

roads_path = r"tests\data\SU_RoadLink.shp"
distance = 550
distance_max = 750
distance_wider = distance_max * 1.25
centre = (442000, 112000)

roads = gpd.read_file(roads_path)
roads = roads.explode().reset_index(drop=True)
roads_simplified = mm.remove_false_nodes(roads)
road_lines = from_shapely(roads_simplified.geometry)

cordon_bz = BufferZone(centre, distance, distance_max)

remaining_roads = cordon_bz.get_intersecting_lines(road_lines)
interior_closure_points = cordon_bz.get_intersecting_perimeter_points("interior",
                                                                      road_lines)
exterior_closure_points = cordon_bz.get_intersecting_perimeter_points("exterior",
                                                                      road_lines)

wider_bz = BufferZone(centre, distance_max, distance_wider)

outside_roads = wider_bz.get_intersecting_lines(road_lines)
outside_points = wider_bz.get_intersecting_perimeter_points("exterior",
                                                            road_lines)

all_remaining_roads = np.concatenate((remaining_roads, outside_roads))
remaining_roads_gdf = gpd.GeoDataFrame(geometry=all_remaining_roads)
# remaining_roads_gdf.plot()
# plt.show()
# exit()

inner_graph = make_buffer_zone_graph(centre, remaining_roads)
full_graph = make_buffer_zone_graph(centre, all_remaining_roads)
# graph = nx.Graph(nx.to_undirected(graph))

subgraphs = get_subgraphs(full_graph, interior_closure_points,
                          exterior_closure_points,
                          outside_points)
data = get_all_closures(subgraphs, inner_graph)

starting_edges_gdf = gpd.GeoDataFrame(data["starting_edges"])
sources_gdf = gpd.GeoDataFrame(data["sources"])
sinks_gdf = gpd.GeoDataFrame(data["sinks"])
closed_edges_calc_gdf = gpd.GeoDataFrame(data["closed_edges_calc"])
closed_edges_hybrid_gdf = gpd.GeoDataFrame(data["closed_edges_hybrid"])

plot_closures(remaining_roads_gdf,
              starting_edges_gdf,
              sources_gdf,
              sinks_gdf,
              closed_edges_calc_gdf,
              closed_edges_hybrid_gdf,
              None, save=False)
for subgraph_id in subgraphs:
    plot_closures(remaining_roads_gdf,
                  starting_edges_gdf[starting_edges_gdf["subgraph_id"] == subgraph_id],
                  sources_gdf[sources_gdf["subgraph_id"] == subgraph_id],
                  sinks_gdf[sinks_gdf["subgraph_id"] == subgraph_id],
                  closed_edges_calc_gdf[closed_edges_calc_gdf["subgraph_id"] == subgraph_id],
                  closed_edges_hybrid_gdf[closed_edges_hybrid_gdf["subgraph_id"] == subgraph_id],
                  subgraph_id, save=False)
