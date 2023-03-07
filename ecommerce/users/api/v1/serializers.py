from django.contrib.auth import get_user_model
from rest_framework import serializers,status
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime
from .utils import generate_random_password
from django.template.loader import render_to_string
from config.settings.base import EMAIL_HOST_USER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }



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
        # email exist
        if not user:
            if User.objects.filter(email=email).exists():
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
        user.last_login = datetime.now()
        user.save()

        refresh = self.get_token(user)

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email"]
        # extra_kwargs = {"password": {"write_only": True}}
        
        
    def create(self, validate_data):

        errors = {}

        # first_name = self._kwargs["data"].pop("first_name")
        # middle_name = self._kwargs["data"].pop("middle_name")
        # last_name = self._kwargs["data"].pop("last_name")
        # mobile_number = self._kwargs["data"].pop("mobile_number")
        email = self._kwargs["data"].pop("email")

        user = User.objects.create(email=email)

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        password = generate_random_password()

        user.set_password(password)
        user.save()

       

        email_subject = "TLMS Account Approval"
        message = render_to_string(
            "email_templates/trainee_user_registration_by_admin.html",
            {
                "email": email,
                "password": password,
            },
        )
        # send_email(email_subject, message, EMAIL_HOST_USER, [email])
        return validate_data

    def validate(self, data):
        errors = {}
        email = data["email"]

        if User.objects.filter(email=email).exists():
            errors["email"] = "Trainee user with this email already exists"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return data

  