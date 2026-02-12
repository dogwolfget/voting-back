from rest_framework import serializers

from apps.competitions.models import Competition, Contestant


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ('name', 'cover')


class CompetitionSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    contestants = ContestantSerializer(many=True, required=False)

    class Meta:
        model = Competition
        fields = ('author', 'name', 'contestants')

    def create(self, validated_data):
        author = self.context['request'].user
        competition = Competition.objects.create(author=author, name=validated_data['name'])
        contestants = validated_data.pop('contestants', [])
        for contestant in contestants:
            cover = contestant.pop('cover')
            contestant = Contestant.objects.create(competition=competition, **contestant)
            contestant.cover = cover
            contestant.save(update_fields=['cover'])
        return competition

    @staticmethod
    def get_author(obj: Competition):
        return obj.author.email
