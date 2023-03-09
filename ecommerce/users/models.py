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
    #: First and last name do not cover name patterns around the globe
    full_name = CharField(_("Name of User"), blank=True, max_length=255)
    # username = None  # type: ignore
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    middle_name = None
    email = models.EmailField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['username'] 
    mobile_number = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    objects = CustomUserManager()
    
    
    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.email})


class Address(TimeStampAbstractModel):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.IntegerField()
    country= models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.street
    

class UserProfile(TimeStampAbstractModel):
    profile_image = models.ImageField(upload_to='user_profile',null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)