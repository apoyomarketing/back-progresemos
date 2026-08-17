from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all().order_by("id")
    serializer_class = RolSerializer
    permission_classes = [IsAdminUser]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related("rol").all().order_by("id")
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminUser]