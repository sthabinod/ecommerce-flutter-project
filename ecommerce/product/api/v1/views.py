from rest_framework.views import APIView
from ecommerce.product.models import Product,Category
from ecommerce.product.api.v1.serializers import ProductSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from ecommerce.product.pagination import CustomPagination


class GetProduct(APIView):
    pagination_class = CustomPagination
    # permission_classes=[]
    def get(self,request,format=None):
         product = Product.objects.all()
         serializer = ProductSerializer(product,many=True)
         return Response(status=status.HTTP_200_OK,data=serializer.data)

class GetCategory(APIView):
    # permission_classes=[]
    def get(self,request,format=None):
         category = Category.objects.all()
         serializer = CategorySerializer(category,many=True)
         return Response(status=status.HTTP_200_OK,data=serializer.data)

class GetCategoryWiseProduct(APIView):
      def get(self,request,id):
        """
        This view should return a filter of category wise product
        """
        category = Product.objects.filter(category=id)
        serializer = ProductSerializer(category,many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    


class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
            {"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
        )

    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(
            {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "Product Details",
            }
            )
        except Product.DoesNotExist:
            return Response(
            {"error": "The product is not available!"}, status=status.HTTP_404_NOT_FOUND
        )

       
    
    