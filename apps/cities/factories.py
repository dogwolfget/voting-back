import factory
from factory.django import DjangoModelFactory

from apps.cities.models import City, Country, Choice


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker('word')


class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker('word')
    country = factory.SubFactory(CountryFactory)


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    left = factory.SubFactory(CityFactory)
    right = factory.SubFactory(CityFactory)
