from django.urls import path, include
from rest_framework import routers
from . import views as api_views
from cms.viewsets import (
    CategoriaPublicacionViewSet,
    PublicacionViewSet,
    MultimediaViewSet,
    CarruselViewSet,
    DocumentoViewSet,
    ConfiguracionSitioViewSet,
)
from candidatos.views import CargoViewSet, CandidatoViewSet
from ubicaciones.views import DepartamentoViewSet, ProvinciaViewSet, DistritoViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'cargos', CargoViewSet, basename='cargos')
router.register(r'candidatos', CandidatoViewSet, basename='candidatos')
router.register(r'departamentos', DepartamentoViewSet, basename='departamentos')
router.register(r'provincias', ProvinciaViewSet, basename='provincias')
router.register(r'distritos', DistritoViewSet, basename='distritos')
router.register(r'categorias-publicacion', CategoriaPublicacionViewSet, basename='categorias-publicacion')
router.register(r'publicaciones', PublicacionViewSet, basename='publicaciones')
router.register(r'multimedia', MultimediaViewSet, basename='multimedia')
router.register(r'carruseles', CarruselViewSet, basename='carruseles')
router.register(r'documentos', DocumentoViewSet, basename='documentos')
router.register(r'configuracion-sitio', ConfiguracionSitioViewSet, basename='configuracion-sitio')

urlpatterns = [
    path('health/', api_views.health, name='health'),
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', api_views.me, name='me'),
]
