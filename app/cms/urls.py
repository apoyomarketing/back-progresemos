from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register(r'categorias-publicacion', viewsets.CategoriaPublicacionViewSet, basename='categorias-publicacion')
router.register(r'publicaciones', viewsets.PublicacionViewSet, basename='publicaciones')
router.register(r'multimedia', viewsets.MultimediaViewSet, basename='multimedia')
router.register(r'carruseles', viewsets.CarruselViewSet, basename='carruseles')
router.register(r'documentos', viewsets.DocumentoViewSet, basename='documentos')
router.register(r'configuracion-sitio', viewsets.ConfiguracionSitioViewSet, basename='configuracion-sitio')
router.register(r'propuestas', viewsets.PropuestaViewSet, basename='propuestas')
router.register(r'estadisticas', viewsets.EstadisticaViewSet, basename='estadisticas')
router.register(r'faqs', viewsets.FaqViewSet, basename='faqs')

urlpatterns = router.urls
