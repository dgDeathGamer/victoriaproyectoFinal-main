from django.contrib import admin
from .models import Venta

class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'precio_total', 'fecha')  # Campos que quieres mostrar
    search_fields = ('producto__nombre',)  # Permite buscar por nombre del producto

admin.site.register(Venta, VentaAdmin)
