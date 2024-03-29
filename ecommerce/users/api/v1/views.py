from django.contrib.auth import get_user_model
from rest_framework import status,generics
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from ecommerce.users.api.v1.serializers import LoginSerializer,RegisterSerializer,ResetPasswordEmailRequestSerializer,PasswordTokenCheckSerilizer, SetNewPasswordSerializer, ChangePasswordSerializer,VerifyOTPSerializer,ResetPasswordSendSerializer,VerifyOTPResetSerializer,ChangePasswordAfterOTPSerializer,AddressSerializer,DefaultAddressSerializer
from drf_spectacular.utils import extend_schema, inline_serializer
from ecommerce.users.models import Address
from ecommerce.users.api.v1.serializers import UserSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()

class ListAddressByUser(APIView):
    def get(self,request,format=None):
        user = request.user
        if Address.objects.filter(user=user).exists():
            user_address = Address.objects.filter(user=user)
            serializer = AddressSerializer(user_address,many=True)
            return Response( {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "All address for user fetched",
            })
        else:
            return Response({"status":"Not Found","statusCode":status.HTTP_404_NOT_FOUND,"message":"No address of the user"},status=status.HTTP_404_NOT_FOUND)      


class AddAddressByUser(APIView):
    serializer_class=AddressSerializer
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )

        if serializer.is_valid():

            data = serializer.save()

            return Response(    
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Add address Successful",
                }
            )

        else:
            return Response({"status": "fail",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "Address add fail!"},status=status.HTTP_404_NOT_FOUND)

class AddressDefaultUpdate(APIView):
    serializer_class=DefaultAddressSerializer   
    def patch(self,request,**kwargs):
        id = kwargs.get('id') 
        print(id)
        instance = get_object_or_404(Address, id=id) 
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_address = Address.objects.filter(user=request.user)
            for address in user_address:
                address.default=False
                address.save()
            serializer.save()
            return Response(
                {"success": "success", "message": f"Default status changed for Address, {instance} to true"},
            status=status.HTTP_200_OK,
            )
        else:
            return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "Could not change default status for Address!"},status=status.HTTP_404_NOT_FOUND)


class UpdateAddress(APIView):
    serializer_class=AddressSerializer   
    def patch(self,request,**kwargs):
        id = kwargs.get('id') 
        print(id)
        instance = get_object_or_404(Address, id=id) 
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"success": "success", "message": "Address updated successfully!"},
            status=status.HTTP_200_OK,
            )
        else:
            return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "Address could not updated successfully!"},status=status.HTTP_404_NOT_FOUND)

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



class VerifyOTP(APIView):
    serializer_class=VerifyOTPSerializer
    permission_classes = ()
    def post(self,request):
      
        data = request.data
        print(data)
        # if Product.objects.filter(name__icontains=search_key).exists():
        # user_otp = User.objects.get(user=user)
        # serializer = self.serializer_class(data=request.data,context={"request":request})
        # if serializer.is_valid():
        if User.objects.filter(email=request.data['email']):
            user = User.objects.get(email=request.data['email'])
            if request.data['otp']==user.otp:
                user.is_verified=True
                user.save()
                return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "OTP Verified Successful",
                    "user_id":user.id
                }
              )
            else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "OTP is not matched"},status=status.HTTP_404_NOT_FOUND)
        else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "User not found with this email address!"},status=status.HTTP_404_NOT_FOUND)

class VerifyOTPReset(APIView):
    serializer_class=VerifyOTPResetSerializer
    permission_classes = ()
    def post(self,request):
        data = request.data
        print(data)
        # if Product.objects.filter(name__icontains=search_key).exists():
        # user_otp = User.objects.get(user=user)
        # serializer = self.serializer_class(data=request.data,context={"request":request})
        # if serializer.is_valid():
        if User.objects.filter(reset_otp=request.data['otp']):
            user = User.objects.get(reset_otp=request.data['otp'])
            if request.data['otp']==user.reset_otp:
           
                
                return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "OTP Verified Successful",
                    "user_id":user.id
                }
              )
            else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "OTP is not matched"},status=status.HTTP_404_NOT_FOUND)
        else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": "OTP expired or not found!"},status=status.HTTP_404_NOT_FOUND)




class ResetPasswordSend(APIView):
    serializer_class=ResetPasswordSendSerializer
    permission_classes = ()
    def post(self,request):
        data = request.data
        print(data)
        # if Product.objects.filter(name__icontains=search_key).exists():
        # user_otp = User.objects.get(user=user)
        serializer = self.serializer_class(data=request.data,context={"request":request})
        # if serializer.is_valid():
        if serializer.is_valid():   
         
                return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "OTP has been sent in your mail",
                }
              )
         
        else:
                return Response({"status": "Failue",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "error": serializer.errors},status=status.HTTP_404_NOT_FOUND)
   
            

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



class ChangePasswordAfterOTP(generics.GenericAPIView):
    serializer_class = ChangePasswordAfterOTPSerializer
    permission_classes=()
    http_method_names = ["patch"]

    @extend_schema(
        operation_id="Change Password",
        description="The user password changed",
        request=ChangePasswordAfterOTPSerializer,
    )
    def patch(self,request,id):
        # must pass in serializer after login credential
        # user=self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"id": id}
        )
        serializer.is_valid(
            raise_exception=True,
        )
        return Response(
            {
                "status": "success",
                "statusCode": status.HTTP_200_OK,
                "message": "Password has been set successfully!",
            }
        )

