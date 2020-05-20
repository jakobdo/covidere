from django.urls import path
from basket.views import BasketAddView, BasketIndexView, BasketUpdateView


urlpatterns = [
    path('', BasketIndexView.as_view(), name="basket_index"),
    path('add/', BasketAddView.as_view(), name="basket_add"),
    path('update/', BasketUpdateView.as_view(), name="basket_update"),
]
