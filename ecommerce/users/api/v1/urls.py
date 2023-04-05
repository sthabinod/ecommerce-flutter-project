from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.users.api.v1.views import (
    UserLoginView,UserRegisterView,ChangePassword,VerifyOTP,ResetPasswordSend,VerifyOTPReset,ChangePasswordAfterOTP,ListAddressByUser,AddAddressByUser,AddressDefaultUpdate
)



app_name = "users"
urlpatterns = [
    # user login and registration
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTP.as_view(), name="verify_otp"),
    path("register/", UserRegisterView.as_view(), name="register"),
    # password reset
    path("change-password/", ChangePassword.as_view(), name="change_password"),
    path("verify-otp-reset/", VerifyOTPReset.as_view(), name="verify_otp_reset"),
    path("reset-password/", ResetPasswordSend.as_view(), name="reset_password_sent"),
    path("change-password-after-otp/<int:id>", ChangePasswordAfterOTP.as_view(), name="change_password_after_otp"),
    # address
    path("address-by-user/", ListAddressByUser.as_view(), name="address_by_user"),
    path("add-address-by-user/",AddAddressByUser.as_view(), name="add_address_by_user"),
    path("update-address-default/<int:id>",AddressDefaultUpdate.as_view(), name="update_address_default"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)