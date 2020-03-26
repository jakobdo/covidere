from django.urls import path
from shop.views import ShopIndexView


urlpatterns = [
    path('', ShopIndexView.as_view(), name="shop_index"),
]