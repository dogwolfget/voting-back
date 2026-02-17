from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from apps.cities.models import City, Choice
from apps.cities.serializers import ChooseCitySerializer, CityStatSerializer


class CityChoiceView(CreateAPIView, RetrieveAPIView):
    serializer_class = ChooseCitySerializer

    def get_object(self):
        return Choice(left=City.objects.random().first(), right=City.objects.random().first())

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'OK'})


class CityStatsView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityStatSerializer
