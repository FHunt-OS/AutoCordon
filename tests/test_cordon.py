import numpy as np
import pytest
from AutoCordon.cordon import get_road_closure_locations
from pygeos.geometry import get_x, get_y

from tests.data import cordon_data as data


@pytest.mark.unit
class TestCordon:

    @pytest.mark.parametrize(*data.test_get_road_closure_locations())
    def test_get_road_closure_locations(self, coords, distance, roads,
                                        expected_result):
        # Arrange

        # Act
        closure_locations = get_road_closure_locations(coords, distance, roads)

        # Assert
        closure_locations_x = np.round(get_x(closure_locations), 2)
        closure_locations_y = np.round(get_y(closure_locations), 2)
        closure_coords = set(list(zip(closure_locations_x,
                                      closure_locations_y)))

        assert closure_coords == expected_result
