from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem,Cart,CartItems
from ecommerce.product.models import Product,Size,Color,Stock
from rest_framework import serializers,status
from ecommerce.product.api.v1.serializers import ProductSerializer,SizeSerializer,ColorSerializer

class OrderItemWriteSerailizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields=('id','product','quantity','order','size','color')
        read_only_fields=('order','shipping_fee')

    
    def create(self, validated_data):
        # order=Order.objects.create(user=self.context.get('user'))
        validated_data.update({'order':self.context.get('order')})
        return super().create(validated_data)
    
    
    
class OrderItemSerailizer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=OrderItem
        fields=('id','product','quantity','order','size','color','shipping_fee')
        read_only_fields=('order','shipping_fee')

 
 
class VerifyStockSerializer(Serializer):
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), source='size_set')
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), source='color_set')
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product_set')
    quantity = serializers.IntegerField(read_only=True)
    class Meta:
        fields=['product','size','color']

    def validate(self,attrs):
        errors = {}
        product = attrs.get("product_set")
        size = attrs.get("size_set")
        color = attrs.get("color_set")    
        
        if Stock.objects.filter(product=product,size=size,color=color):
            if Stock.objects.get(product=product,size=size,color=color).quantity<=0:
                errors["out_of_stock"]="No stock available with this product"  
            else:
                attrs['quantity']=Stock.objects.get(product=product,size=size,color=color).quantity
                return attrs  
        else:
            errors["no_stock"]="No stock found"  

        if errors:
            raise serializers.ValidationError(
               {
                   "status":"Not Found",
                   "statusCode":status.HTTP_404_NOT_FOUND,
                   "message":errors}
            )  
class CheckOutSerializer(ModelSerializer):
    
    # my_calculated_field = serializers.SerializerMethodField()
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), source='size', write_only=True
    )

    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True
    )
    # def get_my_calculated_field(self, obj):
    #     sum=0
    #     # calculate the value for the field
    #     product = obj["product"]
    #     total = obj['quantity']*product.price
    #     sum +=total
    #     # return the calculated value
    #     return sum
    
    # def get_total_value(self, obj):
    #     total_value = 0
        
    #     total_value += self.get_my_calculated_field(obj)
    #     return total_value
    
    class Meta:
        model=CartItems
        fields=['id','product','product_id','quantity','cart','size','size_id','color','color_id']
        read_only_fields=('cart',)



    # def validate(self, data):
    #     sum = 0
    #     errors = {}
    #     product = data["product"]
    #     sum +=product.price
    #     data['sum']=sum
    #     print(data)
    #     if errors:
    #         raise serializers.ValidationError(
    #             {
    #                 "status": "fail",
    #                 "statusCode": status.HTTP_400_BAD_REQUEST,
    #                 "errors": errors,
    #             }
    #         )
    #     return data

class OrderSerailizer(ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        


class CartItemSerailizer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    class Meta:
        model=CartItems
        fields=['id','product','quantity','cart','size','color']
        read_only_fields=('cart','size','color')
        

class CartItemWriteSerailizer(ModelSerializer):
    
    class Meta:
        model=CartItems
        fields=['id','product','quantity','cart','size','color']
        read_only_fields=('cart',)
        

    def create(self,validate_data):

        errors = {}
        user = validate_data.pop('user')
        product = self._kwargs["data"].pop("product")
        color = self._kwargs["data"].pop("color")
        quantity = self._kwargs["data"].pop("quantity")
        size = self._kwargs["data"].pop("size")
        
        if Stock.objects.filter(product=product,color=color,size=size).exists():
            if Stock.objects.get(product=product,color=color,size=size).quantity>0:
                product_obj = Product.objects.get(id=product)
                size_obj = Size.objects.get(id=size)
                color_obj = Color.objects.get(id=color)
                cart = Cart.objects.get(user=user)
            
                cart_items = CartItems.objects.create(product=product_obj,quantity=quantity,cart=cart,color=color_obj,size=size_obj)
            else:
                raise serializers.ValidationError(
                    {
                        "status": "fail",
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "message": "Product is out of stock",
                    }
                )
        else:
            raise serializers.ValidationError(
                    {
                        "status": "fail",
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "message": "Product with this size and color is not available",
                    }
                )
            
      
        return validate_data
     
class CartSerailizer(ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
    
        