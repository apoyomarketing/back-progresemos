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
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']

class PublicacionSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Publicacion
        fields = [
            'id', 'titulo', 'slug', 'contenido', 'categoria', 'estado',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'slug', 'fecha_creacion', 'fecha_actualizacion']

    def validate(self, data):
        # Ensure title is not empty
        if not data.get('titulo'):
            raise serializers.ValidationError({"titulo": "El título es obligatorio."})
        return data

class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = [
            'id', 'tipo', 'archivo', 'url_externa', 'activo', 'publicacion'
        ]
        read_only_fields = ['id']

class CarruselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrusel
        fields = ['id', 'nombre', 'activo', 'orden', 'multimedia']
        read_only_fields = ['id']

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['id', 'archivo', 'url_externa', 'activo', 'publicacion']
        read_only_fields = ['id']

class ConfiguracionSitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSitio
        fields = ['id', 'clave', 'valor']
        read_only_fields = ['id']
