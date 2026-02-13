from django.db import models
from django.db.models import Q

from apps.competitions.models import Contestant, Competition
from apps.core.models import TimestampModel
from apps.gameplay.constants import STAGES
from apps.users.models import User


class Playthrough(TimestampModel):
    class Meta:
        verbose_name = 'Playthrough'
        verbose_name_plural = 'Playthroughs'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playthroughs')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='playthroughs')
    stage = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} in {self.competition.name}'

    @property
    def winner(self):
        if final := self.duels.filter(stage='FINAL').first():
            return final.winner
        return None

    def get_current_duel(self):
        return self.duels.filter(
            Q(stage=self.stage, winner__isnull=True) | Q(stage=STAGES[2], winner__isnull=False)
        ).first()

    def create_stage(self, size: int = 0):
        duels = (
            self._get_first_stage_duels(size)
            if size else
            self._get_next_stage_duels()
        )
        Duel.objects.bulk_create(duels)
        self.change_stage(size)

    def _get_first_stage_duels(self, size: int):
        contestants = self.competition.contestants.order_by('?')[:size]
        return [
            Duel(
                playthrough=self,
                left=contestants[i],
                right=contestants[i + 1],
                stage=STAGES.get(size, f'LAST_{size}'),
            )
            for i in range(0, len(contestants), 2)
        ]

    def _get_next_stage_duels(self):
        prev_duels = self.duels.filter(stage=self.stage)
        size = len(prev_duels)
        return [
            Duel(
                playthrough=self,
                left=prev_duels[i].winner,
                right=prev_duels[i + 1].winner,
                stage=STAGES.get(size, f'LAST_{size}'),
            )
            for i in range(0, len(prev_duels), 2)
        ]

    def change_stage(self, size: int):
        size = (
            size
            if size else
            self.duels.filter(stage=self.stage).count()
        )
        self.stage = STAGES.get(size, f'LAST_{size}')
        self.save(update_fields=['stage'])


class Duel(TimestampModel):
    class Meta:
        verbose_name = 'Duel'
        verbose_name_plural = 'Duels'

    playthrough = models.ForeignKey(Playthrough, on_delete=models.CASCADE, related_name='duels')
    left = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='duels_as_left')
    right = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='duels_as_right')
    winner = models.ForeignKey(
        Contestant,
        on_delete=models.CASCADE,
        related_name='duels_as_winner',
        null=True,
        blank=True,
    )
    stage = models.CharField(max_length=100)

    def __str__(self):
        if self.winner:
            sign = '>' if self.winner == self.left else '<'
            return f'{self.left.name} {sign} {self.right.name}'
        return f'{self.left.name} or {self.right.name}'

    def choose(self, side: str):
        if not self.winner:
            if side == 'left':
                self._choose_left()
            elif side == 'right':
                self._choose_right()

    def _choose_left(self):
        self.winner = self.left
        self.save(update_fields=['winner'])

    def _choose_right(self):
        self.winner = self.right
        self.save(update_fields=['winner'])
