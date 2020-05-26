from django.urls import path

from shop.altenviews import ShopDetailView, ShopListView, ShopActivateView

urlpatterns = [
    path('', ShopListView.as_view(), name="alten_shop_list"),
    path('<int:pk>/', ShopDetailView.as_view(), name="alten_shop_detail"),
    path('<int:pk>/activate/', ShopActivateView.as_view(), name="alten_shop_activate"),
]
