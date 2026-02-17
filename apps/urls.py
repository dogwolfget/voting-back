from django.urls import include, path

urlpatterns = [
    path('cities/', include('apps.cities.urls')),
]
