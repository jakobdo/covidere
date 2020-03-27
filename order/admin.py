from django.contrib import admin

from order.models import Order, OrderItem, OrderStatus

class OrderAdmin(admin.ModelAdmin):
    pass


class OrderItemAdmin(admin.ModelAdmin):
    pass


class OrderStatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)