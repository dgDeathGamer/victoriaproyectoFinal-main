from django.urls import path
from .views import (
    inventario_view, 
    editar_producto, 
    eliminar_producto, 
    agregar_producto, 
    agregar_categoria,  # Vista para agregar categorías
    editar_categoria,  # Vista para editar categorías
    eliminar_categoria,  # Vista para eliminar categorías
    detalle_categoria  # Vista para el detalle de categorías
)

urlpatterns = [
    path('', inventario_view, name='inventario'),  # URL para la vista del inventario
    path('agregar/', agregar_producto, name='agregar_producto'),  # URL para agregar un nuevo producto
    path('editar/<int:id>/', editar_producto, name='editar_producto'),  # URL para editar un producto
    path('eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),  # URL para eliminar un producto
    path('agregar-categoria/', agregar_categoria, name='agregar_categoria'),  # URL para agregar categorías
    path('editar-categoria/<int:id>/', editar_categoria, name='editar_categoria'),  # URL para editar categorías
    path('eliminar-categoria/<int:id>/', eliminar_categoria, name='eliminar_categoria'),  # URL para eliminar categorías
    path('detalle-categoria/<int:id>/', detalle_categoria, name='detalle_categoria'),  # URL para ver el detalle de una categoría
]
