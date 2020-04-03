from django.contrib.auth import views as auth_views
from django.urls import path

from product.views import IndexView
from shop.views import ShopsDetailView, ShopsListView

urlpatterns = [
    path('', ShopsListView.as_view(), name="shops"),
    path('<int:pk>/', ShopsDetailView.as_view(), name="shops_detail"),
    path('<int:pk>/products/', IndexView.as_view(), name="shop_product_list"),
]