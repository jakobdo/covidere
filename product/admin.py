from django.contrib import admin
from product.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime', 'end_datetime', 'active')

admin.site.register(Product, ProductAdmin)
