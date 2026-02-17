import pytest

from apps.cities.factories import CountryFactory, CityFactory


@pytest.fixture
def country_with_cities():
    country = CountryFactory()
    # 3 for left, right and winner failure test
    for _ in range(3):
        CityFactory(country=country)
    return country
