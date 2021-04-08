from pygeos.constructive import buffer
from pygeos.creation import points, linestrings
from pygeos.predicates import crosses
import numpy as np


def get_roads_crossing_cordon(coords, distance, roads):
    # Identifies which roads will have closures (not where or how many)
    basic_cordon = buffer(points(coords), distance)
    road_lines = [linestrings(road) for road in roads.values()]
    road_closures = crosses(basic_cordon, road_lines)
    return np.array(list(roads.keys()))[road_closures]
