from django.urls import path

from base.views import activate

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', activate, name="user_activate"),
]