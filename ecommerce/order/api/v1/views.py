from rest_framework.views import APIView
from ecommerce.order.models import OrderItem,Order,CartItems,Cart
from ecommerce.product.models import Product,Size,Color,Stock
from ecommerce.order.api.v1.serializers import OrderSerailizer,OrderItemSerailizer,CartItemSerailizer,CartItemWriteSerailizer,OrderItemWriteSerailizer, CheckOutSerializer,VerifyStockSerializer,VerifyMaxStockSelectionSerializer
from ecommerce.users.models import Address
from rest_framework.response import Response
from rest_framework import status

class UserOrderView(APIView):
    # permission_classes=[]
    def get(self,request,format=None):
        user = request.user
        order = Order.objects.filter(user=user)
        serializer = OrderSerailizer(order,many=True)
        return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "All Orders",
            })

class UserOrderItemByOrder(APIView):
    # permission_classes=[]
    def get(self,request,id,format=None):
        
        order_item = OrderItem.objects.filter(order=id)
        serializer = OrderItemSerailizer(order_item,many=True)
        return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "All Orders",
            })        
 
 
class CartItemByUser(APIView):
    # permission_classes=[]
    def get(self,request,format=None):
        user = request.user

        if Cart.objects.filter(user=user).exists():
            user_cart = Cart.objects.get(user=user)
            cart_item = CartItems.objects.filter(cart=user_cart)
            serializer = CartItemSerailizer(cart_item,many=True)
            return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "All Cart Items for a user",
            })
        else:
            return Response({"status":"Not Found","statusCode":status.HTTP_404_NOT_FOUND,"message":"Cart is not found for user"},status=status.HTTP_404_NOT_FOUND)      



class AddToCartView(APIView):
    serializer_class=CartItemWriteSerailizer
    def post(self,request):
        data = request.data.copy()
        # if Product.objects.filter(name__icontains=search_key).exists():
        # user_otp = User.objects.get(user=user)
        serializer = self.serializer_class(data=data)
        # if serializer.is_valid():
        if serializer.is_valid():   
            serializer.save(user=request.user)
            return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "Cart added successfully",
                }
              )
         
        else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "error": serializer.errors},status=status.HTTP_404_NOT_FOUND)
                
          
class OrderProductView(APIView):
    serializer_class=OrderItemWriteSerailizer
    def post(self,request):
        print(request.data)
        address_id = request.data[0]['address']
        address = None
        if Address.objects.filter(id=address_id).exists():
            address = Address.objects.get(id=address_id) 
        total =request.data[-1]['total']
        print(total)
        order=Order.objects.create(user=request.user,address=address,total=total)
        serializer = self.serializer_class(data=request.data,many=True, context={'order':order})
        if serializer.is_valid():  
            for item in request.data:
                product = Product.objects.get(id=item['product'])
                size = Size.objects.get(id=item['size'])
                color = Color.objects.get(id=item['size'])
                quantity =item['size']
                
                if Stock.objects.filter(product=product,size=size,color=color).exists():
                    Stock.objects.get(product=product,size=size,color=color).quantity-quantity
         
            serializer.save()
            return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "Order created successfully",
                }
              )
         
        else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "error": serializer.errors},
                                status=status.HTTP_404_NOT_FOUND)
                
class CheckoutView(APIView):
    serializer_class=CheckOutSerializer
    def post(self,request):
        serializer = CheckOutSerializer(data=request.data,many=True)
        if serializer.is_valid():
            total = 0
            print(request.data)
            for item in request.data:
                product = Product.objects.get(id=item['product_id'])
                sub = product.price*item['quantity']
                total+=sub
            total+=100

            # serializer.data['total']=total
            print(serializer.data)
            return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "total":total,
                "data": serializer.data,
                "message": "Fetched checkout details",
                
                
            })
        else:
            return Response({"status":"Not Found","statusCode":status.HTTP_404_NOT_FOUND,"message":serializer.errors},status=status.HTTP_404_NOT_FOUND)      
        

class VerifyStock(APIView):
    serializer_class=VerifyStockSerializer
    def post(self,request):
        serializer = VerifyStockSerializer(data=request.data)
        if serializer.is_valid():
            return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "Found details",
            })
        else:
            return Response({"status":"Not Found","statusCode":status.HTTP_404_NOT_FOUND,"message":serializer.errors}, status=status.HTTP_404_NOT_FOUND)      

class VerifyMaxStockSelection(APIView):
    serializer_class=VerifyMaxStockSelectionSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "Stock found",
            })
        else:
            return Response({"status":"Not Found","statusCode":status.HTTP_404_NOT_FOUND,"message":serializer.errors}, status=status.HTTP_404_NOT_FOUND)  