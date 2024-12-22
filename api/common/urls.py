from django.urls import path

from api.common.views import CrearYAdjuntarJiraIssueAPIView, RegistroUsuarioAPIView, LoginUsuarioAPIView, UsuarioAPIView, EmpresaAPIView, AgricultorAPIView, ChoferAPIView, MaquinariaAPIView, TransporteAPIView


urlpatterns = [
    path('usuarios/registro/', RegistroUsuarioAPIView.as_view(), name='registro'),
    path('usuarios/login/', LoginUsuarioAPIView.as_view(), name='login'),
    path('usuarios/', UsuarioAPIView.as_view(), name='usuarios-list'),
    path('usuarios/<int:pk>/', UsuarioAPIView.as_view(), name='usuarios-update'),
    path('empresas/', EmpresaAPIView.as_view(), name='empresas'),
    path('empresas/<int:pk>/', EmpresaAPIView.as_view(), name='empresas/pk'),
    path('agricultores/', AgricultorAPIView.as_view(), name='agricultores'),
    path('agricultores/<int:pk>/', AgricultorAPIView.as_view(), name='agricultores/pk'),
    path('agricultores/empresa/<int:empresa_id>/', AgricultorAPIView.as_view(), name='agricultores/id-empresa'),
    path('choferes/', ChoferAPIView.as_view(), name='chofers'),
    path('choferes/<int:pk>/', ChoferAPIView.as_view(), name='chofers/pk'),
    path('maquinarias/', MaquinariaAPIView.as_view(), name='maquinarias'),
    path('maquinarias/<int:pk>/', MaquinariaAPIView.as_view(), name='maquinarias/pk'),
    path('transportes/', TransporteAPIView.as_view(), name='transportes'),
    path('transportes/<int:pk>/', TransporteAPIView.as_view(), name='transportes/pk'),
    path("jira/issues/", CrearYAdjuntarJiraIssueAPIView.as_view(), name="crear_y_adjuntar_jira_issue")
]