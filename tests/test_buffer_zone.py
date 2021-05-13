import numpy as np
import pytest
from AutoCordon.buffer_zone import BufferZone
from pygeos.coordinates import get_coordinates
from pygeos.predicates import equals_exact

from tests.data import buffer_zone_data as data


@pytest.mark.unit
class TestBufferZone:

    @pytest.mark.parametrize(*data.test_get_intersecting_lines())
    def test_get_intersecting_lines(self, centre_coord, min_distance,
                                    max_distance, roads, expected_result):
        # Arrange
        bz = BufferZone(centre_coord, min_distance, max_distance)

        # Act
        candidates = bz.get_intersecting_lines(roads)

        # Assert
        assert equals_exact(candidates, expected_result, tolerance=0.01).all()

    @pytest.mark.parametrize(*data.test_get_intersecting_perimeter_points())
    def test_get_intersecting_perimeter_points(self, coords, min_distance,
                                               max_distance, roads, edge,
                                               expected_result):
        # Arrange
        bz = BufferZone(coords, min_distance, max_distance)

        # Act
        candidates = bz.get_intersecting_perimeter_points(edge, roads)

        # Assert
        assert np.isin(np.round(get_coordinates(expected_result), 2),
                       np.round(get_coordinates(candidates), 2)).all()
