from django.contrib import admin

from api.models import Empresa


# Register your models here.

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'giro', 'direccion', 'telefono', 'correo']