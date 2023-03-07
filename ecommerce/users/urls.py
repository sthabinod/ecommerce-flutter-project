from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)



app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)