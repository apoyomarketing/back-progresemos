from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from app.core.models import TimeStampedModel
from app.core.utils import unique_slugify


class CategoriaPublicacion(TimeStampedModel):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table = "categorias_publicacion"
        ordering = ["nombre"]
        verbose_name = "Categoría de publicación"
        verbose_name_plural = "Categorías de publicación"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.nombre, max_length=120)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Publicacion(TimeStampedModel):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"

    categoria = models.ForeignKey(
        CategoriaPublicacion,
        on_delete=models.PROTECT,
        related_name="publicaciones",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="publicaciones",
    )

    titulo = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    resumen = models.TextField(blank=True)
    contenido = models.TextField()

    imagen_portada = models.ImageField(
        upload_to="publicaciones/portadas/",
        null=True,
        blank=True
    )

    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.BORRADOR)

    class Meta:
        db_table = "publicaciones"
        ordering = ["-created_at"]
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        indexes = [
            models.Index(fields=["estado", "-fecha_publicacion"], name="pub_estado_fecha_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.titulo, max_length=255)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Multimedia(TimeStampedModel):
    class Tipo(models.TextChoices):
        IMAGEN = "imagen", "Imagen"
        VIDEO = "video", "Video"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="multimedia",
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)

    tipo = models.CharField(max_length=30, choices=Tipo.choices)

    archivo = models.FileField(
        upload_to="multimedia/",
        null=True,
        blank=True
    )

    url_externa = models.URLField(max_length=500, null=True, blank=True)

    miniatura = models.ImageField(
        upload_to="multimedia/miniaturas/",
        null=True,
        blank=True
    )

    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "multimedia"
        ordering = ["orden", "-created_at"]
        verbose_name = "Multimedia"
        verbose_name_plural = "Multimedia"

    def __str__(self):
        return self.titulo or f"{self.tipo} #{self.pk}"


class Carrusel(TimeStampedModel):
    titulo = models.CharField(max_length=255, blank=True)
    subtitulo = models.CharField(max_length=255, blank=True)

    imagen = models.ImageField(upload_to="carrusel/")

    texto_boton = models.CharField(max_length=100, blank=True)
    url_boton = models.URLField(max_length=500, blank=True)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "carrusel"
        ordering = ["orden"]
        verbose_name = "Carrusel"
        verbose_name_plural = "Carrusel"

    def __str__(self):
        return self.titulo or f"Carrusel #{self.pk}"


class Documento(TimeStampedModel):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="documentos",
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)

    archivo = models.FileField(upload_to="documentos/")
    tipo_archivo = models.CharField(max_length=50, blank=True)

    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "documentos"
        ordering = ["-created_at"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.titulo


class ConfiguracionSitio(TimeStampedModel):
    nombre_partido = models.CharField(max_length=255)
    siglas = models.CharField(max_length=50, blank=True)

    logo = models.ImageField(
        upload_to="configuracion/",
        null=True,
        blank=True
    )

    favicon = models.ImageField(
        upload_to="configuracion/",
        null=True,
        blank=True
    )

    descripcion = models.TextField(blank=True)

    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(max_length=150, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    facebook = models.URLField(max_length=500, blank=True)
    instagram = models.URLField(max_length=500, blank=True)
    tiktok = models.URLField(max_length=500, blank=True)
    youtube = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = "configuracion_sitio"
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def clean(self):
        if self._state.adding and ConfiguracionSitio.objects.exists():
            raise ValidationError(
                "La configuración del sitio ya existe. "
                "Utilice el registro existente para modificarla."
            )

    def save(self, *args, **kwargs):
        if self._state.adding and ConfiguracionSitio.objects.exists():
            raise ValidationError(
                "La configuración del sitio ya existe. "
                "Utilice el registro existente para modificarla."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_partido


class Propuesta(TimeStampedModel):
    class Eje(models.TextChoices):
        EDUCACION = "educacion", "Educación"
        SALUD = "salud", "Salud"
        SEGURIDAD = "seguridad", "Seguridad"
        ECONOMIA = "economia", "Economía"
        INFRAESTRUCTURA = "infraestructura", "Infraestructura"
        AGRICULTURA = "agricultura", "Agricultura"
        INNOVACION = "innovacion", "Innovación"
        DESARROLLO_REGIONAL = "desarrollo_regional", "Desarrollo Regional"

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)

    imagen = models.ImageField(
        upload_to="propuestas/",
        null=True,
        blank=True
    )

    eje = models.CharField(max_length=30, choices=Eje.choices)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "propuestas"
        ordering = ["orden", "-created_at"]
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return self.titulo


class Estadistica(TimeStampedModel):
    etiqueta = models.CharField(max_length=100)
    valor = models.PositiveIntegerField()

    prefijo = models.CharField(max_length=10, blank=True)
    sufijo = models.CharField(max_length=20, blank=True)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "estadisticas"
        ordering = ["orden"]
        verbose_name = "Estadística"
        verbose_name_plural = "Estadísticas"

    def __str__(self):
        return self.etiqueta


class Faq(TimeStampedModel):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "faqs"
        ordering = ["orden"]
        verbose_name = "Pregunta frecuente"
        verbose_name_plural = "Preguntas frecuentes"

    def __str__(self):
        return self.pregunta
