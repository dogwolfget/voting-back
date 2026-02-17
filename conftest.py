from django.test import Client

from apps.cities.tests.fixtures import *  # noqa


@pytest.fixture
def api_client(db):
    return Client()
