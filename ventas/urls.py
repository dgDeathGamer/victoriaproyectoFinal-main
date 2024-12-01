from django.urls import path
from .views import registrar_venta, lista_ventas

urlpatterns = [
    path('registrar/', registrar_venta, name='registrar_ventas'),  # URL para registrar ventas
    path('lista_ventas/', lista_ventas, name='lista_ventas'),      # URL para la lista de ventas exclusiva para el jefe
]
