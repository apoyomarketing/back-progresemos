from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
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

from rest_framework.response import Response
from rest_framework import status

class CategoriaPublicacionViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = CategoriaPublicacion.objects.all()
    serializer_class = CategoriaPublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']

class PublicacionViewSet(viewsets.ModelViewSet):
    """CRUD with slug lookup; anonymous users see only published posts."""
    pagination_class = None
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estado', 'categoria']
    ordering = ['-fecha_creacion']
    ordering_fields = ['fecha_creacion']

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(estado='publicado')
        return qs

class MultimediaViewSet(viewsets.ModelViewSet):
    """CRUD for multimedia with filters for activo and tipo."""
    pagination_class = None
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activo', 'tipo']
    ordering = ['-id']

class CarruselViewSet(viewsets.ModelViewSet):
    """CRUD for carrusel; filter by activo and order by 'orden'."""
    pagination_class = None
    queryset = Carrusel.objects.all()
    serializer_class = CarruselSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activo']
    ordering = ['orden']

class DocumentoViewSet(viewsets.ModelViewSet):
    """CRUD for documento; filter by activo."""
    pagination_class = None
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activo']
    ordering = ['-id']

class ConfiguracionSitioViewSet(viewsets.ModelViewSet):
    """Singleton configuration; read allowed to all, write limited to staff/authenticated users."""
    pagination_class = None
    queryset = ConfiguracionSitio.objects.all()
    serializer_class = ConfiguracionSitioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['clave']

    from rest_framework.response import Response
    from rest_framework import status
    def create(self, request, *args, **kwargs):
        """Create or update the singleton ConfiguracionSitio instance."""
        if ConfiguracionSitio.objects.exists():
            instance = ConfiguracionSitio.objects.first()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
