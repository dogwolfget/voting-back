from django.urls import path

from apps.authentication.views import TokenObtainPairView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
]
