import pytest
from rest_framework.test import APIClient
from .open_problems.factories import OpenProblemFactory
from faker import Faker
from dataclasses import dataclass

fake = Faker()


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def create_open_problems(db):
    def _create_open_problems(n):
        return OpenProblemFactory.create_batch(n)

    return _create_open_problems


@dataclass
class QueryParameters:
    p: int = (1,)
    sorting: str = ("latest",)


@pytest.fixture()
def create_query_params():
    def _create_query_params(): ...
