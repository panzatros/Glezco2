from django.contrib import admin
from .models import productos, DireccionEntrega, OrderItem, Order, Perfil



admin.site.register(productos)
admin.site.register(DireccionEntrega)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Perfil)

