from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from apps.competitions.models import Competition
from apps.competitions.serializers import CompetitionSerializer


class CompetitionCreateView(CreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionListView(ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionMyListView(ListAPIView):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class CompetitionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'competition_pk'

    def get_queryset(self):
        if self.request.method == 'GET':
            return self.queryset
        return self.queryset.filter(author=self.request.user)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
