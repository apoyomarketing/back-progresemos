from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
)

from .serializers import (
    CategoriaPublicacionSerializer,
    PublicacionSerializer,
    MultimediaSerializer,
    CarruselSerializer,
    DocumentoSerializer,
    ConfiguracionSitioSerializer,
)


class PublicReadAuthenticatedWriteMixin:
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAdminUser()]


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
            queryset = queryset.filter(estado="publicado")

        return queryset

    def perform_create(self, serializer):
        estado = serializer.validated_data.get("estado", "borrador")

        if estado == "publicado":
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

        if estado == "publicado" and serializer.instance.fecha_publicacion is None:
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
