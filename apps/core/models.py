from django.db import models
from django.utils import timezone


class TimestampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(verbose_name='Время последнего изменения', auto_now=True, db_index=True)

    @property
    def created_at_pretty(self) -> str:
        return timezone.localtime(self.created_at).strftime('%d.%m.%Y %H:%M:%S')

    created_at_pretty.fget.short_description = 'Время создания'

    @property
    def updated_at_pretty(self) -> str:
        return timezone.localtime(self.changed_at).strftime('%d.%m.%Y %H:%M:%S')

    updated_at_pretty.fget.short_description = 'Время последнего изменения'


class NameModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return self.name.replace(' ', '-').lower()
