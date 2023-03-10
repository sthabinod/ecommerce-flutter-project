from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem,Cart,CartItems

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
        

class CartSerailizer(ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
        
        
        