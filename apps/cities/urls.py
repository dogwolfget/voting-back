from django.urls import path

from apps.cities.views import CityChoiceView, CityStatsView

urlpatterns = [
    path('choose/', CityChoiceView.as_view()),
    path('stats/', CityStatsView.as_view()),
]
