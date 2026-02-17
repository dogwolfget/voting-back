from django.db import models
from django.db.models import Q


class ChoiceManager(models.Manager):
    def get_city_attempts(self, obj: 'City'):
        return self.get_queryset().filter(Q(left=obj) | Q(right=obj))

    def get_city_wins(self, obj: 'City'):
        return self.get_queryset().filter(winner=obj)
