import pytest
from tests.data import some_functionality_data as data


@pytest.mark.unit
class TestSomeFunctionality:

    @pytest.mark.parametrize(*data.test_some_functionality())
    def test_some_functionality(self, input_data, expected_result):
        # Arrange

        # Act

        # Assert
        assert input_data == expected_result
