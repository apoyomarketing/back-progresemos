from rest_framework import serializers

from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
)


class CategoriaPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaPublicacion
        fields = [
            "id_categoria",
            "nombre",
            "slug",
        ]
        read_only_fields = ["id_categoria", "slug"]


class PublicacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source="usuario.nombre",
        read_only=True
    )

    categoria_nombre = serializers.CharField(
        source="categoria.nombre",
        read_only=True
    )

    class Meta:
        model = Publicacion
        fields = [
            "id_publicacion",
            "categoria",
            "categoria_nombre",
            "usuario",
            "usuario_nombre",
            "titulo",
            "slug",
            "resumen",
            "contenido",
            "imagen_portada",
            "fecha_publicacion",
            "estado",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_publicacion",
            "usuario",
            "slug",
            "created_at",
            "updated_at",
        ]


class MultimediaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source="usuario.nombre",
        read_only=True
    )

    class Meta:
        model = Multimedia
        fields = [
            "id_multimedia",
            "usuario",
            "usuario_nombre",
            "titulo",
            "descripcion",
            "tipo",
            "archivo",
            "url_externa",
            "miniatura",
            "fecha_publicacion",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_multimedia",
            "usuario",
            "created_at",
            "updated_at",
        ]


class CarruselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrusel
        fields = [
            "id_carrusel",
            "titulo",
            "subtitulo",
            "imagen",
            "texto_boton",
            "url_boton",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_carrusel",
            "created_at",
            "updated_at",
        ]


class DocumentoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source="usuario.nombre",
        read_only=True
    )

    class Meta:
        model = Documento
        fields = [
            "id_documento",
            "usuario",
            "usuario_nombre",
            "titulo",
            "descripcion",
            "archivo",
            "tipo_archivo",
            "fecha_publicacion",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_documento",
            "usuario",
            "created_at",
            "updated_at",
        ]


class ConfiguracionSitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSitio
        fields = [
            "id_configuracion",
            "nombre_partido",
            "siglas",
            "logo",
            "favicon",
            "descripcion",
            "telefono",
            "correo",
            "direccion",
            "facebook",
            "instagram",
            "tiktok",
            "youtube",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_configuracion",
            "created_at",
            "updated_at",
        ]