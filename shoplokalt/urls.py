"""shoplokalt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path

from product.views import ProductsView
from base.views import AboutPageView, set_language

urlpatterns = [
    path('', ProductsView.as_view(), name="index"),
    path('about/', AboutPageView.as_view(), name='about'),
    path('users/', include('base.urls')),
    path('products/', include('product.urls')),
    path('postcode/', include('postcode.urls')),
    path('basket/', include('basket.urls')),
    path('order/', include('order.urls')),
    path('shops/', include('shop.urls')),
    path('shopadmin/', include('shop.adminurls')),
    path('altenadmin/', include('shop.altenurls')),
    path('language/', set_language, name="set_language"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib import admin
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('admin/', admin.site.urls),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)