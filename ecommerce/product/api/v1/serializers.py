from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.product.models import Product,Category, Color,Size


class SizeSerializer(ModelSerializer):
    class Meta:
        model=Size
        fields=['id','title']



class ColorSerializer(ModelSerializer):
    class Meta:
        model=Color
        fields=['id','color']


class ProductSerializer(ModelSerializer):
    color = ColorSerializer(read_only=True,many=True)
    size = SizeSerializer(read_only=True,many=True)
    class Meta:
        model=Product
        fields=['id','name','description','price','image','category','quantity','size','color']
        
        
        
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','image','description']
        
        