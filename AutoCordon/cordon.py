import pygeos as pyg
from pygeos.constructive import buffer
from pygeos.creation import points, linestrings
from pygeos.predicates import crosses
import numpy as np


def cordon(coords, distance, roads):
    basic_cordon = buffer(points(coords), distance)
    road_lines = linestrings(list(roads.values()))
    road_closures = crosses(basic_cordon, road_lines)
    return np.array(list(roads.keys()))[road_closures]
