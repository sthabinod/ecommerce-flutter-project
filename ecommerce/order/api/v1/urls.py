from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from ecommerce.order.api.v1 import views

app_name = "order"

urlpatterns = [
    # API base url
    path('list-user-order/', views.UserOrderView.as_view(), name='User Order'),
    path('list-order-items-by-order/<uuid:id>/', views.UserOrderItemByOrder.as_view(), name='User Order Items By Order'),
    path('list-cart-items-by-user/', views.CartItemByUser.as_view(), name='User Order Items By Order'),
]

