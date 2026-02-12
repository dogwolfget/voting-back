from django.contrib import admin

from apps.competitions.models import Competition, Contestant


class ContestantsInline(admin.TabularInline):
    model = Contestant
    verbose_name_plural = 'Contestants'
    extra = 1
    fields = ('name', 'cover')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author')
    search_fields = ('name',)

    inlines = [ContestantsInline]
