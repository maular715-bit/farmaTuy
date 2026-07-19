from rest_framework import serializers
from .models import Farmacia, Medicamento, InventarioFarmacia, Tipo, Usuario, AuthUsuario


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'


class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioFarmacia
        fields = '__all__'


class AuthUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUsuario
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nombre_primero = serializers.CharField(max_length=255, required=False, allow_blank=True)
    apellido_paterno = serializers.CharField(max_length=255, required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserPublicSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
