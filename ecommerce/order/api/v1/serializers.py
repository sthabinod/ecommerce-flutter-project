from rest_framework.serializers import ModelSerializer,Serializer
from ecommerce.order.models import Order,OrderItem,Cart,CartItems
from ecommerce.product.models import Product
from rest_framework import serializers,status
from ecommerce.product.api.v1.serializers import ProductSerializer

class OrderItemSerailizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields=('product','quantity','order')
        read_only_fields=('order',)
        
    
    
    
    def create(self,validated_data):

        errors = {}
        # user = validate_data.pop('user')
        # product = validate_data.pop("product")
        # quantity = validate_data.pop("quantity")
        
        # order_details = validate_data.pop('orderitem_set')
        # order = Order.objects.create(user=user)
        
        order_items = []
        
        for order in validated_data:
            obj = OrderItem(**order)
            order_items.append(obj)

        
        # new_order= OrderItem.objects.create(user=user)
      
        order_items = OrderItem.objects.bulk_create(order_items)
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return validate_data
        

class OrderSerailizer(ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        


class CartItemSerailizer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model=CartItems
        fields=['product','quantity','cart']
        read_only_fields=('cart',)
        

    def create(self,validate_data):

        errors = {}
        user = validate_data.pop('user')
        product = self._kwargs["data"].pop("product")
        product_obj = Product.objects.get(id=product)
        quantity = self._kwargs["data"].pop("quantity")
        cart = Cart.objects.get(user=user)
        
        cart_items = CartItems.objects.bulk_create(product=product_obj,quantity=quantity,cart=cart)
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
    
        