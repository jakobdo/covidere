from django.urls import path

from product.views import ProductsNewestView, ProductsOfferView

urlpatterns = [
    path('newest/', ProductsNewestView.as_view(), name="products_newest"),
    path('offer/', ProductsOfferView.as_view(), name="products_offer"),
]