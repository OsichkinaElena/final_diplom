from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem




admin.site.register(Order) #OrderAdmin)
admin.site.register(OrderItem)


