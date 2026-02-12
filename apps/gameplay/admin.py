from django.contrib import admin

from apps.gameplay.models import Duel, Playthrough


class DuelInline(admin.TabularInline):
    model = Duel
    verbose_name_plural = 'Duels'
    extra = 0
    fields = ('left', 'right', 'winner')


@admin.register(Playthrough)
class PlaythroughAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'competition')

    inlines = [DuelInline]
