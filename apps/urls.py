from django.urls import include, path

urlpatterns = [
    path('authentication/', include('apps.authentication.urls')),
    path('competitions/', include('apps.competitions.urls')),
]
