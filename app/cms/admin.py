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
    list_display = ("id_categoria", "nombre", "slug")
    search_fields = ("nombre", "slug")


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
        "id_publicacion",
        "titulo",
        "categoria",
        "usuario",
        "estado",
        "fecha_publicacion",
        "created_at",
    )

    list_filter = (
        "estado",
        "categoria",
    )

    search_fields = (
        "titulo",
        "slug",
        "resumen",
        "contenido",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = (
        "id_multimedia",
        "titulo",
        "tipo",
        "usuario",
        "activo",
        "orden",
        "fecha_publicacion",
    )

    list_filter = (
        "tipo",
        "activo",
    )

    search_fields = (
        "titulo",
        "descripcion",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Carrusel)
class CarruselAdmin(admin.ModelAdmin):
    list_display = (
        "id_carrusel",
        "titulo",
        "orden",
        "activo",
        "created_at",
    )

    list_filter = ("activo",)

    search_fields = (
        "titulo",
        "subtitulo",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        "id_documento",
        "titulo",
        "usuario",
        "tipo_archivo",
        "activo",
        "fecha_publicacion",
        "created_at",
    )

    list_filter = (
        "activo",
        "tipo_archivo",
    )

    search_fields = (
        "titulo",
        "descripcion",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = (
        "id_configuracion",
        "nombre_partido",
        "siglas",
        "correo",
        "telefono",
        "updated_at",
    )

    search_fields = (
        "nombre_partido",
        "siglas",
        "correo",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )