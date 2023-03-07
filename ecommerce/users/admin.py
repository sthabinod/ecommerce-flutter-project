from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ecommerce.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
  
    list_display = ["email", "first_name", "is_superuser"]
    search_fields = ["first_name"]
