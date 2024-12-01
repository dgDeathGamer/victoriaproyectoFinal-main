# reportes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reporte_view, name='reportes'),  # Página principal de reportes
    path('generar/', views.generar_reporte, name='generar_reporte'),  # URL para generar reportes con filtros
]
