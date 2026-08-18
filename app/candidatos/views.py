from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app.core.mixins import PublicReadAuthenticatedWriteMixin

from .models import Cargo, Candidato
from .serializers import CargoSerializer, CandidatoSerializer


class CargoViewSet(PublicReadAuthenticatedWriteMixin, viewsets.ModelViewSet):
    queryset = Cargo.objects.all().order_by("nombre")
    serializer_class = CargoSerializer


class CandidatoViewSet(PublicReadAuthenticatedWriteMixin, viewsets.ModelViewSet):
    serializer_class = CandidatoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["cargo", "activo"]

    def get_queryset(self):
        queryset = Candidato.objects.select_related("cargo").all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset