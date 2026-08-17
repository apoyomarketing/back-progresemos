from rest_framework import serializers
from .models import Cargo, Candidato


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = [
            "id_cargo",
            "nombre",
        ]


class CandidatoSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer(read_only=True)

    id_cargo = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.all(),
        source="cargo",
        write_only=True
    )

    class Meta:
        model = Candidato
        fields = [
            "id_candidato",
            "id_cargo",
            "cargo",
            "nombres",
            "apellido_paterno",
            "apellido_materno",
            "foto",
            "descripcion",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id_candidato",
            "created_at",
            "updated_at",
        ]