from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem,Cart,CartItems
from ecommerce.product.models import Product,Size,Color,Stock
from rest_framework import serializers,status
from ecommerce.product.api.v1.serializers import ProductSerializer

class OrderItemWriteSerailizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields=('product','quantity','order','size','color')
        read_only_fields=('order',)

    
    def create(self, validated_data):
        # order=Order.objects.create(user=self.context.get('user'))
        validated_data.update({'order':self.context.get('order')})
        return super().create(validated_data)
    
    
    
class OrderItemSerailizer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=OrderItem
        fields=('product','quantity','order','size','color')
        read_only_fields=('order',)

 
 
 
class CheckOutSerializer(ModelSerializer):
    
    my_calculated_field = serializers.SerializerMethodField()

    def get_my_calculated_field(self, obj):
        sum=0
        # calculate the value for the field
        product = obj["product"]
        sum +=product.price
        
        # return the calculated value
        return sum
    
    class Meta:
        model=CartItems
        fields=['product','quantity','cart','size','color','my_calculated_field']
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
    product = ProductSerializer()
    
    class Meta:
        model=CartItems
        fields=['product','quantity','cart','size','color']
        read_only_fields=('cart',)
        


    
    

class CartItemWriteSerailizer(ModelSerializer):
    
    class Meta:
        model=CartItems
        fields=['product','quantity','cart','size','color']
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
    
        