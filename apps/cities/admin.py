from django.contrib import admin

from apps.cities.models import Country, City, Choice


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('str_display',)
    search_fields = ('left', 'right', 'winner')

    @admin.display(description="str")
    def str_display(self, obj):
        return str(obj)
