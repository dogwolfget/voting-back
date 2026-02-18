from rest_framework import serializers

from apps.cities.dtos import StatDTO
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

    def validate(self, attrs):
        if attrs['left'] == attrs['right']:
            raise serializers.ValidationError({
                'left': 'Have to differ from right',
                'right': 'Have to differ from left',
            })
        winner = attrs.get('winner')
        if not winner or winner not in (attrs['left'], attrs['right']):
            raise serializers.ValidationError({'winner': 'Have to match either left or right'})
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['left'] = CitySerializer(instance.left).data
        representation['right'] = CitySerializer(instance.right).data
        return representation


class CityStatsSerializer(CitySerializer):
    stats = serializers.SerializerMethodField()

    class Meta(CitySerializer.Meta):
        fields = CitySerializer.Meta.fields + ('stats',)

    @staticmethod
    def get_stats(obj: City):
        attempts = Choice.objects.get_city_attempts(obj).count()
        wins = Choice.objects.get_city_wins(obj).count()
        return StatDTO(attempts=attempts, wins=wins).as_dict()


class CityAdvancedStatsSerializer(CityStatsSerializer):
    stats = serializers.SerializerMethodField()
    best_vs = serializers.SerializerMethodField()
    worst_vs = serializers.SerializerMethodField()

    class Meta(CityStatsSerializer.Meta):
        fields = CityStatsSerializer.Meta.fields + ('best_vs', 'worst_vs')

    @staticmethod
    def get_best_vs(obj: City):
        opponents = obj.get_stats()
        data = [
            {'name': f'{k.name} ({k.country.name})', 'stats': v.as_dict()}
            for k, v in opponents.items() if v.winrate > 50
        ]
        data.sort(key=lambda x: x['stats']['winrate'])
        return data[:5]

    @staticmethod
    def get_worst_vs(obj: City):
        opponents = obj.get_stats()
        data = [
            {'name': f'{k.name} ({k.country.name})', 'stats': v.as_dict()}
            for k, v in opponents.items() if v.winrate < 50
        ]
        data.sort(key=lambda x: x['stats']['winrate'], reverse=True)
        return data[:5]
