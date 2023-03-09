from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from ecommerce.product.api.v1 import views

app_name = "order"

urlpatterns = [
    # API base url
    # path('list/', views.GetProduct.as_view(), name='List Product'),
]

