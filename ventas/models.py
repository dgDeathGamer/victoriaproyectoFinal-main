from django.db import models
from inventario.models import Producto  # Asegúrate de que esta importación sea correcta

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción opcional de la venta

    def save(self, *args, **kwargs):
        # Validación y actualización del stock del producto al registrar la venta
        if self.pk is None:  # Solo disminuir el stock si es una nueva venta
            if self.cantidad > self.producto.stock:
                raise ValueError("No hay suficiente stock para realizar esta venta.")
            
            # Calcular el precio total en función del precio del producto
            self.precio_total = self.producto.precio * self.cantidad
            
            # Disminuir el stock del producto
            self.producto.stock -= self.cantidad
            self.producto.save()  # Guarda los cambios en el stock del producto
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} x {self.producto.nombre} - {self.precio_total} - {self.fecha.strftime('%Y-%m-%d')}"
