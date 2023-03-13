from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.users.api.v1.views import (
    UserLoginView,UserRegisterView,ChangePassword,VerifyOTP,ResetPasswordSend,VerifyOTPReset,ChangePasswordAfterOTP
)



app_name = "users"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTP.as_view(), name="verify_otp"),
    path("reset-password/", ResetPasswordSend.as_view(), name="reset_password_sent"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("change-password/", ChangePassword.as_view(), name="change_password"),
    path("verify-otp-reset/", VerifyOTPReset.as_view(), name="verify_otp_reset"),
    path("change-password-after-otp/<int:id>", ChangePasswordAfterOTP.as_view(), name="change_password_after_otp"),
    # path(
    #     "request-reset-email/userID/<int:userID>/",
    #     RequestPasswordResetEmail.as_view(),
    #     name="request-reset-email",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     PasswordTokenCheckAPI.as_view(),
    #     name="password-reset-confirm",
    # ),
    # path(
    #     "password-reset-complete/",
    #     SetNewPasswordAPIView.as_view(),
    #     name="password-reset-complete",
    # ),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)