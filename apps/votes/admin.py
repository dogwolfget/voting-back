from django.contrib import admin

from apps.votes.models import Competition, Contestant, Choice, Playthrough


class ContestantsInline(admin.TabularInline):
    model = Contestant
    verbose_name_plural = 'Contestants'
    extra = 1
    fields = ('name', 'cover')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')
    search_fields = ('name',)

    inlines = [ContestantsInline]


class ChoiceInline(admin.TabularInline):
    model = Choice
    verbose_name_plural = 'Choices'
    extra = 0
    fields = ('active', 'rejected')


@admin.register(Playthrough)
class PlaythroughAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition')

    inlines = [ChoiceInline]
