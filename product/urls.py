from django.urls import path

from product.views import ProductsView, ProductsNewestView, ProductsOfferView, ProductsPostcodeView

urlpatterns = [
    path('', ProductsView.as_view(), name="products_list"),
    path('newest/', ProductsNewestView.as_view(), name="products_newest"),
    path('offer/', ProductsOfferView.as_view(), name="products_offer"),
    path('<int:postcode>/', ProductsPostcodeView.as_view(), name="products_postcode"),
]