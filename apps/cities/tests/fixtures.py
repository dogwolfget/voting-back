import pytest

from apps.cities.factories import CountryFactory, CityFactory, ChoiceFactory


@pytest.fixture
def country_with_cities():
    country = CountryFactory()
    # 3 for left, right and winner failure test
    for _ in range(3):
        CityFactory(country=country)
    return country


@pytest.fixture
def country_with_choices(country_with_cities):
    cities = country_with_cities.cities.all()
    ChoiceFactory(left=cities[0], right=cities[1], winner=cities[0])
    ChoiceFactory(left=cities[0], right=cities[1], winner=cities[1])
    ChoiceFactory(left=cities[0], right=cities[1], winner=cities[1])
    return country_with_cities
