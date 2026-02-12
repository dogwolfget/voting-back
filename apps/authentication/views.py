from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView

from apps.authentication.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class TokenObtainPairView(BaseTokenObtainPairView):
    pass
