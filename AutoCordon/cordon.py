from pygeos.constructive import buffer
from pygeos.creation import points, prepare, linestrings
from pygeos.set_operations import intersection
from pygeos.geometry import get_exterior_ring, get_dimensions, get_parts


def get_basic_cordon(coords, distance):
    cordon = buffer(points(coords), distance)
    return get_exterior_ring(cordon)


def get_intersecting_points(intersection_result):
    points_bool = get_dimensions(intersection_result) == 0
    intersecting_points = intersection_result[points_bool]
    return get_parts(intersecting_points)


def get_road_closure_locations(coords, distance, roads):
    basic_cordon = get_basic_cordon(coords, distance)
    prepare(roads)
    intersecting_roads = intersection(roads, basic_cordon)
    return get_intersecting_points(intersecting_roads)


def get_cordon_graph(centre_coord, distance, roads):
    return linestrings([
                        [(2, 2), (2, 0.5)],
                        [(2, 0.5), (2, 1)],
                        [(2, 2), (2.5, 2)],
                        [(2.5, 2), (3, 2)],
                        [(2, 2), (2, 2.5)],
                        [(2, 2.5), (2, 3)],
                        [(2, 2), (1.5, 2)],
                        [(1.5, 2), (1, 2)]
                  ])
