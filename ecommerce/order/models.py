from django.db import models
from ecommerce.core.models import TimeStampAbstractModel
from ecommerce.product.models import Product,Size,Color
from ecommerce.users.models import Address
import uuid
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
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    
    
class Order(TimeStampAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order",
    )
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    
    
    
class OrderItem(TimeStampAbstractModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    
    
    
    