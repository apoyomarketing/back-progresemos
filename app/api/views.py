from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
def health(request):
    return JsonResponse({'status': 'ok'})

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
