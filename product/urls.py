from django.urls import path

from product.views import ProductsNewestView, ProductsOnSaleView

urlpatterns = [
    path('newest/', ProductsNewestView.as_view(), name="products_newest"),
    path('onsale/', ProductsOnSaleView.as_view(), name="products_onsale"),
]