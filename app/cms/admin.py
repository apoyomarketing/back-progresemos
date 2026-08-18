from django.contrib import admin

from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
    Propuesta,
    Estadistica,
    Faq,
)


@admin.register(CategoriaPublicacion)
class CategoriaPublicacionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "slug")
    search_fields = ("nombre", "slug")


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "id",
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
        "id",
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
        "id",
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
        "id",
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


@admin.register(Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "eje", "activo", "orden")
    list_filter = ("eje", "activo")
    search_fields = ("titulo", "descripcion")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Estadistica)
class EstadisticaAdmin(admin.ModelAdmin):
    list_display = ("id", "etiqueta", "valor", "prefijo", "sufijo", "activo", "orden")
    list_filter = ("activo",)
    search_fields = ("etiqueta",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta", "activo", "orden")
    list_filter = ("activo",)
    search_fields = ("pregunta", "respuesta")
    readonly_fields = ("created_at", "updated_at")