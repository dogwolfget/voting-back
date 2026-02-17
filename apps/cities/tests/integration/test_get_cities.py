from rest_framework import status

url = '/api/cities/choose/'


def test_get_cities(api_client, country_with_cities):
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['left']['id'] != response_data['right']['id']
