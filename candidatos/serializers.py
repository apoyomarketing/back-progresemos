from rest_framework import serializers
from .models import Cargo, Candidato


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id_cargo', 'nombre']


class CandidatoSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer(read_only=True)
    cargo_id = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.all(), source='cargo', write_only=True
    )

    class Meta:
        model = Candidato
        fields = [
            'id_candidato',
            'nombre',
            'apellido',
            'cargo',
            'cargo_id',
            'foto',
            'biografia',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
