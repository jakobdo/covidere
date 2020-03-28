from django.contrib import admin
from shop.models import Shop, Zipcode

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


class ZipcodeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)
admin.site.register(Zipcode, ZipcodeAdmin)
