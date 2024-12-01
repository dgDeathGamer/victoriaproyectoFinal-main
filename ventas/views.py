# ventas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Venta
from .forms import VentaForm
from inventario.models import Producto

# Función para verificar si el usuario es jefe o superusuario
def es_jefe(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'userprofile', None) and user.userprofile.user_type == 'jefe')

@login_required
def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto

            # Validar que haya suficiente stock antes de registrar la venta
            if producto.stock >= venta.cantidad:
                venta.precio_total = producto.precio * venta.cantidad
                venta.save()
                
                # Actualizar el stock del producto
                producto.stock -= venta.cantidad
                producto.save()

                # Redirigir con parámetro de éxito
                return HttpResponseRedirect(f"{reverse('registrar_ventas')}?success=true")
            else:
                messages.error(request, "No hay suficiente stock para realizar esta venta.")
    else:
        form = VentaForm()
    
    productos = Producto.objects.all()
    return render(request, 'ventas/registrar_ventas.html', {'form': form, 'productos': productos})



@login_required
@user_passes_test(es_jefe)  # Restringe el acceso a usuarios con permisos de jefe
def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})
