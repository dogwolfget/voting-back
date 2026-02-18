from django.urls import path

from apps.cities.views import CityChoiceView, CityStatsListView, CityStatsDetailView

urlpatterns = [
    path('choose/', CityChoiceView.as_view()),
    path('stats/', CityStatsListView.as_view()),
    path('stats/<str:country>/<str:city>/', CityStatsDetailView.as_view()),
]
