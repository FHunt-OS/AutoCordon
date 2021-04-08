from pytest import param
import numpy as np
import pickle as pkl

sample_roads = pkl.load(open(r"tests\data\sample_roads.pickle", "rb"))
sample_centre = (442500, 112573)


def test_cordon():
    test_variables = 'coords, distance, roads, expected_result'
    test_data = [
        param((0, 0),
              3,
              {"a": [(0, 0), (0, 10)]},
              np.array(["a"]),
              id='single road from coord'
              ),
        param((0, 0),
              3,
              {"a": [(0, 0), (0, 10)],
               "b": [(5, 5), (10, 10)]},
              np.array(["a"]),
              id='two roads, one outside cordon'
              ),
        param((0, 0),
              3,
              {"a": [(0, 0), (1, 5), (0, 10)],
               "b": [(5, 5), (10, 10)]},
              np.array(["a"]),
              id='two roads, one outside cordon'
              ),
        param((0, 0),
              3,
              {"a": [(0, 0), (0, 10)],
               "b": [(5, 5), (10, 10)],
               "c": [(0, 1), (1, 10)],
               "d": [(0, 0), (0, 2)]},
              np.array(["a", "c"]),
              id='four roads, one terminates within radius'
              ),
        param(sample_centre,
              50,
              sample_roads,
              np.array(["osgb4000000023282961",
                        "osgb4000000023282967",
                        "osgb4000000023313958",
                        "osgb4000000023313976"]),
              id='sample_roads, 50m'
              ),
        param(sample_centre,
              100,
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
              )
    ]
    return test_variables, test_data
