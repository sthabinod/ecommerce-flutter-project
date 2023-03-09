from django.db import models
from ecommerce.core.models import TimeStampAbstractModel
from ecommerce.product.models import Product
class Cart(TimeStampAbstractModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cart",
    )
    
    
class CartItems(TimeStampAbstractModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items",)
    
    
class Order(TimeStampAbstractModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order",
    )
    
    
class OrderItem(TimeStampAbstractModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items",)
    