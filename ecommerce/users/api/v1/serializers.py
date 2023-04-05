from django.contrib.auth import get_user_model
from rest_framework import serializers,status
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime
from .utils import generate_random_password,generate_otp
from django.template.loader import render_to_string
from config.settings.base import EMAIL_HOST_USER
from django.utils.encoding import force_str, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ecommerce.users.models import Address,User
from django.core.mail import send_mail
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name"]

    



class LoginSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """
    Used for user login
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        errors = {}
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        print(user)
        
        
        # email exist
        if user:
            if user.is_verified==False:
                errors["not_verified"] = "Please verify your account!"
            elif user.is_verified:
                user.last_login = datetime.now()
                user.save()

                refresh = self.get_token(user)

                response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
                }
                return response
        elif not user:
                errors["email"] = "Invalid Credential"



            # if user.last_login == "":
            #     errors[
            #         "first_login_check"
            #     ] = "Update your profile,it's your first login"
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email","full_name","mobile_number","date_of_birth","username"]
        # extra_kwargs = {"password": {"write_only": True}}
        
        
    def create(self, validate_data):

        errors = {}

        # first_name = self._kwargs["data"].pop("first_name")
        # middle_name = self._kwargs["data"].pop("middle_name")
        # last_name = self._kwargs["data"].pop("last_name")
        # mobile_number = self._kwargs["data"].pop("mobile_number")
        email = self._kwargs["data"].pop("email")
        full_name = self._kwargs["data"].pop("full_name")
        mobile_number = self._kwargs["data"].pop("mobile_number")
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

        email_subject = "OTP Verification"
        # message = render_to_string(
        #     "email_templates/trainee_user_registration_by_admin.html",
        #     {
        #         "email": email,
        #         "password": password,
        #     },
        # )
        message = f"Please verify your otp, Your OTP is: {otp}"
        send_mail(email_subject, message, EMAIL_HOST_USER, [email],fail_silently=False)
        
        return validate_data

    def validate(self, data):
        errors = {}
        email = data["email"]

        if User.objects.filter(email=email).exists():
            errors["email"] = "User with this email already exists!"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return data

class ResetPasswordSendSerializer(serializers.Serializer):
    """
    Resets password using user email
    """
    

    email = serializers.EmailField(max_length=100)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = generate_otp()
            user.reset_otp=otp
            user.save()
            print(f"____________________________          {otp}           _____________________________________")
            email_subject = "OTP Verification"
        # message = render_to_string(
        #     "email_templates/trainee_user_registration_by_admin.html",
        #     {
        #         "email": email,
        #         "password": password,
        #     },
        # )
            message = f"Please verify your otp, Your OTP is: {otp}"
            send_mail(email_subject, message, EMAIL_HOST_USER, [email],fail_silently=False)

        else:
            raise serializers.ValidationError({"message": "Email is not registered!"})

        return attrs


  
  
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    
class VerifyOTPResetSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    """
    Resets password using user email
    """

    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=self.context["request"]).domain
            # relativeLink = reverse(
            #     kwargs={"link":"reset-password","uidb64": uidb64, "token": token},
            # )
            print(token)
            print(uidb64)
            print(user)
            userID = self.context.get("userID")

            if userID == 1:
                absurl = (
                    "http://"
                    + current_site
                    + "/admin/reset-password/"
                    + uidb64
                    + "/"
                    + token
                )
            else:
                absurl = (
                    "http://" + current_site + "/reset-password/" + uidb64 + "/" + token
                )

            email_body = (
                "Hello user,\n" "Please use this link to reset your password\n" + absurl
            )
            email_subject = "Reset your password"

            # data = {
            #     "email_body": email_body,
            #     "to_email": user.email,
            #     "email_subject": "Reset your password",
            # }
            # send_email(email_subject, email_body, EMAIL_HOST_USER, [email])

        else:
            raise serializers.ValidationError({"email": "Email is not registered!"})

        return attrs


class PasswordTokenCheckSerilizer(serializers.Serializer):
    """
    Checks password token
    """

    def validate(self, data):
        id = smart_str(urlsafe_base64_decode(self.context.get("uidb64")))
        token = self.context.get("token")

        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(
                "Token is not valid, please request a new one"
            )
        return data


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Sets new password
    """

    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, max_length=68, write_only=True)
    uidb64 = serializers.CharField(min_length=1, max_length=68, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Takes old_password, new_password and confirm password for changing password
    """

    old_password = serializers.CharField(min_length=4, write_only=True)
    new_password = serializers.CharField(min_length=4, write_only=True)
    confirm_password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, attrs):
        errors = {}

        user = self.context["request"].user
        current_email = user
        user = User.objects.get(email=current_email)
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        matchcheck = check_password(old_password, user.password)
        if not matchcheck:
            errors["old_password"] = "Old password does not match!"
        if new_password != confirm_password:
            errors["new_password"] = "Password does not match!"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        user.set_password(new_password)
        user.save()
        return super().validate(attrs)
    
    
  
  
class ChangePasswordAfterOTPSerializer(serializers.Serializer):
    """
    Takes old_password, new_password and confirm password for changing password
    """

    new_password = serializers.CharField(min_length=4, write_only=True)
    confirm_password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        fields = ["new_password", "confirm_password"]

    def validate(self, attrs):
        errors = {}

        user_id = self.context["id"]
        user = User.objects.get(id=user_id)
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        if new_password != confirm_password:
            errors["new_password"] = "Password does not match!"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        user.set_password(new_password)
        user.save()
        return super().validate(attrs)
    
class AddressSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model=Address
        fields=('id','name','longitude','latitude','user','default')
        read_only_fields=('user','default')

    
    def create(self, validated_data):
        # order=Order.objects.create(user=self.context.get('user'))
        validated_data.update({'user':self.context.get('user')})
        return super().create(validated_data)
    
    
class DefaultAddressSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model=Address
        fields=('default',)