from rest_framework import viewsets, permissions

from .models import Departamento, Provincia, Distrito
from .serializers import DepartamentoSerializer, ProvinciaSerializer, DistritoSerializer


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Departamento.objects.all().order_by("id_departamento")
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.AllowAny]


class ProvinciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Provincia.objects.all().order_by("id_provincia")
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()

        departamento_id = self.request.query_params.get("departamento")

        if departamento_id:
            qs = qs.filter(departamento_id=departamento_id)

        return qs


class DistritoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Distrito.objects.all().order_by("id_distrito")
    serializer_class = DistritoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()

        provincia_id = self.request.query_params.get("provincia")

        if provincia_id:
            qs = qs.filter(provincia_id=provincia_id)

        return qs