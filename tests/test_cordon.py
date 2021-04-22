import numpy as np
import pytest
from AutoCordon.cordon import get_road_closure_locations, get_cordon_graph
from pygeos.coordinates import get_coordinates

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
        assert np.isin(np.round(get_coordinates(expected_result), 2),
                       np.round(get_coordinates(closure_locations), 2)).all()

    @pytest.mark.parametrize(*data.test_get_cordon_graph())
    def test_get_cordon_graph(self, coords, distance, roads,
                                        expected_result):
        # Arrange

        # Act
        cordon_graph = get_cordon_graph(coords, distance, roads)

        # Assert
        assert np.isin(np.round(get_coordinates(expected_result), 2),
                       np.round(get_coordinates(cordon_graph), 2)).all()
