from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem,Cart,CartItems
from ecommerce.product.models import Product
from rest_framework import serializers,status
class OrderItemSerailizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'
        

class OrderSerailizer(ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        


class CartItemSerailizer(ModelSerializer):
    class Meta:
        model=CartItems
        fields='__all__'
        read_only_fields=('cart',)
        

    def create(self,validate_data):

        errors = {}
        user = validate_data.pop('user')
        product = self._kwargs["data"].pop("product")
        product_obj = Product.objects.get(id=product)
        quantity = self._kwargs["data"].pop("quantity")
        cart = Cart.objects.get(user=user)
        
        cart_items = CartItems.objects.create(product=product_obj,quantity=quantity,cart=cart)
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return validate_data
     
class CartSerailizer(ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
    
        
        