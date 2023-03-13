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
        read_only_fields=('cart',)
        

    def create(self, validate_data,request):

        errors = {}
        cart = request.user
        # first_name = self._kwargs["data"].pop("first_name")
        # middle_name = self._kwargs["data"].pop("middle_name")
        # last_name = self._kwargs["data"].pop("last_name")
        # mobile_number = self._kwargs["data"].pop("mobile_number")
        product = self._kwargs["data"].pop("product_id")
        quantity = self._kwargs["data"].pop("quantity")
        cart = self._kwargs["data"].pop("mobile_number")
        date_of_birth = self._kwargs["data"].pop("date_of_birth")
        username = self._kwargs["data"].pop("username")
        

        user = User.objects.create(email=email,full_name=full_name,mobile_number=mobile_number,date_of_birth=date_of_birth,username=username)
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        password = generate_random_password()
        otp = generate_otp()
        user.username=generate_random_password()
        user.set_password(password)
        user.otp=otp
        user.save()
        print(f"____________________________          {otp}                _____________________________________")
        print(f"____________________________          {password}           _____________________________________")

class CartSerailizer(ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
        
        
        