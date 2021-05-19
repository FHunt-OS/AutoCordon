import geopandas as gpd
from AutoCordon.buffer_zone import BufferZone
from AutoCordon.buffer_zone_graph import get_subgraphs, make_buffer_zone_graph
from pygeos.io import from_shapely
import pickle as pkl

roads = gpd.read_file(r"tests\data\sample_roads_soton_centre.geojson")
roads = roads.explode().reset_index(drop=True)
road_lines = from_shapely(roads.geometry)
distance = 550
distance_max = 750
centre = (442000, 112000)

bz = BufferZone(centre, distance, distance_max)
remaining_roads = bz.get_intersecting_lines(road_lines)
interior_closure_points = bz.get_intersecting_perimeter_points("interior",
                                                               road_lines)
exterior_closure_points = bz.get_intersecting_perimeter_points("exterior",
                                                               road_lines)

graph = make_buffer_zone_graph(centre, remaining_roads)
subgraphs = get_subgraphs(graph, interior_closure_points,
                          exterior_closure_points)

pkl.dump(subgraphs, open("subgraphs.pkl", "wb"))
pkl.dump(remaining_roads, open("remaining_roads.pkl", "wb"))
