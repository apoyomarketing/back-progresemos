from django.contrib import admin
from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
)

@admin.register(CategoriaPublicacion)
class CategoriaPublicacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'slug', 'categoria', 'estado', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')
    list_filter = ('estado', 'categoria')
    prepopulated_fields = {'slug': ('titulo',)}

@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'archivo', 'url_externa', 'activo', 'publicacion')
    search_fields = ('tipo',)
    list_filter = ('activo', 'tipo')

@admin.register(Carrusel)
class CarruselAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo', 'orden')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    ordering = ('orden',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'archivo', 'url_externa', 'activo', 'publicacion')
    search_fields = ('archivo',)
    list_filter = ('activo',)

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave', 'valor')
    search_fields = ('clave',)
    list_filter = ('clave',)
