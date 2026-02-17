from django.db import models
from django_random_queryset import RandomManager

from apps.cities.managers import ChoiceManager
from apps.core.models import TimestampModel, NameModel


def flag_file_path(instance: 'Country', filename: str) -> str:
    return f'flags/{instance.slug}/{filename}'


def city_photo_file_path(instance: 'City', filename: str) -> str:
    return f'photos/{instance.country.slug}/{instance.slug}/{filename}'


class Country(TimestampModel, NameModel):
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    flag = models.ImageField(upload_to=flag_file_path, null=True, blank=True)


class City(TimestampModel, NameModel):
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    objects = RandomManager()

    country = models.ForeignKey(Country, related_name='cities', null=True, blank=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=city_photo_file_path, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Choice(TimestampModel):
    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    objects = ChoiceManager()

    left = models.ForeignKey(City, related_name='choices_as_left', on_delete=models.CASCADE)
    right = models.ForeignKey(City, related_name='choices_as_right', on_delete=models.CASCADE)
    winner = models.ForeignKey(City, related_name='choices_as_winner', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        sign = '>'
        if not self.winner:
            sign = '/'
        elif self.winner == self.right:
            sign = '<'
        return f"{self.left} {sign} {self.right}"
