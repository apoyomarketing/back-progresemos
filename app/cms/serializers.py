from rest_framework import serializers

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


class CategoriaPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaPublicacion
        fields = [
            "id",
            "nombre",
            "slug",
        ]
        read_only_fields = ["id", "slug"]


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
            "id",
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
            "id",
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
            "id",
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
            "id",
            "usuario",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        archivo = attrs.get("archivo", getattr(self.instance, "archivo", None))
        url_externa = attrs.get("url_externa", getattr(self.instance, "url_externa", None))

        if not archivo and not url_externa:
            raise serializers.ValidationError(
                "Debe proporcionar un archivo o una URL externa."
            )

        return attrs


class CarruselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrusel
        fields = [
            "id",
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
            "id",
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
            "id",
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
            "id",
            "usuario",
            "created_at",
            "updated_at",
        ]


class ConfiguracionSitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSitio
        fields = [
            "id",
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
            "id",
            "created_at",
            "updated_at",
        ]


class PropuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propuesta
        fields = [
            "id",
            "titulo",
            "descripcion",
            "imagen",
            "eje",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class EstadisticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadistica
        fields = [
            "id",
            "etiqueta",
            "valor",
            "prefijo",
            "sufijo",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = [
            "id",
            "pregunta",
            "respuesta",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
