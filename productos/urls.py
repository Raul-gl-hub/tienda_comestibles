# productos/urls.py

from django.urls import path
from . import views, views_auth

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views_auth.registro, name='registro'),
    path('iniciar_sesion/', views_auth.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views_auth.cerrar_sesion, name='cerrar_sesion'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar_carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_carrito/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pagar_pedido/<int:pedido_id>/', views.pagar_pedido, name='pagar_pedido'),
    # Añade otras rutas según las funcionalidades que implementes
]