from pygeos.constructive import buffer
from pygeos.creation import points, linestrings, prepare
from pygeos.set_operations import intersection
from pygeos.geometry import get_exterior_ring, get_dimensions, get_parts


def get_prepared_roads(roads):
    road_lines = [linestrings(road) for road in roads]
    prepare(road_lines)
    return road_lines


def get_basic_cordon(coords, distance):
    cordon = buffer(points(coords), distance)
    return get_exterior_ring(cordon)


def get_road_closure_locations(coords, distance, roads):
    basic_cordon = get_basic_cordon(coords, distance)
    prepared_roads = get_prepared_roads(roads)
    intersecting_roads = intersection(prepared_roads, basic_cordon)
    intersecting_points = [geom for geom in intersecting_roads
                           if get_dimensions(geom) == 0]
    return get_parts(intersecting_points)
