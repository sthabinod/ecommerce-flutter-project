from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.product.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        
        
        