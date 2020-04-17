from django.urls import path

from product.views import ProductsView
from shop.views import (ShopContactView, ShopRegisteredView, ShopRegisterView,
                        ShopsDetailView, ShopsListView)

urlpatterns = [
    path('', ShopsListView.as_view(), name="shops"),
    path('<int:pk>/', ShopsDetailView.as_view(), name="shop_detail"),
    path('<int:pk>/products/', ProductsView.as_view(), name="shop_product_list"),
    path('<int:pk>/contact/', ShopContactView.as_view(), name="shop_contact"),
    path('register/', ShopRegisterView.as_view(), name="shop_register"),
    path('registered/', ShopRegisteredView.as_view(), name="shop_registered"),
]
