from rest_framework.views import APIView
from ecommerce.order.models import OrderItem,Order
from ecommerce.order.api.v1.serializers import OrderSerailizer,OrderItemSerailizer
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
         