from django.urls import path
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = SimpleRouter()
router.register(r'roles', views.RolViewSet, basename='roles')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.me, name='me'),
    path('auth-token/', auth_views.obtain_auth_token, name='api-token'),
    *router.urls,
]
