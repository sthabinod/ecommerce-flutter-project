from django.contrib.auth import get_user_model
from rest_framework import status,generics
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from ecommerce.users.api.v1.serializers import LoginSerializer,RegisterSerializer,ResetPasswordEmailRequestSerializer,PasswordTokenCheckSerilizer, SetNewPasswordSerializer, ChangePasswordSerializer
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
        
# Forgot password

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = []

    @extend_schema(
        operation_id="Send password reset link to Email",
        description="This end point is for sending link to email",
        request=ResetPasswordEmailRequestSerializer,
    )
    def post(self, request, userID):

        serializer = self.serializer_class(
            data=request.data, context={"request": request, "userID": userID}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": "we have sent yout a link to reset your password"},
            status=status.HTTP_200_OK,
        )



class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = PasswordTokenCheckSerilizer
    permission_classes = []

    @extend_schema(
        operation_id="UID and token check",
        description="This endpoint checks the uid and token is valid or not",
        request=PasswordTokenCheckSerilizer,
    )
    def get(self, request, uidb64, token):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "uidb64": uidb64, "token": token},
        )
        if serializer.is_valid():
            return Response({"success": "Success"})
        return Response(
            {"error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
        )


class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = SetNewPasswordSerializer
    http_method_names = ["patch"]

    @extend_schema(
        operation_id="Reseting new password",
        description="This endpoint reset a new password to the user",
        request=SetNewPasswordSerializer,
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": "success", "message": "password reset success"},
            status=status.HTTP_200_OK,
        )


class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    http_method_names = ["patch"]

    @extend_schema(
        operation_id="Change Password",
        description="The user password changed",
        request=ChangePasswordSerializer,
    )
    def patch(self, request):
        # must pass in serializer after login credential
        # user=self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(
            raise_exception=True,
        )
        return Response(
            {
                "status": "success",
                "statusCode": status.HTTP_200_OK,
                "message": "Password Changed",
            },
        )
