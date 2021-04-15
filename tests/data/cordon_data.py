from pytest import param
from tests.data.dummy_roads import centre_crossroads, dummy_roads
from pygeos.creation import points

def test_get_road_closure_locations():
    test_variables = 'coords, distance, roads, expected_result'
    test_data = [
        param((2, 2),
              0.5,
              centre_crossroads,
              points([(2.0, 1.5),
                      (2.5, 2.0),
                      (2.0, 2.5),
                      (1.5, 2.0)]),
              id='centre_crossroads distance 0.5'
              ),
        param((2, 2),
              1,
              centre_crossroads,
              points([(2.0, 1.0),
                      (3.0, 2.0),
                      (2.0, 3.0),
                      (1.0, 2.0)]),
              id='centre_crossroads distance 1'
              ),
        param((2, 2),
              1.25,
              dummy_roads,
              points([(1.26, 3.0),
                      (2.74, 3.0),
                      (1.0, 2.74),
                      (3.0, 1.26),
                      (1.26, 1.0),
                      (2.74, 1.0),
                      (1.0, 1.26),
                      (3.0, 2.74)]),
              id='dummy_roads distance 1.25'
              )
        ]
    return test_variables, test_data
