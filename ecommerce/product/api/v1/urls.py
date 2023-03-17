from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from ecommerce.product.api.v1 import views

app_name = "product"

urlpatterns = [
    # API base url
    path('product-list/', views.GetProduct.as_view(), name='List Product'),
    path('categories-list/', views.GetCategory.as_view(), name='List Categories'),
    path('category-product/<int:id>/', views.GetCategoryWiseProduct.as_view(), name='Filter Categories wise Filter'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(),name='Get Single Product'),
    path('product-search/<str:search_key>/', views.SearchProduct.as_view(),name='Get Searched Product'),
    path('product-filter-by-price/', views.SearchProductByPrice.as_view(),name='Get Searched Product by price'),
]

