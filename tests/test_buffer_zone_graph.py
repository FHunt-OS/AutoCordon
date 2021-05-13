import pytest
from AutoCordon.buffer_zone_graph import make_buffer_zone_graph

from networkx.algorithms.isomorphism import is_isomorphic
from tests.data import buffer_zone_graph_data as data


@pytest.mark.unit
class TestCordonGraph:

    @pytest.mark.parametrize(*data.test_make_buffer_zone_graph())
    def test_make_buffer_zone_graph(self, centre_coords, roads,
                                    expected_result):
        # Arrange

        # Act
        graph = make_buffer_zone_graph(centre_coords, roads)
        print(graph.edges)
        print(len(graph.edges))
        print(expected_result.edges)
        print(len(expected_result.edges))
        # Assert
        assert is_isomorphic(graph, expected_result)
