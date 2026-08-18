from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from app.core.mixins import PublicReadAuthenticatedWriteMixin

from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
    Propuesta,
    Estadistica,
    Faq,
)

from .serializers import (
    CategoriaPublicacionSerializer,
    PublicacionSerializer,
    MultimediaSerializer,
    CarruselSerializer,
    DocumentoSerializer,
    ConfiguracionSitioSerializer,
    PropuestaSerializer,
    EstadisticaSerializer,
    FaqSerializer,
)


class CategoriaPublicacionViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    queryset = CategoriaPublicacion.objects.all()
    serializer_class = CategoriaPublicacionSerializer


class PublicacionViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = PublicacionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["categoria", "estado"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Publicacion.objects.select_related(
            "categoria",
            "usuario"
        ).all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(estado=Publicacion.Estado.PUBLICADO)

        return queryset

    def perform_create(self, serializer):
        estado = serializer.validated_data.get("estado", Publicacion.Estado.BORRADOR)

        if estado == Publicacion.Estado.PUBLICADO:
            serializer.save(
                usuario=self.request.user,
                fecha_publicacion=timezone.now()
            )
        else:
            serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        estado = serializer.validated_data.get(
            "estado",
            serializer.instance.estado
        )

        if estado == Publicacion.Estado.PUBLICADO and serializer.instance.fecha_publicacion is None:
            serializer.save(fecha_publicacion=timezone.now())
        else:
            serializer.save()


class MultimediaViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = MultimediaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tipo", "activo"]

    def get_queryset(self):
        queryset = Multimedia.objects.select_related("usuario").all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class CarruselViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = CarruselSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["activo"]

    def get_queryset(self):
        queryset = Carrusel.objects.all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset


class DocumentoViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = DocumentoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["activo", "tipo_archivo"]

    def get_queryset(self):
        queryset = Documento.objects.select_related("usuario").all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ConfiguracionSitioViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    queryset = ConfiguracionSitio.objects.all()
    serializer_class = ConfiguracionSitioSerializer

    def create(self, request, *args, **kwargs):
        if ConfiguracionSitio.objects.exists():
            return Response(
                {
                    "detail": (
                        "La configuración del sitio ya existe. "
                        "Utilice PATCH o PUT para modificarla."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


class PropuestaViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = PropuestaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["eje", "activo"]

    def get_queryset(self):
        queryset = Propuesta.objects.all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset


class EstadisticaViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = EstadisticaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["activo"]

    def get_queryset(self):
        queryset = Estadistica.objects.all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset


class FaqViewSet(
    PublicReadAuthenticatedWriteMixin,
    viewsets.ModelViewSet
):
    serializer_class = FaqSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["activo"]

    def get_queryset(self):
        queryset = Faq.objects.all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(activo=True)

        return queryset
