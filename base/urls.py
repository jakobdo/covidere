from django.urls import path

from base.views import ActivateUserView

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', ActivateUserView.as_view(), name="user_activate"),
]