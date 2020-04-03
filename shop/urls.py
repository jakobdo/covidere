from django.urls import path

from product.views import IndexView
from shop.views import ShopsDetailView, ShopsListView, ShopContactView

urlpatterns = [
    path('', ShopsListView.as_view(), name="shops"),
    path('<int:pk>/', ShopsDetailView.as_view(), name="shop_detail"),
    path('<int:pk>/products/', IndexView.as_view(), name="shop_product_list"),
    path('<int:pk>/contact/', ShopContactView.as_view(), name="shop_contact"),
]