from rest_framework import serializers

from apps.cities.models import City, Choice, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'flag')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'photo', 'country')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = CountrySerializer(instance.country).data
        return representation


class ChooseCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('left', 'right', 'winner')
        extra_kwargs = {'winner': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['left'] = CitySerializer(instance['left']).data
        representation['right'] = CitySerializer(instance['right']).data
        return representation
