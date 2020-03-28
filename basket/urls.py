from django.urls import path
from django.contrib.auth import views as auth_views
from basket.views import BasketAddView, BasketIndexView


urlpatterns = [
    path('', BasketIndexView.as_view(), name="basket_index"),
    path('add/', BasketAddView.as_view(), name="add_basket"),
]