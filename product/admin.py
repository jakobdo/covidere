from django.contrib import admin

from product.models import Product, ProductImage, ProductSize, ProductColor


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime', 'end_datetime', 'active')


class ProductColorAdmin(admin.ModelAdmin):
    pass


class ProductImageAdmin(admin.ModelAdmin):
    pass


class ProductSizeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
