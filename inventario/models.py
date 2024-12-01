from django.db import models
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Categoría", unique=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de la Categoría")

    def save(self, *args, **kwargs):
        """
        Reutiliza IDs eliminados al crear nuevas categorías.
        """
        if not self.pk:  # Solo aplica al crear una nueva categoría
            ids_existentes = Categoria.objects.values_list('id', flat=True).order_by('id')
            menor_id_disponible = 1
            for id_existente in ids_existentes:
                if menor_id_disponible == id_existente:
                    menor_id_disponible += 1
                else:
                    break
            self.pk = menor_id_disponible
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']


class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría"
    )  # Campo para la categoría
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(verbose_name="Cantidad en Stock", default=0)
    stock_minimo = models.PositiveIntegerField(verbose_name="Stock Mínimo", default=10)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del Producto")

    def __str__(self):
        return f"{self.nombre} - ${self.precio} - Stock: {self.stock}"

    def tiene_stock(self, cantidad):
        """
        Verifica si el producto tiene suficiente stock para una cantidad específica.
        Retorna True si hay suficiente stock, de lo contrario False.
        """
        return self.stock >= cantidad

    def es_stock_bajo(self):
        """
        Verifica si el stock actual está por debajo del nivel mínimo.
        """
        return self.stock < self.stock_minimo

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']


class Inventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de Movimiento")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Movimiento")
    descripcion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción")
    tipo_movimiento = models.CharField(
        max_length=10,
        choices=TIPOS_MOVIMIENTO,
        verbose_name="Tipo de Movimiento"
    )

    def clean(self):
        """
        Valida que el movimiento sea coherente con el stock.
        """
        if self.tipo_movimiento == 'salida' and self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock para realizar esta salida de {self.producto.nombre}.")

    def save(self, *args, **kwargs):
        """
        Actualiza el stock del producto al guardar un movimiento de inventario.
        """
        if self.pk is None:  # Solo aplicar el movimiento si es un nuevo registro
            if self.tipo_movimiento == 'entrada':
                self.producto.stock += self.cantidad
            elif self.tipo_movimiento == 'salida':
                if self.cantidad > self.producto.stock:
                    raise ValueError(f"No hay suficiente stock de {self.producto.nombre} para realizar esta salida.")
                self.producto.stock -= self.cantidad

            self.producto.save()

            # Verificar si el stock está por debajo del mínimo después de la actualización
            if self.producto.es_stock_bajo():
                # Aquí puedes agregar lógica adicional, como notificaciones por correo o logs
                print(f"Advertencia: El stock de {self.producto.nombre} está por debajo del mínimo.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        movimiento = "Entrada" if self.tipo_movimiento == 'entrada' else "Salida"
        return f"{movimiento} - {self.producto.nombre} - Cantidad: {self.cantidad} - Fecha: {self.fecha.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha']
