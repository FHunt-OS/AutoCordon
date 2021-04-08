from pytest import param
import numpy as np


def test_cordon():
    test_variables = 'coords, distance, roads, expected_result'
    test_data = [
        param((0, 0),
              3,
              {"a": ((0, 0), (0, 10))},
              np.array(["a"]),
              id='single road from coord'
              ),
        param((0, 0),
              3,
              {"a": ((0, 0), (0, 10)),
               "b": ((5, 5), (10, 10))},
              np.array(["a"]),
              id='two roads, one closure'
              ),
        param((0, 0),
              3,
              {"a": ((0, 0), (0, 10)),
               "b": ((5, 5), (10, 10)),
               "c": ((0, 1), (1, 10)),
               "d": ((0, 0), (0, 2))},
              np.array(["a", "c"]),
              id='four roads, one terminates within radius'
              )
    ]
    return test_variables, test_data
