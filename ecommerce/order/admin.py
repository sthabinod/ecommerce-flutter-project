from django.contrib import admin
from ecommerce.order.models import Order, OrderItem, Cart, CartItems

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItems)