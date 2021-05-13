from AutoCordon.cordon_graph import make_buffer_zone_graph
from AutoCordon.buffer_zone import BufferZone
from pygeos.io import from_shapely
import geopandas as gpd

roads = gpd.read_file(r"tests\data\sample_roads_soton_centre.geojson").explode().reset_index(drop=True)
road_lines = from_shapely(roads.geometry)
distance = 550
distance_max = 750
centre = (442000, 112000)

bz = BufferZone(centre, distance, distance_max)
remaining_roads = bz.get_intersecting_lines(road_lines)
interior_closure_points = bz.get_intersecting_perimeter_points("interior", road_lines)
exterior_closure_points = bz.get_intersecting_perimeter_points("exterior", road_lines)

g = make_buffer_zone_graph(centre, remaining_roads)

