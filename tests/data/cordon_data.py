import pickle as pkl

import numpy as np
from AutoCordon.cordon import get_basic_cordon
from pygeos.creation import linestrings, points
from pytest import param
from tests.data.dummy_roads import dummy_roads, centre_crossroads

sample_roads = pkl.load(open(r"tests\data\test_roads.pickle", "rb"))
sample_centre = (442500, 112573)


def test_get_roads_crossing_cordon():
    test_variables = 'basic_cordon, roads, expected_result'
    test_data = [
        param(get_basic_cordon((0, 0), 3),
              {"a": [(0, 0), (0, 10)]},
              np.array(["a"]),
              id='single road from coord'
              ),
        param(get_basic_cordon((0, 0), 3),
              {"a": [(0, 0), (0, 10)],
               "b": [(5, 5), (10, 10)]},
              np.array(["a"]),
              id='two roads, one outside cordon'
              ),
        param(get_basic_cordon((0, 0), 3),
              {"a": [(0, 0), (1, 5), (0, 10)],
               "b": [(5, 5), (10, 10)]},
              np.array(["a"]),
              id='two roads, one outside cordon'
              ),
        param(get_basic_cordon((0, 0), 3),
              {"a": [(0, 0), (0, 10)],
               "b": [(5, 5), (10, 10)],
               "c": [(0, 1), (1, 10)],
               "d": [(0, 0), (0, 2)]},
              np.array(["a", "c"]),
              id='four roads, one terminates within radius'
              ),
        param(get_basic_cordon(sample_centre, 50),
              sample_roads,
              np.array(["osgb4000000023282961",
                        "osgb4000000023282967",
                        "osgb4000000023313958",
                        "osgb4000000023313976"]),
              id='sample_roads, 50m'
              ),
        param(get_basic_cordon(sample_centre, 100),
              sample_roads,
              np.array(["osgb4000000023282966",
                        "osgb4000000023282965",
                        "osgb5000005209993358",
                        "osgb5000005209993360",
                        "osgb4000000023282961",
                        "osgb4000000023282963",
                        "osgb4000000023282967",
                        "osgb4000000023282960"]),
              id='sample_roads, 100m'
              ),
        param(get_basic_cordon((2, 2), 0.5),
              {fid: road for fid, road in enumerate(dummy_roads)},
              np.array([0, 1, 2, 3]),
              id='centre dummy_roads'
              ),
        param(get_basic_cordon((2, 2), 1.1),
              {fid: road for fid, road in enumerate(dummy_roads)},
              np.array([4, 5, 6, 7]),
              id='ring dummy_roads'
              ),
        param(get_basic_cordon((2, 2), 1.5),
              {fid: road for fid, road in enumerate(dummy_roads)},
              np.array([8, 9, 10, 11]),
              id='spoke dummy_roads'
              )
    ]
    return test_variables, test_data


def test_get_road_closure_locations():
    test_variables = 'basic_cordon, roads_crossing_cordon, expected_result'
    test_data = [
        param(get_basic_cordon((2, 2), 0.5),
              [linestrings(road) for road in centre_crossroads],
              [points((2, 1.5)),
               points((2.5, 2)),
               points((2, 2.5)),
               points((1.5, 2))],
              id='centre dummy_roads distance 0.5'
              ),
        param(get_basic_cordon((2, 2), 1),
              [linestrings(road) for road in centre_crossroads],
              [points((2, 1)),
               points((3, 2)),
               points((2, 3)),
               points((1, 2))],
              id='centre dummy_roads distance 1'
              )
        ]
    return test_variables, test_data
