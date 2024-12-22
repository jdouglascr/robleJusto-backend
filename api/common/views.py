from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from api.common.serializers import CrearJiraIssueSerializer, UsuarioSerializer
from django.contrib.auth import get_user_model
from api.common.serializers import EmpresaSerializer, AgricultorSerializer, ChoferSerializer, MaquinariaSerializer, TransporteSerializer
from api.models import Empresa, Agricultor, Chofer, Maquinaria, Transporte, JiraAPI, Usuario
from django.utils.timezone import now
import time

class RegistroUsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            username = request.data.get('username')
            if Usuario.objects.filter(username=username).exists():
                return Response({'message': f'El Usuario {username} ya está registrado.'},status=status.HTTP_400_BAD_REQUEST)

            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.save()
                return Response({'message': f'Usuario {usuario.nombre} registrado correctamente'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUsuarioAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                usuario.last_login = now()
                usuario.save()
                refresh = RefreshToken.for_user(usuario)
                refresh['rol'] = usuario.rol

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                usuario = get_object_or_404(Usuario, pk=pk)
                serializer = UsuarioSerializer(usuario)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_usuarios = Usuario.objects.all()
                serializer = UsuarioSerializer(lista_usuarios, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID del usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            usuario = get_object_or_404(Usuario, pk=pk)

            if 'password' in request.data:
                usuario.set_password(request.data['password'])
                request.data['password'] = usuario.password
            
            username = request.data.get('username')
            if Usuario.objects.filter(username=username).exists():
                return Response({'message': f'El Usuario {username} ya está registrado.'},status=status.HTTP_400_BAD_REQUEST)

            serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Usuario {nombre} actualizado correctamente'.format(nombre=usuario.nombre)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = get_object_or_404(Usuario, pk=pk)
            usuario.delete()
            return Response({'message': 'Usuario {nombre} eliminado correctamente'.format(nombre=usuario.nombre)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EmpresaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            rut = request.data.get('rut')
            if Empresa.objects.filter(rut=rut).exists():
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = EmpresaSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Empresa {nombre} creada correctamente'.format(nombre=serializer.data['nombre'])}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk:
            try:
                empresa = get_object_or_404(Empresa, pk=pk)
                serializer = EmpresaSerializer(empresa)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_empresas = Empresa.objects.all()
                serializer = EmpresaSerializer(lista_empresas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID de la empresa es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            empresa = get_object_or_404(Empresa, pk=pk)

            rut = request.data.get('rut')
            if (Empresa.objects.filter(rut=rut).exists() and empresa.rut != rut):
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = EmpresaSerializer(empresa, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Empresa {nombre} actualizada correctamente'.format(nombre=empresa.nombre)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la empresa es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            empresa = get_object_or_404(Empresa, pk=pk)
            empresa.delete()
            return Response({'message': 'Empresa {nombre} eliminada correctamente'.format(nombre=empresa.nombre)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AgricultorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            rut = request.data.get('rut')
            if Agricultor.objects.filter(rut=rut).exists():
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = AgricultorSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Agricultor {nombre} creado correctamente'.format(nombre=serializer.data['nombre'])}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None, empresa_id=None):
        if pk:
            try:
                agricultor = get_object_or_404(Agricultor, pk=pk)
                serializer = AgricultorSerializer(agricultor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif empresa_id:
            try:
                agricultores = Agricultor.objects.filter(empresa_id=empresa_id)
                serializer = AgricultorSerializer(agricultores, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_agricultores = Agricultor.objects.all()
                serializer = AgricultorSerializer(lista_agricultores, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID de la agricultor es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            agricultor = get_object_or_404(Agricultor, pk=pk)

            rut = request.data.get('rut')
            if (Agricultor.objects.filter(rut=rut).exists() and agricultor.rut != rut):
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = AgricultorSerializer(agricultor, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Agricultor {nombre} actualizado correctamente'.format(nombre=agricultor.nombre)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la agricultor es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            agricultor = get_object_or_404(Agricultor, pk=pk)
            agricultor.delete()
            return Response({'message': 'Agricultor {nombre} eliminado correctamente'.format(nombre=agricultor.nombre)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChoferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            rut = request.data.get('rut')
            if Chofer.objects.filter(rut=rut).exists():
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ChoferSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Chofer {nombre} creado correctamente'.format(nombre=serializer.data['nombre'])}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk:
            try:
                chofer = get_object_or_404(Chofer, pk=pk)
                serializer = ChoferSerializer(chofer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_chofers = Chofer.objects.all()
                serializer = ChoferSerializer(lista_chofers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID de la chofer es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            chofer = get_object_or_404(Chofer, pk=pk)

            rut = request.data.get('rut')
            if (Chofer.objects.filter(rut=rut).exists() and chofer.rut != rut):
                return Response(
                    {'message': f'El RUT {rut} ya está registrado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ChoferSerializer(chofer, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Chofer {nombre} actualizado correctamente'.format(nombre=chofer.nombre)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la chofer es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chofer = get_object_or_404(Chofer, pk=pk)
            chofer.delete()
            return Response({'message': 'Chofer {nombre} eliminado correctamente'.format(nombre=chofer.nombre)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MaquinariaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            patente = request.data.get('patente')
            if Maquinaria.objects.filter(patente=patente).exists():
                return Response(
                    {'message': f'La patente {patente} ya está registrada.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MaquinariaSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Maquinaria {patente} creada correctamente'.format(patente=serializer.data['patente'])}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk:
            try:
                maquinaria = get_object_or_404(Maquinaria, pk=pk)
                serializer = MaquinariaSerializer(maquinaria)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_maquinarias = Maquinaria.objects.all()
                serializer = MaquinariaSerializer(lista_maquinarias, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID de la maquinaria es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            maquinaria = get_object_or_404(Maquinaria, pk=pk)

            patente = request.data.get('patente')
            if (Maquinaria.objects.filter(patente=patente).exists() and maquinaria.patente != patente):
                return Response(
                    {'message': f'La patente {patente} ya está registrada.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MaquinariaSerializer(maquinaria, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Maquinaria {patente} actualizada correctamente'.format(patente=maquinaria.patente)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la maquinaria es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            maquinaria = get_object_or_404(Maquinaria, pk=pk)
            maquinaria.delete()
            return Response({'message': 'Maquinaria {patente} eliminada correctamente'.format(patente=maquinaria.patente)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class TransporteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = TransporteSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Transporte ID {id} creado correctamente'.format(id=serializer.data['id'])}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk:
            try:
                transporte = get_object_or_404(Transporte, pk=pk)
                serializer = TransporteSerializer(transporte)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lista_transportes = Transporte.objects.all()
                serializer = TransporteSerializer(lista_transportes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        try:
            if not pk:
                return Response({'message': 'El ID del transporte es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            transporte = get_object_or_404(Transporte, pk=pk)

            serializer = TransporteSerializer(transporte, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Transporte ID {id} actualizado correctamente'.format(id=transporte.id)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, pk=None):
        if not pk:
            return Response({'message': 'El ID de la transporte es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transporte = get_object_or_404(Transporte, pk=pk)
            idTransporte = transporte.id
            transporte.delete()
            return Response({'message': 'Transporte ID {id} eliminado correctamente'.format(id=idTransporte)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CrearYAdjuntarJiraIssueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CrearJiraIssueSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            assigned_person = user.nombre

            issue = JiraAPI.create_issue(
                issue_type=serializer.validated_data.get("issue_type", "Error"),
                summary=serializer.validated_data["summary"],
                description=serializer.validated_data["description"],
                assigned_person=assigned_person
            )

            file = request.FILES.get("file")
            if file:
                file_path = f"/tmp/{file.name}"
                with open(file_path, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                response = JiraAPI.attach_file(issue["id"], file_path)

                if "error" in response:
                    return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            return Response({
                    'message': 'Gracias por informarnos de la incidencia. Trabajaremos para atenderla lo antes posible.'
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)