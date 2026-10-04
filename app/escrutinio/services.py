from django.db.models import Sum, F, Count, Q
from django.db import transaction
from .models import Voto, LocalVotacion, Partido


def validate_nro_mesa_unico(nro_mesa, tipo_eleccion, id_local_actual=None):
    """
    Valida que el número de mesa no esté ya registrado en otro local,
    independientemente del tipo de elección.
    Un número de mesa es físicamente único: pertenece a un solo local.
    Si se pasa id_local_actual, permite que la mesa ya exista en ESE local
    (registrar los 4 tipos de elección para la misma mesa del mismo local está permitido).
    """
    qs = Voto.objects.filter(nro_mesa=str(nro_mesa))
    if id_local_actual is not None:
        qs = qs.exclude(local_id=id_local_actual)
    if qs.exists():
        otro_local = qs.values_list('local__nombre_local', 'local__id_local').first()
        raise ValueError(
            f"El número de mesa '{nro_mesa}' ya está registrado en el local "
            f"'{otro_local[0]}' (id: {otro_local[1]}). "
            f"Los números de mesa son únicos a nivel global (independiente del tipo de elección)."
        )

def registrar_votos_mesa(id_local, nro_mesa, tipo_eleccion, datos_votos):
    """
    Registra los votos de una mesa específica.
    `tipo_eleccion` es 'REGIONAL', 'CONSEJERO', 'PROVINCIAL' o 'DISTRITAL'
    `datos_votos` es una lista de diccionarios: [{'id_partido': 1, 'cant_voto': 150}, ...]
    """
    with transaction.atomic():
        local = LocalVotacion.objects.get(id_local=id_local)
        
        # Validar que el número de mesa no esté repetido en otro local
        validate_nro_mesa_unico(nro_mesa, tipo_eleccion, id_local_actual=id_local)
        
        # Calcular el límite de votos según el tipo de elección
        if tipo_eleccion == 'DISTRITAL':
            limite_votos = local.electores_municipal
        else:
            limite_votos = local.electores_regional
            
        # Obtener los votos actuales del local para esta elección, excluyendo la mesa actual (para sobreescribirla en el cálculo)
        total_actual = Voto.objects.filter(
            local=local, 
            tipo_eleccion=tipo_eleccion
        ).exclude(
            nro_mesa=nro_mesa
        ).aggregate(total=Sum('cant_voto'))['total'] or 0
        
        # Calcular los nuevos votos a ingresar para esta mesa
        nuevos_votos_mesa = sum(int(dato.get('cant_voto', 0)) for dato in datos_votos)
        
        if total_actual + nuevos_votos_mesa > limite_votos:
            raise ValueError(f"La cantidad total de votos ({total_actual + nuevos_votos_mesa}) excede la cantidad de electores admitidos ({limite_votos}) para este local.")
        
        # Validar y crear/actualizar cada voto
        votos_creados = []
        for dato in datos_votos:
            partido = Partido.objects.get(id_partido=dato['id_partido'])
            voto, created = Voto.objects.update_or_create(
                local=local,
                nro_mesa=nro_mesa,
                tipo_eleccion=tipo_eleccion,
                partido=partido,
                defaults={'cant_voto': dato['cant_voto']}
            )
            votos_creados.append(voto)
            
        return votos_creados

def obtener_resultados_provinciales(provincia, tipo_eleccion):
    """
    Obtiene el total de votos por partido a nivel provincial para un tipo de elección.
    """
    resultados = Voto.objects.filter(
        local__provincia=provincia,
        tipo_eleccion=tipo_eleccion
    ).values(
        'partido__nombre_partido'
    ).annotate(
        total_votos=Sum('cant_voto')
    ).order_by('-total_votos')
    
    return list(resultados)

def obtener_resultados_distritales(distrito, tipo_eleccion):
    """
    Obtiene el total de votos por partido a nivel distrital para un tipo de elección.
    """
    resultados = Voto.objects.filter(
        local__distrito=distrito,
        tipo_eleccion=tipo_eleccion
    ).values(
        'partido__nombre_partido'
    ).annotate(
        total_votos=Sum('cant_voto')
    ).order_by('-total_votos')
    
    return list(resultados)

def obtener_resultados_por_local(id_local, tipo_eleccion):
    """
    Total de votos por local, replicando la vista SQL `vista_votos_por_local`
    """
    resultados = Voto.objects.filter(
        local_id=id_local,
        tipo_eleccion=tipo_eleccion
    ).values(
        'partido__nombre_partido'
    ).annotate(
        total_votos=Sum('cant_voto')
    ).order_by('-total_votos')
    
    # También podemos devolver total emitido general
    total_emitido = sum(r['total_votos'] for r in resultados) if resultados else 0
    
    local = LocalVotacion.objects.get(id_local=id_local)
    electores = local.electores_municipal if tipo_eleccion == 'DISTRITAL' else local.electores_regional
    
    pct_participacion = (total_emitido * 100.0 / electores) if electores > 0 else 0

    return {
        'resultados_partidos': list(resultados),
        'total_emitido': total_emitido,
        'electores_habiles': electores,
        'pct_participacion': round(pct_participacion, 2)
    }

def obtener_matriz_escrutinio(provincia=None, distrito=None, tipo_eleccion='REGIONAL'):
    """
    Construye la matriz consolidada de actas registradas por mesa y colegio de votación.
    Solo devuelve filas y columnas para las mesas y partidos con votos digitados.
    """
    votos_qs = Voto.objects.filter(tipo_eleccion=tipo_eleccion).select_related('local', 'partido')
    
    if provincia:
        votos_qs = votos_qs.filter(local__provincia__iexact=provincia)
    if distrito:
        votos_qs = votos_qs.filter(local__distrito__iexact=distrito)

    mesas_dict = {}
    partidos_set = set()
    totales_partidos = {}
    gran_total_votos = 0

    for voto in votos_qs.order_by('local__id_local', 'nro_mesa', 'partido__id_partido'):
        key = (voto.local.id_local, str(voto.nro_mesa))
        partido_nombre = voto.partido.nombre_partido
        
        partidos_set.add(partido_nombre)
        
        if key not in mesas_dict:
            nro_m = int(voto.nro_mesa) if (isinstance(voto.nro_mesa, str) and voto.nro_mesa.isdigit()) else voto.nro_mesa
            mesas_dict[key] = {
                "id_local": voto.local.id_local,
                "provincia": voto.local.provincia,
                "distrito": voto.local.distrito,
                "nombre_local": voto.local.nombre_local,
                "direccion_local": voto.local.direccion_local or "",
                "nro_mesa": nro_m,
                "votos_partidos": {},
                "total_votos": 0
            }
        
        cant = voto.cant_voto
        mesas_dict[key]["votos_partidos"][partido_nombre] = cant
        mesas_dict[key]["total_votos"] += cant
        
        totales_partidos[partido_nombre] = totales_partidos.get(partido_nombre, 0) + cant
        gran_total_votos += cant

    partidos_ordenados = sorted(partidos_set, key=lambda p: totales_partidos.get(p, 0), reverse=True)

    matriz = []
    for mesa_info in mesas_dict.values():
        votos_completos = {p: mesa_info["votos_partidos"].get(p, 0) for p in partidos_ordenados}
        mesa_info["votos_partidos"] = votos_completos
        matriz.append(mesa_info)

    return {
        "tipo_eleccion": tipo_eleccion,
        "partidos": partidos_ordenados,
        "matriz": matriz,
        "totales_partidos": {p: totales_partidos.get(p, 0) for p in partidos_ordenados},
        "gran_total_votos": gran_total_votos
    }

def obtener_dashboard_resultados(tipo_eleccion='PROVINCIAL', modo='provincial', provincia=None, distrito=None, id_local=None, nro_mesa=None):
    """
    Obtiene los resultados consolidados para el Dashboard de Escrutinio según el modo y filtros.
    """
    votos_qs = Voto.objects.filter(tipo_eleccion=tipo_eleccion)
    locales_qs = LocalVotacion.objects.all()

    if modo == 'mesa':
        if id_local:
            votos_qs = votos_qs.filter(local_id=id_local)
            locales_qs = locales_qs.filter(id_local=id_local)
        if nro_mesa:
            votos_qs = votos_qs.filter(nro_mesa=str(nro_mesa))
    elif modo == 'local':
        if id_local:
            votos_qs = votos_qs.filter(local_id=id_local)
            locales_qs = locales_qs.filter(id_local=id_local)
    elif modo == 'distrito':
        if provincia:
            votos_qs = votos_qs.filter(local__provincia__iexact=provincia)
            locales_qs = locales_qs.filter(provincia__iexact=provincia)
        if distrito:
            votos_qs = votos_qs.filter(local__distrito__iexact=distrito)
            locales_qs = locales_qs.filter(distrito__iexact=distrito)
    else: # provincial
        p = provincia or 'PUNO'
        votos_qs = votos_qs.filter(local__provincia__iexact=p)
        locales_qs = locales_qs.filter(provincia__iexact=p)

    campo_electores = 'electores_municipal' if tipo_eleccion == 'DISTRITAL' else 'electores_regional'
    electores_habiles = locales_qs.aggregate(total=Sum(campo_electores))['total'] or 0

    partidos_agg = votos_qs.values('partido__nombre_partido').annotate(
        total_votos=Sum('cant_voto')
    ).order_by('-total_votos')

    total_emitido = sum(p['total_votos'] for p in partidos_agg) if partidos_agg else 0

    resultados_partidos = []
    for p in partidos_agg:
        cant = p['total_votos']
        pct = round((cant * 100.0 / total_emitido), 2) if total_emitido > 0 else 0.0
        resultados_partidos.append({
            "nombre_partido": p['partido__nombre_partido'],
            "total_votos": cant,
            "porcentaje": pct
        })

    partido_lider = resultados_partidos[0] if resultados_partidos else None
    pct_participacion = round((total_emitido * 100.0 / electores_habiles), 2) if electores_habiles > 0 else 0.0

    res = {
        "modo": modo,
        "tipo_eleccion": tipo_eleccion,
        "total_emitido": total_emitido,
        "electores_habiles": electores_habiles,
        "pct_participacion": pct_participacion,
        "partido_lider": partido_lider,
        "resultados_partidos": resultados_partidos
    }

    if provincia:
        res["provincia"] = provincia
    elif modo in ['provincial', 'distrito']:
        res["provincia"] = 'PUNO'

    if distrito or modo == 'distrito':
        res["distrito"] = distrito

    if id_local or modo == 'local':
        res["id_local"] = id_local

    if nro_mesa or modo == 'mesa':
        res["nro_mesa"] = nro_mesa

    return res


def cobertura_mesas(distrito=None, id_local=None):
    """
    Retorna el estado de cobertura de mesas por local de votación.
    Para cada local muestra:
      - Total de mesas esperadas (cant_mesas del local).
      - Mesas ya registradas en el sistema (con al menos un voto digitado).
      - Mesas faltantes por llenar.
    Acepta filtros opcionales por `distrito` y/o `id_local`.
    """
    locales_qs = LocalVotacion.objects.all()

    if distrito:
        locales_qs = locales_qs.filter(distrito__iexact=distrito)
    if id_local:
        locales_qs = locales_qs.filter(id_local=id_local)

    locales_qs = locales_qs.order_by('distrito', 'nombre_local')

    resultado = []
    total_mesas_esperadas = 0
    total_mesas_registradas = 0

    for local in locales_qs:
        mesas_registradas = (
            Voto.objects
            .filter(local=local)
            .values('nro_mesa')
            .distinct()
            .count()
        )
        mesas_esperadas = local.cant_mesas
        mesas_faltantes = max(mesas_esperadas - mesas_registradas, 0)

        total_mesas_esperadas += mesas_esperadas
        total_mesas_registradas += mesas_registradas

        resultado.append({
            'id_local': local.id_local,
            'nombre_local': local.nombre_local,
            'direccion': local.direccion_local or '',
            'distrito': local.distrito,
            'provincia': local.provincia,
            'mesas_esperadas': mesas_esperadas,
            'mesas_registradas': mesas_registradas,
            'mesas_faltantes': mesas_faltantes,
            'pct_cobertura': round(
                (mesas_registradas * 100.0 / mesas_esperadas), 2
            ) if mesas_esperadas > 0 else 0.0,
        })

    return {
        'filtros': {
            'distrito': distrito,
            'id_local': id_local,
        },
        'resumen': {
            'total_locales': len(resultado),
            'total_mesas_esperadas': total_mesas_esperadas,
            'total_mesas_registradas': total_mesas_registradas,
            'total_mesas_faltantes': max(total_mesas_esperadas - total_mesas_registradas, 0),
            'pct_cobertura_global': round(
                (total_mesas_registradas * 100.0 / total_mesas_esperadas), 2
            ) if total_mesas_esperadas > 0 else 0.0,
        },
        'locales': resultado,
    }
