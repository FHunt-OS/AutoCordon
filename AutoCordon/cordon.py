from pygeos.constructive import buffer
from pygeos.creation import points, linestrings, prepare
from pygeos.predicates import crosses
from pygeos.set_operations import intersection
from pygeos.geometry import get_exterior_ring
import numpy as np


def prepare_roads(roads):
    road_lines = [linestrings(road) for road in roads.values()]
    prepare(road_lines)
    return road_lines


def get_basic_cordon(coords, distance):
    cordon = buffer(points(coords), distance)
    return get_exterior_ring(cordon)


def get_roads_crossing_cordon(basic_cordon, roads):
    # Identifies which roads will have closures (not where or how many)
    road_lines = prepare_roads(roads)
    road_closures = crosses(road_lines, basic_cordon)
    return np.array(list(roads.keys()))[road_closures]


def get_road_closure_locations(basic_cordon, roads_crossing_cordon):
    return intersection(roads_crossing_cordon, basic_cordon)


def cordon(coords, distance, roads):
    basic_cordon = get_basic_cordon(coords, distance)
    roads_crossing_cordon = get_roads_crossing_cordon(basic_cordon, roads)
    roads_cross_geoms = [roads[road] for road in roads_crossing_cordon]  # TODO get rid of this step
    get_road_closure_locations(basic_cordon, roads_cross_geoms)
