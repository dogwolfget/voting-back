from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from apps.competitions.models import Competition

from apps.gameplay.models import Playthrough
from apps.gameplay.serializers import (
    PlaythroughCreateSerializer,
    PlaythroughSerializer,
    DuelSerializer,
    WinnerSerializer,
)


class PlaythroughCreateView(GenericAPIView):
    serializer_class = PlaythroughCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        competition = get_object_or_404(Competition, pk=serializer.validated_data['competition_id'])
        if not competition.valid:
            raise ValidationError(detail={'competition': 'Competition does not have enough contestants'})

        size = serializer.validated_data.get('size', competition.max_size)
        playthrough = Playthrough.objects.create(competition=competition, user=request.user)
        playthrough.create_stage(size=size)

        output_serializer = PlaythroughSerializer(instance=playthrough)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)


class PlaythroughDetailView(RetrieveAPIView):
    serializer_class = PlaythroughSerializer
    queryset = Playthrough.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'playthrough_pk'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class DuelDetailView(GenericAPIView):
    queryset = Playthrough.objects.all()
    serializer_class = WinnerSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'playthrough_pk'

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_class if kwargs.get('type') != 'duel' else DuelSerializer

    def get(self, request, *args, **kwargs):
        playthrough = self.get_object()
        duel = playthrough.get_current_duel()
        if not duel:
            playthrough.create_stage()
            duel = playthrough.get_current_duel()
        elif duel.winner:
            serializer = self.get_serializer({'winner': playthrough.winner.name})
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        serializer = self.get_serializer(duel, type='duel')
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playthrough = self.get_object()
        duel = playthrough.get_current_duel()
        duel.choose(serializer.validated_data['winner'])
        return Response(status=status.HTTP_201_CREATED, data={'message': 'OK'})
