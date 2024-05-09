import pytest
from rest_framework.test import APIClient
from faker import Faker

from .open_problems.factories import OpenProblemFactory, SubmittedOpenProblemFactory


fake = Faker()


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def create_random_open_problems(db):
    def _create_open_problems(n):
        return OpenProblemFactory.create_batch(n)

    return _create_open_problems


@pytest.fixture
def create_open_problem(db):
    def _create_open_problem(**kwargs):
        return OpenProblemFactory.build(**kwargs)

    return _create_open_problem


@pytest.fixture
def create_submitted_problem(db):
    def _create_submitted_problem(**kwargs):
        return SubmittedOpenProblemFactory.build(**kwargs)

    return _create_submitted_problem
