from django.core.validators import RegexValidator
from django.db import connection, models

from app.core.models import TimeStampedModel

from .config import CODIGO_INICIO

validador_dni = RegexValidator(r"^\d{8}$", "El DNI debe tener 8 dígitos.")
validador_celular = RegexValidator(
    r"^9\d{8}$", "El celular debe tener 9 dígitos y empezar con 9."
)

SECUENCIA_CODIGO = "voluntarios_codigo_seq"


def _rol_afiliado_default():
    from app.asistencia.models import RolAfiliado

    return RolAfiliado.objects.get(rol_name=RolAfiliado.AFILIADO).pk


def generar_codigo() -> str:
    """
    Devuelve el siguiente código correlativo: PRG-0001, PRG-0002, …

    Usa una secuencia de PostgreSQL en vez de contar filas. nextval() nunca
    entrega el mismo número dos veces, ni siquiera con varios workers
    insertando a la vez, así que no hay carreras ni colisiones.

    Puede haber huecos si una inserción falla después de pedir el número.
    Es normal y no rompe nada: el código identifica, no cuenta.

    A partir de 10000 el código crece solo a PRG-10000, sin romper el formato.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT nextval('{SECUENCIA_CODIGO}')")
        numero = cursor.fetchone()[0]
    return f"PRG-{numero + CODIGO_INICIO:04d}"


class Voluntario(TimeStampedModel):
    """Preinscripción confirmada. Una fila por persona."""

    PREINSCRITO = "preinscrito"
    CONFIRMADO = "confirmado"
    BAJA = "baja"
    ESTADOS = [
        (PREINSCRITO, "Preinscrito"),
        (CONFIRMADO, "Confirmado"),
        (BAJA, "Baja"),
    ]

    codigo = models.CharField(max_length=12, unique=True, editable=False)
    dni = models.CharField(max_length=8, unique=True, validators=[validador_dni])
    nombres = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80, blank=True)
    nombre_completo = models.CharField(max_length=255)
    celular = models.CharField(max_length=9, validators=[validador_celular])
    acepta_whatsapp = models.BooleanField(default=False)
    foto = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    rol_afiliado = models.ForeignKey(
        "asistencia.RolAfiliado",
        db_column="id_rol_afiliado",
        on_delete=models.PROTECT,
        default=_rol_afiliado_default,
        related_name="voluntarios",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PREINSCRITO)
    origen = models.CharField(max_length=40, default="web_unete")
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        db_table = "voluntarios"
        ordering = ["-created_at"]
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"
        indexes = [
            models.Index(fields=["-created_at"], name="voluntario_creado_idx"),
            models.Index(fields=["estado"], name="voluntario_estado_idx"),
        ]

    def __str__(self):
        return f"{self.dni} — {self.nombre_completo}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = generar_codigo()
        super().save(*args, **kwargs)


class ConsultaReniec(TimeStampedModel):
    """
    Caché compartida de consultas a Decolecta.

    Va en tabla y no en la caché de Django porque LocMemCache vive en la
    memoria de CADA worker de gunicorn: el worker A guarda el dato y el
    worker B lo vuelve a consultar, gastando otro crédito.

    Efecto sobre el límite de la API: el paso 2 (validar) y el paso 3
    (confirmar) del mismo usuario cuestan UNA consulta, no dos.
    """

    dni = models.CharField(max_length=8, primary_key=True)
    nombres = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80, blank=True)
    nombre_completo = models.CharField(max_length=255)

    class Meta:
        db_table = "voluntarios_consulta_reniec"
        verbose_name = "Consulta a RENIEC"
        verbose_name_plural = "Consultas a RENIEC"
        indexes = [models.Index(fields=["updated_at"], name="reniec_consultado_idx")]

    def como_dict(self):
        return {
            "dni": self.dni,
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "nombre_completo": self.nombre_completo,
        }


class LimitadorApi(models.Model):
    """
    Cubeta de fichas compartida por todos los procesos vía base de datos.

    La cubeta se rellena sola a `tasa` fichas por segundo hasta el tope de
    `capacidad`. Cada consulta a Decolecta toma una ficha.

    CALIBRACIÓN (medida con prueba de carga, no estimada):
      capacidad = 3  -> ráfaga máxima acumulable
      tasa      = 6  -> consultas por segundo sostenidas

    El peor caso es capacidad + tasa en un mismo segundo: 3 + 6 = 9, con 1
    de margen bajo el tope de 10/s de Decolecta. Con capacidad 8 y tasa 8
    la peor ráfaga medida fue 16 consultas en un segundo, que dispara 429.

    REGLA AL CALIBRAR: capacidad + tasa < tope de la API.
    Se cambia en caliente desde el admin, sin redesplegar.
    """

    clave = models.CharField(max_length=40, primary_key=True)
    tokens = models.FloatField(default=3.0)
    capacidad = models.FloatField(default=3.0, help_text="Ráfaga máxima")
    tasa = models.FloatField(default=6.0, help_text="Fichas por segundo (sostenido)")
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "voluntarios_limitador_api"
        verbose_name = "Limitador de API"
        verbose_name_plural = "Limitadores de API"

    def __str__(self):
        return f"{self.clave}: {self.tasa}/s"
