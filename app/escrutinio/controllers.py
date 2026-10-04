from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import services, serializers
from .models import LocalVotacion, Partido

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def gestionar_partidos(request):
    """
    GET: Listar todos los partidos políticos.
    POST: Crear un nuevo partido político si no existe.
    Ejemplo Body POST:
    {
        "nombre_partido": "NUEVO PARTIDO POLITICO",
        "categoria": "PARTIDO"
    }
    """
    if request.method == 'GET':
        partidos = Partido.objects.all().order_by('id_partido')
        serializer = serializers.PartidoSerializer(partidos, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = serializers.PartidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def listar_locales(request):
    provincia = request.query_params.get('provincia')
    distrito = request.query_params.get('distrito')
    
    locales = LocalVotacion.objects.all()
    if provincia:
        locales = locales.filter(provincia=provincia)
    if distrito:
        locales = locales.filter(distrito=distrito)
        
    serializer = serializers.LocalVotacionSerializer(locales, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_votos(request):
    """
    Formato esperado:
    {
        "id_local": 15958,
        "nro_mesa": "012345",
        "tipo_eleccion": "PROVINCIAL",
        "votos": [
            {"id_partido": 1, "cant_voto": 100},
            {"id_partido": 2, "cant_voto": 80}
        ]
    }
    """
    data = request.data
    try:
        serv_votos = services.registrar_votos_mesa(
            id_local=data['id_local'],
            nro_mesa=data['nro_mesa'],
            tipo_eleccion=data['tipo_eleccion'],
            datos_votos=data['votos']
        )
        return Response({"mensaje": f"{len(serv_votos)} registros de votos guardados correctamente."})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def resultados_provinciales(request):
    provincia = request.query_params.get('provincia', 'PUNO')
    tipo_eleccion = request.query_params.get('tipo', 'PROVINCIAL')
    resultados = services.obtener_resultados_provinciales(provincia, tipo_eleccion)
    return Response(resultados)

@api_view(['GET'])
@permission_classes([AllowAny])
def resultados_local(request, id_local):
    tipo_eleccion = request.query_params.get('tipo', 'PROVINCIAL')
    resultados = services.obtener_resultados_por_local(id_local, tipo_eleccion)
    return Response(resultados)

@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_matriz(request):
    provincia = request.query_params.get('provincia')
    distrito = request.query_params.get('distrito')
    tipo_eleccion = request.query_params.get('tipo', 'REGIONAL')
    
    matriz_data = services.obtener_matriz_escrutinio(
        provincia=provincia,
        distrito=distrito,
        tipo_eleccion=tipo_eleccion
    )
    return Response(matriz_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def resultados_dashboard(request):
    tipo_eleccion = request.query_params.get('tipo', 'PROVINCIAL')
    modo = request.query_params.get('modo', 'provincial')
    provincia = request.query_params.get('provincia')
    distrito = request.query_params.get('distrito')
    id_local = request.query_params.get('id_local')
    nro_mesa = request.query_params.get('nro_mesa')

    if id_local:
        try:
            id_local = int(id_local)
        except ValueError:
            id_local = None

    resultado = services.obtener_dashboard_resultados(
        tipo_eleccion=tipo_eleccion,
        modo=modo,
        provincia=provincia,
        distrito=distrito,
        id_local=id_local,
        nro_mesa=nro_mesa
    )
    return Response(resultado)




@api_view(['GET'])
@permission_classes([AllowAny])
def cobertura_mesas(request):
    """
    Reporte de cobertura de mesas por local de votacion.
    Indica cuantas mesas faltan por registrar en cada local.

    Query params opcionales:
      - distrito: filtra por nombre de distrito (case-insensitive)
      - id_local: filtra por un local especifico
    """
    distrito = request.query_params.get('distrito')
    id_local = request.query_params.get('id_local')

    if id_local:
        try:
            id_local = int(id_local)
        except ValueError:
            return Response({"error": "id_local debe ser un numero entero."}, status=400)

    resultado = services.cobertura_mesas(
        distrito=distrito,
        id_local=id_local,
    )
    return Response(resultado)