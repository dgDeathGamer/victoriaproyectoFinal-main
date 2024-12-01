from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Producto, Inventario, Categoria
from .forms import ProductoForm, CategoriaForm
from usuarios.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@login_required
def inventario_view(request):
    query = request.GET.get('q', '')

    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(categoria__nombre__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    low_stock_messages = [
        f"Advertencia: El stock de '{producto.nombre}' es bajo ({producto.stock} unidades)."
        for producto in productos if producto.es_stock_bajo()
    ]

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_type = user_profile.user_type
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    categorias = Categoria.objects.all()

    return render(request, 'inventario/inventario.html', {
        'productos': productos,
        'categorias': categorias,
        'low_stock_messages': low_stock_messages,
        'user_type': user_type,
    })

@login_required
def agregar_producto(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para agregar productos.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            Inventario.objects.create(
                producto=producto,
                cantidad=producto.stock,
                tipo_movimiento='entrada',
                descripcion='Producto agregado al inventario'
            )
            return HttpResponseRedirect(f"{reverse('inventario')}?success=true")
    else:
        form = ProductoForm()

    return render(request, 'inventario/agregar_producto.html', {'form': form})

@login_required
def agregar_categoria(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para agregar categorías.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría agregada correctamente.')
            return redirect('inventario')
    else:
        form = CategoriaForm()

    return render(request, 'inventario/agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, id):
    """
    Permite editar el nombre de una categoría específica.
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para editar categorías.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('new_category_name')  # Captura el nuevo nombre de la categoría
        if nuevo_nombre:
            categoria.nombre = nuevo_nombre
            categoria.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return HttpResponseRedirect(f"{reverse('inventario')}?categoria_actualizada=true")  # Redirige con un indicador de éxito
        else:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
            return redirect('editar_categoria', id=id)

    return render(request, 'inventario/editar_categoria.html', {'categoria': categoria})


@login_required
def eliminar_categoria(request, id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para eliminar categorías.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('inventario')
    return render(request, 'inventario/eliminar_categoria.html', {'categoria': categoria})

@login_required
def editar_producto(request, id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para editar productos.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            nuevo_stock = form.cleaned_data.get('stock')
            diferencia_stock = nuevo_stock - producto.stock
            producto = form.save()

            if diferencia_stock > 0:
                Inventario.objects.create(
                    producto=producto,
                    cantidad=diferencia_stock,
                    tipo_movimiento='entrada',
                    descripcion='Actualización de stock (entrada)'
                )
            elif diferencia_stock < 0:
                Inventario.objects.create(
                    producto=producto,
                    cantidad=abs(diferencia_stock),
                    tipo_movimiento='salida',
                    descripcion='Actualización de stock (salida)'
                )
            messages.success(request, 'Producto editado correctamente.')
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para eliminar productos.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        Inventario.objects.create(
            producto=producto,
            cantidad=producto.stock,
            tipo_movimiento='salida',
            descripcion='Producto eliminado del inventario'
        )
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('inventario')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

@login_required
def detalle_categoria(request, id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'jefe':
            messages.error(request, 'No tienes permisos para ver los detalles de la categoría.')
            return redirect('inventario')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('inventario')

    categoria = get_object_or_404(Categoria, id=id)
    return render(request, 'inventario/detalle_categoria.html', {'categoria': categoria})
