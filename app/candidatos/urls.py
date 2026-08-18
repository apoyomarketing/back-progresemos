from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'cargos', views.CargoViewSet, basename='cargos')
router.register(r'candidatos', views.CandidatoViewSet, basename='candidatos')

urlpatterns = router.urls
