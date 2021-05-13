import networkx as nx
from pygeos.creation import linestrings, points
from pytest import param
from tests.data.dummy_roads import centre_crossroads_coords, ring_road_coords


def test_make_buffer_zone_graph():
    test_variables = 'centre_coords, roads, expected_result'
    test_data = [
        param((2, 2),
              linestrings(centre_crossroads_coords),
              nx.DiGraph(centre_crossroads_coords),
              id='centre_crossroads'
              ),
        param((2, 2),
              linestrings(ring_road_coords),
              nx.DiGraph([
                    [points(3, 1), points(3, 3)],
                    [points(3, 3), points(3, 1)],

                    [points(3, 3), points(1, 3)],
                    [points(1, 3), points(3, 3)],

                    [points(1, 3), points(1, 1)],
                    [points(1, 1), points(1, 3)],

                    [points(1, 1), points(3, 1)],
                    [points(3, 1), points(1, 1)]
                    ]),
              id='dummy_roads'
              ),
        ]
    return test_variables, test_data
