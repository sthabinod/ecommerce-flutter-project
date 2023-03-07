from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.users.api.v1.views import (
    UserLoginView,UserRegisterView
)



app_name = "users"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)