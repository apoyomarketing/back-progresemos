from django.conf import settings
from django.db import models
from django.utils.text import slugify


class CategoriaPublicacion(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table = "categorias_publicacion"
        ordering = ["nombre"]
        verbose_name = "Categoría de publicación"
        verbose_name_plural = "Categorías de publicación"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    ESTADO_CHOICES = [
        ("borrador", "Borrador"),
        ("publicado", "Publicado"),
    ]

    id_publicacion = models.AutoField(primary_key=True)

    categoria = models.ForeignKey(
        CategoriaPublicacion,
        on_delete=models.PROTECT,
        related_name="publicaciones",
        db_column="id_categoria"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="publicaciones",
        db_column="id_usuario"
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
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default="borrador")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "publicaciones"
        ordering = ["-created_at"]
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Multimedia(models.Model):
    TIPO_CHOICES = [
        ("imagen", "Imagen"),
        ("video", "Video"),
    ]

    id_multimedia = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="multimedia",
        db_column="id_usuario",
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)

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
    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "multimedia"
        ordering = ["orden", "-created_at"]
        verbose_name = "Multimedia"
        verbose_name_plural = "Multimedia"

    def __str__(self):
        return self.titulo or f"{self.tipo} #{self.id_multimedia}"


class Carrusel(models.Model):
    id_carrusel = models.AutoField(primary_key=True)

    titulo = models.CharField(max_length=255, blank=True)
    subtitulo = models.CharField(max_length=255, blank=True)

    imagen = models.ImageField(upload_to="carrusel/")

    texto_boton = models.CharField(max_length=100, blank=True)
    url_boton = models.URLField(max_length=500, blank=True)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carrusel"
        ordering = ["orden"]
        verbose_name = "Carrusel"
        verbose_name_plural = "Carrusel"

    def __str__(self):
        return self.titulo or f"Carrusel #{self.id_carrusel}"


class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="documentos",
        db_column="id_usuario",
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)

    archivo = models.FileField(upload_to="documentos/")
    tipo_archivo = models.CharField(max_length=50, blank=True)

    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documentos"
        ordering = ["-created_at"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.titulo


class ConfiguracionSitio(models.Model):
    id_configuracion = models.AutoField(primary_key=True)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "configuracion_sitio"
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return self.nombre_partido