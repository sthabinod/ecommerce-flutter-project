from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.product.models import Product,Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        
        
        
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields=['name','description']
        
        