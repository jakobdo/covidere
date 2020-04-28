from django.contrib import admin

from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'offer_price', 'start_datetime', 'end_datetime', 'active')


admin.site.register(Product, ProductAdmin)
