from django.contrib import admin
from shop.models import Shop
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')

    formfield_overrides = {
        PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    }


admin.site.register(Shop, ShopAdmin)
