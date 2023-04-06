from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from ecommerce.core.models import TimeStampAbstractModel
from .managers import CustomUserManager
class User(AbstractUser):
    """
    Default custom user model for Ecommerce.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    #: First and last name do not cover name patterns around the globe
    full_name = CharField(_("Name of User"), blank=True, max_length=255)
    # username = None  # type: ignore
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    middle_name = None
    email = models.EmailField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['username'] 
    mobile_number = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)
    reset_otp = models.CharField(max_length=6)
    date_of_birth = models.DateField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    objects = CustomUserManager()
    
    
    def __str__(self) -> str:
        return self.email


class Address(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    longitude = models.DecimalField(max_digits=10,decimal_places=5)
    latitude = models.DecimalField(max_digits=10,decimal_places=5)
    default = models.BooleanField(blank=True,null=True,default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    

class UserProfile(TimeStampAbstractModel):
    profile_image = models.ImageField(upload_to='user_profile',null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)