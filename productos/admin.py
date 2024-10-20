from django.contrib import admin
from .models import Categoria, Producto, Pedido, PedidoItem

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'estado', 'total')
    list_filter = ('estado', 'fecha')
    inlines = [PedidoItemInline]

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido, PedidoAdmin)