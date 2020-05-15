from django.urls import path
from order.views import OrderCreateView, OrderCreatedView


urlpatterns = [
    path('', OrderCreateView.as_view(), name="order"),
    path('thanks/', OrderCreatedView.as_view(), name="order_thanks"),
]
