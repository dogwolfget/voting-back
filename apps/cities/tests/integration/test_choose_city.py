import pytest
from rest_framework import status

from apps.cities.models import Choice, City

url = '/api/cities/choose/'


@pytest.mark.parametrize(
    'body', [
        {'left': 1, 'right': 2, 'winner': 1},
        {'left': 1, 'right': 2, 'winner': 2},
    ])
def test_choose_cities_success(api_client, country_with_cities, body):
    expected_response = {'message': 'OK'}

    response = api_client.post(url, data=body)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response

    winner = City.objects.get(pk=body['winner'])
    assert Choice.objects.get_city_attempts(winner).count() == 1
    assert Choice.objects.get_city_wins(winner).count() == 1

    loser = City.objects.exclude(pk=body['winner']).first()
    assert Choice.objects.get_city_attempts(loser).count() == 1
    assert Choice.objects.get_city_wins(loser).count() == 0


@pytest.mark.parametrize(
    'body, expected_response', [
        (
                {},
                {'left': ['This field is required.'], 'right': ['This field is required.']},
        ),
        (
                {'left': 1, 'right': 1, 'winner': 1},
                {'left': ['Have to differ from right'], 'right': ['Have to differ from left']},
        ),
        (
                {'left': 1, 'right': 2, 'winner': 3},
                {'winner': ['Have to match either left or right']},
        ),
        (
                {'left': 1, 'right': 2},
                {'winner': ['Have to match either left or right']},
        ),
        (
                {'left': 0, 'right': 0, 'winner': 0},
                {
                    'left': ['Invalid pk "0" - object does not exist.'],
                    'right': ['Invalid pk "0" - object does not exist.'],
                    'winner': ['Invalid pk "0" - object does not exist.'],
                },
        ),
    ])
def test_choose_cities_failure(api_client, country_with_cities, body, expected_response):
    response = api_client.post(url, data=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response
    assert Choice.objects.count() == 0
