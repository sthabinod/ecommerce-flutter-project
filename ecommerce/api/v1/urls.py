from django.urls import include, path

app_name = "api_v1"

urlpatterns = [
    path("product/", include("ecommerce.product.api.v1.urls", namespace="product")),
    path("users/", include("ecommerce.users.api.v1.urls", namespace="users")),
   
]
