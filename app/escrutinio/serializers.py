from rest_framework import serializers
from .models import LocalVotacion, Partido, Voto

class LocalVotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVotacion
        fields = '__all__'

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = '__all__'
