import json
import random

from django.urls import reverse, resolve
from open_problems.views import (
    ListProblemsView,
    SubmitOpenProblemView,
    RetrieveProblemView,
)
from .factories import OpenProblemFactory
import pytest


class TestList:
    @pytest.mark.django_db
    def test_list_open_problems(
        self, api_client: pytest.fixture, create_open_problems: pytest.fixture
    ):
        """
        Test with no query params
        """
        random_integer = random.randint(a=1, b=5)
        create_open_problems(n=random_integer)
        endpoint = "/api/open-problems/"
        response = api_client().get(endpoint)
        # Check the status code and then check the count. Do not len the response content as pagination settings are
        # activated.
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content.get("count") == random_integer

    @pytest.mark.django_db
    def test_list_query_params(self):
        """Test with query params"""
        ...
