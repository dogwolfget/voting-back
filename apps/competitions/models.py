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

    @property
    def valid(self):
        return self.contestants.count() > 1

    @property
    def max_size(self):
        total_size = self.contestants.count()
        current_size = 2
        if current_size >= total_size:
            return current_size

        while current_size < total_size:
            current_size *= 2

        return int(current_size / 2)


class Contestant(TimestampModel):
    class Meta:
        verbose_name = 'Contestant'
        verbose_name_plural = 'Contestants'

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='contestants')
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to=contestant_cover_path)

    def __str__(self):
        return f'{self.competition.name} choice {self.name}'

    def save(self, *args, **kwargs):
        if self.pk:
            return super().save(*args, **kwargs)

        cover = self.cover
        self.cover = None
        super().save(*args, **kwargs)
        kwargs.pop('force_insert', None)
        self.cover = cover
        return self.save(update_fields=['cover'])
