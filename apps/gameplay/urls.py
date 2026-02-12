from django.urls import path

from apps.gameplay.views import (
    PlaythroughCreateView,
    PlaythroughDetailView,
    DuelDetailView,
)

urlpatterns = [
    path('add/', PlaythroughCreateView.as_view()),
    path('<int:playthrough_pk>/', PlaythroughDetailView.as_view()),
    path('<int:playthrough_pk>/duel/', DuelDetailView.as_view()),
]
