from rest_framework import serializers
from .models import Rol, Usuario


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = [
            "id",
            "nombre",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    rol_nombre = serializers.CharField(
        source="rol.nombre",
        read_only=True
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "rol",
            "rol_nombre",
            "nombre",
            "email",
            "password",
            "estado",
            "is_staff",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({
                "password": "La contraseña es obligatoria."
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        usuario = Usuario.objects.create_user(
            email=validated_data.pop("email"),
            nombre=validated_data.pop("nombre"),
            password=password,
            **validated_data
        )

        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance