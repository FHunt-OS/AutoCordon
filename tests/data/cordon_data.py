from pytest import param


def test_cordon():
    test_variables = 'coords, distance, roads, expected_result'
    test_data = [
        param((0, 0),
              3,
              {"a": ((0, 0), (0, 10))},
              "a",
              id='single road from coord'
              )
    ]
    return test_variables, test_data
