import pytest
from tests.data import cordon_data as data
from AutoCordon.cordon import cordon


@pytest.mark.unit
class TestCordon:

    @pytest.mark.parametrize(*data.test_cordon())
    def test_cordon(self, coords, distance, roads, expected_result):
        # Arrange

        # Act
        closed_roads = cordon(coords, distance, roads)
        closed_roads.sort()
        expected_result.sort()
        print(closed_roads)
        print(expected_result)

        # Assert
        assert (closed_roads == expected_result).all()
