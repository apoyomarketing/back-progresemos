"""
Comprobaciones que corren con `manage.py check` y en cada despliegue.

El limitador de caudal depende de que las peticiones NO estén envueltas en
una transacción global. Si lo estuvieran, el candado de la fila del limitador
se retendría durante toda la petición (incluida la llamada HTTP a Decolecta)
y los registros se atenderían de uno en uno.

Medido: con ATOMIC_REQUESTS=True un segundo worker espera 1.7 s por una ficha
que debería obtener al instante.
"""
from django.core.checks import Error, register


@register()
def comprobar_atomic_requests(app_configs, **kwargs):
    from django.conf import settings

    problemas = []
    for alias, config in settings.DATABASES.items():
        if config.get("ATOMIC_REQUESTS"):
            problemas.append(
                Error(
                    f"La base '{alias}' tiene ATOMIC_REQUESTS=True.",
                    hint=(
                        "El limitador de Decolecta retendría el candado durante "
                        "toda la petición y serializaría los registros. Ponlo en "
                        "False, o envuelve solo las vistas que lo necesiten con "
                        "@transaction.atomic."
                    ),
                    id="voluntarios.E001",
                )
            )
    return problemas
