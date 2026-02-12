from django.urls import path

from apps.competitions.views import (
    CompetitionCreateView,
    CompetitionListView,
    CompetitionMyListView,
    CompetitionDetailAPIView,
)

urlpatterns = [
    path('add/', CompetitionCreateView.as_view()),
    path('list/', CompetitionListView.as_view()),
    path('my/', CompetitionMyListView.as_view()),
    path('<int:competition_pk>/', CompetitionDetailAPIView.as_view()),
]
