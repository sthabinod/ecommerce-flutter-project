from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.product.models import Product,Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','description','price','image','category','quantity','created_at','updated_at']
        
        
        
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','image','description','created_at','updated_at']
        
        