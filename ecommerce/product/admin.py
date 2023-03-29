from django.contrib import admin
from ecommerce.product.models import Product, Category,Size,Color,Stock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print("Hello WOlrd ***********************************************")
        # # Send email notification
        # send_mail(
        #     'New product added',
        #     f'A new product with name {obj.name} has been added.',
        #     'admin@example.com',
        #     ['notifications@example.com'],
        #     fail_silently=False,
        # )
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Stock)

