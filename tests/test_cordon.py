import numpy as np
import pytest
from AutoCordon.cordon import (extract_closure_candidates,
                               get_road_closure_locations,
                               split_roads_with_cordon)
from pygeos.coordinates import get_coordinates
from pygeos.predicates import equals_exact

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


    @pytest.mark.parametrize(*data.test_split_roads_with_cordon())
    def test_split_roads_with_cordon(self, coords, distance, roads,
                                     expected_result):
        # Arrange

        # Act
        cordon_graph = split_roads_with_cordon(coords, distance, roads)
        print(cordon_graph)
        print(expected_result)
        # Assert
        assert np.isin(np.round(get_coordinates(expected_result), 2),
                       np.round(get_coordinates(cordon_graph), 2)).all()

    @pytest.mark.parametrize(*data.test_extract_closure_candidates())
    def test_extract_closure_candidates(self, centre_coord, min_distance,
                                        max_distance, roads, expected_result):
        # Arrange

        # Act
        candidates = extract_closure_candidates(centre_coord, min_distance,
                                                max_distance, roads)

        # Assert
        assert equals_exact(candidates, expected_result, tolerance=0.01).all()
