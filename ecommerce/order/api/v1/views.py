from rest_framework.views import APIView
from ecommerce.product.models import Product
from ecommerce.product.api.v1.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status

class GetProduct(APIView):
    # permission_classes=[]
    def get(self,request,format=None):
         product = Product.objects.all()
         serializer = ProductSerializer(product,many=True)
         return Response(status=status.HTTP_200_OK,data=serializer.data)
         