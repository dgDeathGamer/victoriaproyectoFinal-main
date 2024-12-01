from django.contrib import admin
from .models import Producto, Categoria, Inventario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Muestra el nombre y descripción de las categorías
    search_fields = ('nombre',)  # Permite buscar categorías por nombre
    ordering = ('nombre',)  # Ordena las categorías alfabéticamente

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'stock_minimo')  # Muestra el nuevo campo de categoría
    search_fields = ('nombre', 'categoria__nombre')  # Permite buscar productos por nombre o categoría
    list_filter = ('categoria', 'precio')  # Filtra productos por categoría o rango de precios
    ordering = ('nombre',)  # Ordena los productos alfabéticamente

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'fecha')  # Muestra información del movimiento
    search_fields = ('producto__nombre',)  # Permite buscar movimientos por nombre de producto
    list_filter = ('tipo_movimiento', 'fecha')  # Filtra movimientos por tipo o fecha
    ordering = ('-fecha',)  # Ordena los movimientos por fecha descendente
