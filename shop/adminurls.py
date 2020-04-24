from django.urls import path

from shop.adminviews import (ShopNewOrderListView, ShopOrderDetailView,
                             ShopOrderListView, ShopOrderStatusUpdateView,
                             ShopOverviewView, ShopProductActiveListView,
                             ShopProductCreateView,
                             ShopProductExpiringListView,
                             ShopProductInactiveListView, ShopProductListView,
                             ShopProductUpdateView, ShopUpdateView)

urlpatterns = [
    path('', ShopOverviewView.as_view(), name="shop_overview"),
    path('update/', ShopUpdateView.as_view(), name="shop_update"),
    path('products/', ShopProductListView.as_view(), name="shop_products"),
    path('products/active/', ShopProductActiveListView.as_view(), name="shop_active_products"),
    path('products/expire/', ShopProductExpiringListView.as_view(), name="shop_expire_products"),
    path('products/inactive/', ShopProductInactiveListView.as_view(), name="shop_inactive_products"),
    path('products/<int:pk>/', ShopProductUpdateView.as_view(), name="shop_product_update"),
    path('products/create/', ShopProductCreateView.as_view(), name="shop_product_create"),
    path('orders/', ShopOrderListView.as_view(), name="shop_orders"),
    path('orders/new/', ShopNewOrderListView.as_view(), name="shop_new_orders"),
    path('orders/<int:pk>/', ShopOrderDetailView.as_view(), name="show_order_detail"),
    path('orders/<int:pk>/status/', ShopOrderStatusUpdateView.as_view(), name="show_order_status_update"),
]