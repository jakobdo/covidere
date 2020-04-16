from django.contrib import admin
from shop.models import Shop, Postcode


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


class PostcodeAdmin(admin.ModelAdmin):
    list_display = ('postcode', 'city', 'active')
    search_fields = ['postcode']
    list_filter = ('active', )

admin.site.register(Shop, ShopAdmin)
admin.site.register(Postcode, PostcodeAdmin)
