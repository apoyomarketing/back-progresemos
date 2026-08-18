from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "estado": user.estado,
        "is_staff": user.is_staff,
        "rol": {
            "id": user.rol.id,
            "nombre": user.rol.nombre,
        } if user.rol else None,
    })