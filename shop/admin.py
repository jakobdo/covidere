from django.contrib import admin
from shop.models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


admin.site.register(Shop, ShopAdmin)
