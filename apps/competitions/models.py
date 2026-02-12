from django.db import models

from apps.core.models import TimestampModel
from apps.users.models import User


def contestant_cover_path(instance, filename):
    return f'contestants/{instance.competition.pk}/{instance.pk}/{filename}'


class Competition(TimestampModel):
    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_competitions')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} by {self.author.email}'


class Contestant(TimestampModel):
    class Meta:
        verbose_name = 'Contestant'
        verbose_name_plural = 'Contestants'

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='contestants')
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to=contestant_cover_path)

    def __str__(self):
        return f'{self.competition.name} choice {self.name}'
