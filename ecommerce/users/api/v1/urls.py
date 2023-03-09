from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.users.api.v1.views import (
    UserLoginView,UserRegisterView,RequestPasswordResetEmail,PasswordTokenCheckAPI,SetNewPasswordAPIView,ChangePassword
)



app_name = "users"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path(
        "request-reset-email/userID/<int:userID>/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)