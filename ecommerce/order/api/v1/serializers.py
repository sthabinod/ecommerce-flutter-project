from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem

class OrderItemSerailizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'
        

class OrderSerailizer(ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        
        
        