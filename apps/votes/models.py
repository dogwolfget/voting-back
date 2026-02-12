from django.db import models

from apps.core.models import TimestampModel
from apps.users.models import User
from apps.votes.managers import ChoiceManager


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
    cover = models.ImageField(upload_to='contestants/')

    def __str__(self):
        return f'{self.competition.name} choice {self.name}'


class Playthrough(TimestampModel):
    class Meta:
        verbose_name = 'User playthrough'
        verbose_name_plural = 'User playthroughs'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playthroughs')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='playthroughs')

    def __str__(self):
        return f'{self.user.email} in {self.competition.name}'

    @property
    def winner(self):
        unrejected = self.choices.unrejected()
        return unrejected.first() if unrejected.count() == 1 else None

    @property
    def completed_stage(self):
        return not self.choices.filter(active=True).exists()


class Choice(TimestampModel):
    class Meta:
        verbose_name = 'User choice'
        verbose_name_plural = 'User choices'

    objects = ChoiceManager()

    playthrough = models.ForeignKey(Playthrough, on_delete=models.CASCADE, related_name='choices')
    active = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.playthrough.user.email} in {self.playthrough.competition.name}'

    def choose(self):
        self.active = False
        self.save(update_fields=['active'])

    def reject(self):
        self.rejected = True
        self.active = False
        self.save(update_fields=['rejected', 'active'])
