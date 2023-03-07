from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from ecommerce.users.api.v1.serializers import LoginSerializer,RegisterSerializer
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserLoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = ()
    

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            # data = serializer.save()

                return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Login Successful",
                }
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    serializer_class=RegisterSerializer
    permission_classes=()
    
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Registration Successful",
                }
              )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)