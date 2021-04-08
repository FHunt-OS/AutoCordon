import pytest
from AutoCordon.cordon import (get_road_closure_locations,
                               get_roads_crossing_cordon)
from pygeos.constructive import normalize
from pygeos.predicates import equals_exact

from tests.data import cordon_data as data


@pytest.mark.unit
class TestCordon:

    @pytest.mark.parametrize(*data.test_get_roads_crossing_cordon())
    def test_get_roads_crossing_cordon(self, basic_cordon, roads,
                                       expected_result):
        # Arrange

        # Act
        closed_roads = get_roads_crossing_cordon(basic_cordon, roads)
        closed_roads.sort()
        expected_result.sort()

        # Assert
        assert (closed_roads == expected_result).all()

    @pytest.mark.parametrize(*data.test_get_road_closure_locations())
    def test_get_road_closure_locations(self, basic_cordon,
                                        roads_crossing_cordon,
                                        expected_result):
        # Arrange

        # Act
        closure_locations = get_road_closure_locations(basic_cordon,
                                                       roads_crossing_cordon)

        # Assert
        assert equals_exact(normalize(closure_locations),
                            normalize(expected_result),
                            tolerance=0.0001).all()
