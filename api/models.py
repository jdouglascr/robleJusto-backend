from django.db import models
from django.contrib.auth.models import AbstractUser
import requests
from decouple import config

JIRA_BASE_URL = config('JIRA_BASE_URL')
JIRA_USERNAME = config('JIRA_USERNAME')
JIRA_TOKEN = config('JIRA_TOKEN')

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50)
    roles = [
        ('Administrador', 'Administrador'),
        ('Asistente', 'Asistente'),
    ]
    rol = models.CharField(max_length=20, choices=roles)

    def __str__(self):
        return self.nombre or self.username

class Empresa(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    giro = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)

class Agricultor(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='empresa_id')

class Chofer(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)
    cuenta_bancaria = models.JSONField()

class Maquinaria(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    tipos = [
        ('Camión', 'Camión'),
        ('Carro de Arrastre', 'Carro de Arrastre')
    ]
    tipo = models.CharField(max_length=20, choices=tipos)
    ubicacion = models.CharField(max_length=100)

class Transporte(models.Model):
    fecha_transporte = models.DateTimeField()
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='empresa_id')
    agricultor_id = models.ForeignKey(Agricultor, on_delete=models.CASCADE, db_column='agricultor_id')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia = models.FloatField()
    precio = models.IntegerField()
    maquinaria_id = models.ForeignKey(Maquinaria, on_delete=models.CASCADE, db_column='maquinaria_id')
    chofer_id = models.ForeignKey(Chofer, on_delete=models.CASCADE, db_column='chofer_id')
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')
    estados = [
        ('Por hacer', 'Por hacer'),
        ('En curso', 'En curso'),
        ('Finalizado', 'Finalizado'),
        ('Cobrado', 'Cobrado'),
        ('Pagado', 'Pagado')
    ]
    estado = models.CharField(max_length=10, choices=estados)

class JiraAPI:
    @staticmethod
    def create_issue(issue_type, summary, description, assigned_person, project_id="10005"):
        url = f"{JIRA_BASE_URL}issue"
        headers = {
            "Content-Type": "application/json",
        }
        auth = (JIRA_USERNAME, JIRA_TOKEN)
        payload = {
            "fields": {
                "project": {"id": project_id},
                "issuetype": {"name": issue_type},
                "summary": f"[{issue_type}] {summary}",
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description}
                            ]
                        }
                    ]
                },
                "customfield_10039": assigned_person,
            }
        }
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        return response.json()
    
    @staticmethod
    def attach_file(issue_id, file_path):
        url = f"{JIRA_BASE_URL}issue/{issue_id}/attachments"
        headers = {
            "X-Atlassian-Token": "no-check",
        }
        auth = (JIRA_USERNAME, JIRA_TOKEN)
        files = {"file": open(file_path, "rb")}

        response = requests.post(url, headers=headers, files=files, auth=auth)
        return response.json()