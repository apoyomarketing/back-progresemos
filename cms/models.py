from django.db import models
from django.utils.text import slugify


class CategoriaPublicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'categorias_publicacion'
        verbose_name = 'Categoría de Publicación'
        verbose_name_plural = 'Categorías de Publicación'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    contenido = models.TextField()
    categoria = models.ForeignKey(CategoriaPublicacion, on_delete=models.PROTECT, related_name='publicaciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'publicaciones'
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)


class Multimedia(models.Model):
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='multimedia/')
    url_externa = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='multimedias', null=True, blank=True)

    class Meta:
        db_table = 'multimedia'
        verbose_name = 'Multimedia'
        verbose_name_plural = 'Multimedia'
        ordering = ['-id']

    def __str__(self):
        return f"{self.tipo} - {self.archivo.name}"


class Carrusel(models.Model):
    nombre = models.CharField(max_length=100)
    multimedia = models.ManyToManyField(Multimedia, related_name='carruseles')
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'carruseles'
        verbose_name = 'Carrusel'
        verbose_name_plural = 'Carruseles'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    archivo = models.FileField(upload_to='documentos/')
    url_externa = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='documentos')

    class Meta:
        db_table = 'documentos'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-id']

    def __str__(self):
        return self.archivo.name


class ConfiguracionSitio(models.Model):
    clave = models.CharField(max_length=100, unique=True)
    valor = models.CharField(max_length=255)

    class Meta:
        db_table = 'configuracion_sitio'
        verbose_name = 'Configuración del Sitio'
        verbose_name_plural = 'Configuraciones del Sitio'

    def __str__(self):
        return f"{self.clave} = {self.valor}"

