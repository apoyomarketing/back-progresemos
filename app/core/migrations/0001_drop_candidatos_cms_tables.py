from django.db import migrations

# app.candidatos y app.cms se eliminaron del proyecto; esta migración borra
# sus tablas (si existen) en cualquier base donde hayan llegado a crearse.
DROP_TABLES_SQL = """
DROP TABLE IF EXISTS
    multimedia,
    carrusel,
    documentos,
    configuracion_sitio,
    propuestas,
    estadisticas,
    faqs,
    publicaciones,
    categorias_publicacion,
    candidatos,
    cargos
CASCADE;
"""


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql=DROP_TABLES_SQL,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
