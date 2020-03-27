from django.urls import path
from django.contrib.auth import views as auth_views
from shop.views import ShopIndexView, ShopUpdateView, ShopUpdatedView, ShopProductListView, ShopOverviewView, ShopOrderListView


urlpatterns = [
    path('', ShopIndexView.as_view(), name="shop_index"),
    path('update/', ShopUpdateView.as_view(), name="shop_update"),
    path('update/success/', ShopUpdatedView.as_view(), name="shop_updated"),
    path('products/', ShopProductListView.as_view(), name="shop_products"),
    path('overview/', ShopOverviewView.as_view(), name="shop_overview"),
    path('orders/', ShopOrderListView.as_view(), name="shop_orders"),
    # Auth
    path('login/', auth_views.LoginView.as_view()),
]