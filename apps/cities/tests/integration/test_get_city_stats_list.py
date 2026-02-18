from rest_framework import status

from apps.cities.tests.integration.test_choose_city import url as choose_url

url = '/api/cities/stats/'


def test_get_stats_empty(api_client, country_with_cities):
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['results']
    assert all([x['stats']['attempts'] == 0 for x in response_data['results']])
    assert all([x['stats']['wins'] == 0 for x in response_data['results']])
    assert all([x['stats']['winrate'] == 0 for x in response_data['results']])


def test_get_stats(api_client, country_with_cities):
    def get_current_stats():
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        return response.json()['results']

    api_client.post(choose_url, data={'left': 1, 'right': 2, 'winner': 1})
    response_data = get_current_stats()
    left_stats = response_data[0]['stats']
    assert left_stats['attempts'] == 1
    assert left_stats['wins'] == 1
    assert left_stats['winrate'] == 100.0
    right_stats = response_data[1]['stats']
    assert right_stats['attempts'] == 1
    assert right_stats['wins'] == 0
    assert right_stats['winrate'] == 0.0

    api_client.post(choose_url, data={'left': 1, 'right': 2, 'winner': 2})
    response_data = get_current_stats()
    left_stats = response_data[0]['stats']
    assert left_stats['attempts'] == 2
    assert left_stats['wins'] == 1
    assert left_stats['winrate'] == 50.0
    right_stats = response_data[1]['stats']
    assert right_stats['attempts'] == 2
    assert right_stats['wins'] == 1
    assert right_stats['winrate'] == 50.0

    api_client.post(choose_url, data={'left': 1, 'right': 2, 'winner': 2})
    response_data = get_current_stats()
    left_stats = response_data[0]['stats']
    assert left_stats['attempts'] == 3
    assert left_stats['wins'] == 1
    assert left_stats['winrate'] == 33.33
    right_stats = response_data[1]['stats']
    assert right_stats['attempts'] == 3
    assert right_stats['wins'] == 2
    assert right_stats['winrate'] == 66.67
