from rest_framework import serializers

from apps.gameplay.models import Playthrough, Duel


class PlaythroughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playthrough
        fields = ('pk', 'competition', 'stage')


class PlaythroughCreateSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    size = serializers.IntegerField(required=False)

    @staticmethod
    def validate_size(value):
        if value <= 0 or (value & (value - 1)) != 0:
            raise serializers.ValidationError('Size must be power of 2')
        return value


class DuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duel
        fields = ('left', 'right')


class DuelChooseSerializer(serializers.Serializer):
    winner = serializers.CharField()
