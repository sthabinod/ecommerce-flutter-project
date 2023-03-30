from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.product.models import Product,Category, Color,Size,Stock
from rest_framework import serializers,status

class SizeSerializer(ModelSerializer):
    class Meta:
        model=Size
        fields=['id','title']



class ColorSerializer(ModelSerializer):
    class Meta:
        model=Color
        fields=['id','color']

class StockSerializer(ModelSerializer):
    size = serializers.CharField(source='size.title', read_only=True)
    color = ColorSerializer(read_only=True)
    class Meta:
        model=Stock
        fields=['product','color','size','quantity']
    

class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','image','description']

class ProductSerializer(ModelSerializer):
    stock = StockSerializer(source="stock_set", read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','name','description','price','image','category','sizes','colors','stock']
        
    def get_sizes(self, obj):
        size_ids = obj.stock_set.values_list("size", flat=True).distinct()
        sizes = Size.objects.filter(id__in=size_ids)
        serializer = SizeSerializer(sizes, many=True)
        return serializer.data
    def get_colors(self, obj):
        color_ids = obj.stock_set.values_list("size", flat=True).distinct()
        colors = Color.objects.filter(id__in=color_ids)
        serializer = ColorSerializer(colors, many=True)
        return serializer.data
    
        
        

        


class PriceProductSearchSerializer(serializers.Serializer):
    from_price = serializers.IntegerField()
    to_price = serializers.IntegerField()
        
        
  
        