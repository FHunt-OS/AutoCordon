from pytest import param
from tests.data.dummy_roads import centre_crossroads, dummy_roads
from pygeos.creation import linestrings, points


def test_get_intersecting_lines():
    test_variables = 'centre_coord, min_distance, max_distance, roads, expected_result'
    test_data = [
        param((2, 2),
              0.5,
              1,
              centre_crossroads,
              linestrings([
                        [(2, 1.5), (2, 1)],
                        [(2.5, 2), (3, 2)],
                        [(2, 2.5), (2, 3)],
                        [(1.5, 2), (1, 2)]
                  ]),
              id='centre_crossroads min_dist 0.5, max_dist 1'
              ),
        param((2, 2),
              0.5,
              1,
              dummy_roads,
              linestrings([
                        [(2, 1.5), (2, 1)],
                        [(2.5, 2), (3, 2)],
                        [(2, 2.5), (2, 3)],
                        [(1.5, 2), (1, 2)]
                  ]),
              id='dummy_roads min_dist 0.5, max_dist 1'
              ),
        ]
    return test_variables, test_data


def test_get_intersecting_perimeter_points():
    test_variables = 'coords, min_distance, max_distance, roads, edge, expected_result'
    test_data = [
        param((2, 2),
              0.5,
              3,
              centre_crossroads,
              "interior",
              points([(2.0, 1.5),
                      (2.5, 2.0),
                      (2.0, 2.5),
                      (1.5, 2.0)]),
              id='centre_crossroads distance 0.5 interior'
              ),
        param((2, 2),
              1,
              3,
              centre_crossroads,
              "interior",
              points([(2.0, 1.0),
                      (3.0, 2.0),
                      (2.0, 3.0),
                      (1.0, 2.0)]),
              id='centre_crossroads distance 1 interior'
              ),
        param((2, 2),
              1.25,
              3,
              dummy_roads,
              "interior",
              points([(1.26, 3.0),
                      (2.74, 3.0),
                      (1.0, 2.74),
                      (3.0, 1.26),
                      (1.26, 1.0),
                      (2.74, 1.0),
                      (1.0, 1.26),
                      (3.0, 2.74)]),
              id='dummy_roads distance 1.25 interior'
              ),
        param((2, 2),
              0.25,
              0.5,
              centre_crossroads,
              "exterior",
              points([(2.0, 1.5),
                      (2.5, 2.0),
                      (2.0, 2.5),
                      (1.5, 2.0)]),
              id='centre_crossroads distance 0.5 exterior'
              ),
        param((2, 2),
              0.5,
              1,
              centre_crossroads,
              "exterior",
              points([(2.0, 1.0),
                      (3.0, 2.0),
                      (2.0, 3.0),
                      (1.0, 2.0)]),
              id='centre_crossroads distance 1 exterior'
              ),
        param((2, 2),
              1,
              1.25,
              dummy_roads,
              "exterior",
              points([(1.26, 3.0),
                      (2.74, 3.0),
                      (1.0, 2.74),
                      (3.0, 1.26),
                      (1.26, 1.0),
                      (2.74, 1.0),
                      (1.0, 1.26),
                      (3.0, 2.74)]),
              id='dummy_roads distance 1.25 exterior'
              )
        ]
    return test_variables, test_data
