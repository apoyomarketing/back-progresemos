from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cargo, Candidato
from .serializers import CargoSerializer, CandidatoSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all().order_by("nombre")
    serializer_class = CargoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CandidatoViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.select_related("cargo").all()
    serializer_class = CandidatoSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["cargo", "activo"]