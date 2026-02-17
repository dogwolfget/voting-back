from django.urls import path

from apps.cities.views import CityChoiceView

urlpatterns = [
    path('', CityChoiceView.as_view()),
]
