from django.contrib import admin
from ecommerce.product.models import Product, Category,Size,Color


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)