from django.urls import path

from postcode.views import PostCodeView, postcodes

urlpatterns = [
    path('', PostCodeView.as_view(), name="postcode_set"),
    path('json/', postcodes, name="postcode_json"),
]
