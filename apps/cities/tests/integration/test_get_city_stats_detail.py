from rest_framework import status

url = '/api/cities/stats/{}/{}/'


def test_get_stats_detail_empty(api_client, country_with_cities):
    city = country_with_cities.cities.first()
    response = api_client.get(url.format(country_with_cities.name, city.name))

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['best_vs'] == []
    assert response_data['worst_vs'] == []


def test_get_stats_detail(api_client, country_with_choices):
    cities = country_with_choices.cities.all()

    response = api_client.get(url.format(country_with_choices.name, cities[0].name))
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['best_vs'] == []
    assert response_data['worst_vs'] == [
        {
            "name": str(cities[1]),
            "stats": {
                "attempts": 3,
                "wins": 1,
                "winrate": 33.33
            }
        }
    ]

    response = api_client.get(url.format(country_with_choices.name, cities[1].name))
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['best_vs'] == [
        {
            "name": str(cities[0]),
            "stats": {
                "attempts": 3,
                "wins": 2,
                "winrate": 66.67
            }
        }
    ]
    assert response_data['worst_vs'] == []

    response = api_client.get(url.format(country_with_choices.name, cities[2].name))
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['best_vs'] == []
    assert response_data['worst_vs'] == []


def test_get_stats_detail_not_found(api_client):
    response = api_client.get(url.format('test', 'test'))
    assert response.status_code == status.HTTP_404_NOT_FOUND
