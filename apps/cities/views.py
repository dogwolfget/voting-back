from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from apps.cities.models import City, Choice
from apps.cities.serializers import ChooseCitySerializer, CityStatsSerializer, CityAdvancedStatsSerializer


class CityChoiceView(CreateAPIView, RetrieveAPIView):
    serializer_class = ChooseCitySerializer

    def get_object(self):
        left = City.objects.random().first()
        right = City.objects.exclude(pk=left.pk).random().first()
        return Choice(left=left, right=right)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'OK'})


class CityStatsListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityStatsSerializer


class CityStatsDetailView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityAdvancedStatsSerializer

    def get_object(self):
        return get_object_or_404(City, country__name=self.kwargs['country'], name=self.kwargs['city'])
