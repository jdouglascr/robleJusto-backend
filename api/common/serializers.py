from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Empresa, Agricultor, Chofer, Maquinaria, Transporte

Usuario = get_user_model()
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'rol', 'password', 'last_login']
        read_only_fields = ['last_login']

    def create(self, validated_data):
        usuario = Usuario(
            username=validated_data['username'],
            nombre=validated_data['nombre'],
            rol=validated_data['rol']
        )
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = '__all__'

class AgricultorSerializer(serializers.ModelSerializer):
    empresa = serializers.CharField(source='empresa_id.nombre', read_only=True)

    class Meta:
        model = Agricultor
        fields = ['id', 'rut', 'nombre', 'direccion', 'telefono', 'empresa', 'empresa_id']
        extra_kwargs = {
            'empresa_id': {'write_only': True}
        }

class ChoferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chofer
        fields = '__all__'

class MaquinariaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maquinaria
        fields = '__all__'

class TransporteSerializer(serializers.ModelSerializer):
    empresa = serializers.CharField(source='empresa_id.nombre', read_only=True)
    agricultor = serializers.CharField(source='agricultor_id.nombre', read_only=True)
    patente_maquinaria = serializers.CharField(source='maquinaria_id.patente', read_only=True)
    tipo_maquinaria = serializers.CharField(source='maquinaria_id.tipo', read_only=True)
    chofer = serializers.CharField(source='chofer_id.nombre', read_only=True)
    usuario = serializers.CharField(source='usuario_id.nombre', read_only=True)

    class Meta:
        model = Transporte
        fields = ['id','fecha_transporte', 'empresa', 'agricultor', 'origen', 'destino', 'distancia', 'precio', 'patente_maquinaria', 'tipo_maquinaria', 'chofer', 'usuario', 'empresa_id', 'agricultor_id', 'maquinaria_id', 'chofer_id', 'usuario_id', 'estado']
        extra_kwargs = {
            'empresa_id': {'write_only': True},
            'agricultor_id': {'write_only': True},
            'chofer_id': {'write_only': True},
            'usuario_id': {'write_only': True},
            'maquinaria_id': {'write_only': True}
        }

class CrearJiraIssueSerializer(serializers.Serializer):
    issue_type = serializers.CharField(max_length=50)
    summary = serializers.CharField(max_length=200)
    description = serializers.CharField()

class AdjuntarArchivoJiraSerializer(serializers.Serializer):
    file = serializers.FileField()