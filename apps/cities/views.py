from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.cities.models import City, Choice
from apps.cities.serializers import ChooseCitySerializer


class CityChoiceView(GenericAPIView):
    serializer_class = ChooseCitySerializer

    def get(self, request, *args, **kwargs):
        data = {
            'left': City.objects.random().first().pk,
            'right': City.objects.random().first().pk,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Choice.objects.create(
            left=serializer.validated_data['left'],
            right=serializer.validated_data['right'],
            winner=serializer.validated_data['winner'],
        )

        return Response(status=status.HTTP_201_CREATED, data={'message': 'OK'})
