from django.urls import path
from django.contrib.auth import views as auth_views
from shop.adminviews import ShopUpdateView, ShopProductListView, ShopOverviewView, ShopOrderListView, ShopProductUpdateView, ShopProductCreateView, ShopOrderDetailView


urlpatterns = [
    path('', ShopOverviewView.as_view(), name="shop_overview"),
    path('update/', ShopUpdateView.as_view(), name="shop_update"),
    path('products/', ShopProductListView.as_view(), name="shop_products"),
    path('products/<int:pk>/', ShopProductUpdateView.as_view(), name="shop_product_update"),
    path('products/create/', ShopProductCreateView.as_view(), name="shop_product_create"),
    path('orders/', ShopOrderListView.as_view(), name="shop_orders"),
    path('orders/<int:pk>/', ShopOrderDetailView.as_view(), name="show_order_detail"),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name="login"),
]