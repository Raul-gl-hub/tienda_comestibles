# productos/views.py

from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido, PedidoItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
#from .templatetags.math_filters import multiply  # Asegúrate de que este import es correcto

def inicio(request):
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')  # Obtiene el ID de la categoría desde la URL
    
    if categoria_id:
     productos = Producto.objects.filter(categoria_id=categoria_id)
    else:

     productos = Producto.objects.all()

     # Paginación: 6 productos por página
    paginator = Paginator(productos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'productos/inicio.html', {'categorias': categorias, 'page_obj': page_obj})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad

    request.session['carrito'] = carrito
    messages.success(request, f"Agregaste {cantidad} x {producto.nombre} al carrito.")
    return redirect('inicio')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'productos/carrito.html', {'productos': productos, 'total': total})

@login_required
def eliminar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        messages.info(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def realizar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('inicio')

    productos = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        if producto.stock < cantidad:
            messages.error(request, f"Stock insuficiente para {producto.nombre}.")
            return redirect('ver_carrito')
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append((producto, cantidad, subtotal))

    if request.method == 'POST':
        direccion_envio = request.POST.get('direccion_envio')
        pedido = Pedido.objects.create(
            usuario=request.user,
            estado='pendiente',
            total=total,
            direccion_envio=direccion_envio,
        )
        for producto, cantidad, subtotal in productos:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio=producto.precio,
            )
            # Actualizar stock
            producto.stock -= cantidad
            producto.save()
        # Vaciar el carrito
        request.session['carrito'] = {}
        messages.success(request, "Pedido realizado exitosamente.")
        return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'productos/realizar_pedido.html', {'total': total, 'productos': productos})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'productos/detalle_pedido.html', {'pedido': pedido})

@login_required
def pagar_pedido(request, pedido_id):
    # Implementación de pago aquí
    pass  # Reemplaza con tu lógica de pago