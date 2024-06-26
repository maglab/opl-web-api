import json
import random
import pytest


class TestList:
    @pytest.mark.django_db
    def test_list_open_problems(
        self, api_client: pytest.fixture, create_random_open_problems: pytest.fixture
    ):
        """
        Test with no query params
        """
        random_integer = random.randint(a=1, b=5)
        create_random_open_problems(n=random_integer)
        endpoint = "/api/open-problems/"
        response = api_client().get(endpoint)
        # Check the status code and then check the count. Do not len the response content as pagination settings are
        # activated.
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content.get("count") == random_integer
